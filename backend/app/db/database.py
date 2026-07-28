"""
Database access layer. Uses SQLAlchemy Core for simplicity — swap for the ORM
if you prefer, but keeping raw-ish SQL here makes it easy to explain in the
interview exactly what queries run against Postgres/MySQL.
"""
import os
import json
from datetime import datetime
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./aivoa_complaints.db")
engine = create_engine(DATABASE_URL)
IS_SQLITE = DATABASE_URL.startswith("sqlite")


def init_db():
    schema_file = "schema_sqlite.sql" if IS_SQLITE else "schema.sql"
    with open(os.path.join(os.path.dirname(__file__), schema_file)) as f:
        schema_sql = f.read()
    with engine.begin() as conn:
        for statement in schema_sql.split(";"):
            if statement.strip():
                conn.execute(text(statement))


def generate_complaint_ref() -> str:
    year = datetime.now().year
    with engine.begin() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM complaints")).scalar()
    return f"CMP-{year}-{count + 1:04d}"


def save_complaint(state: dict, source_type: str) -> int:
    ref = generate_complaint_ref()
    with engine.begin() as conn:
        result = conn.execute(text("""
            INSERT INTO complaints (
                complaint_ref, source_type, raw_input_text, product_name, batch_number,
                manufacturing_date, expiry_date, customer_name, customer_organization,
                complaint_type, complaint_description, quantity_affected, product_category,
                completeness_status, missing_fields, is_duplicate, duplicate_of_id,
                duplicate_confidence, severity_level, risk_score, risk_reasoning,
                root_cause_suggestion, capa_recommendation, ai_summary, status
            ) VALUES (
                :ref, :source_type, :raw_text, :product_name, :batch_number,
                :manufacturing_date, :expiry_date, :customer_name, :customer_organization,
                :complaint_type, :complaint_description, :quantity_affected, :product_category,
                :completeness_status, :missing_fields, :is_duplicate, :duplicate_of_id,
                :duplicate_confidence, :severity_level, :risk_score, :risk_reasoning,
                :root_cause_suggestion, :capa_recommendation, :ai_summary, 'New'
            ) RETURNING id
        """), {
            "ref": ref,
            "source_type": source_type,
            "raw_text": state.get("raw_text"),
            "product_name": state.get("product_name"),
            "batch_number": state.get("batch_number"),
            "manufacturing_date": state.get("manufacturing_date"),
            "expiry_date": state.get("expiry_date"),
            "customer_name": state.get("customer_name"),
            "customer_organization": state.get("customer_organization"),
            "complaint_type": state.get("complaint_type"),
            "complaint_description": state.get("complaint_description"),
            "quantity_affected": state.get("quantity_affected"),
            "product_category": state.get("product_category"),
            "completeness_status": state.get("completeness_status"),
            "missing_fields": json.dumps(state.get("missing_fields") or []),
            "is_duplicate": state.get("is_duplicate", False),
            "duplicate_of_id": state.get("duplicate_of_id"),
            "duplicate_confidence": state.get("duplicate_confidence"),
            "severity_level": state.get("severity_level"),
            "risk_score": state.get("risk_score"),
            "risk_reasoning": state.get("risk_reasoning"),
            "root_cause_suggestion": state.get("root_cause_suggestion"),
            "capa_recommendation": state.get("capa_recommendation"),
            "ai_summary": state.get("ai_summary"),
        })
        return result.scalar()


def get_recent_complaints_for_dedup(product_name: str, batch_number: str, limit: int = 5) -> str:
    """Fetch a short text summary of recent complaints for the same product/batch,
    used as context for the LLM-based duplicate check node."""
    if not product_name and not batch_number:
        return ""
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT id, product_name, batch_number, complaint_description
            FROM complaints
            WHERE product_name = :product_name OR batch_number = :batch_number
            ORDER BY created_at DESC
            LIMIT :limit
        """), {"product_name": product_name, "batch_number": batch_number, "limit": limit}).fetchall()

    if not rows:
        return ""
    lines = [f"[id={r.id}] Product: {r.product_name}, Batch: {r.batch_number}, "
             f"Description: {r.complaint_description}" for r in rows]
    return "\n".join(lines)


def list_complaints(limit: int = 50):
    with engine.begin() as conn:
        rows = conn.execute(text(
            "SELECT * FROM complaints ORDER BY created_at DESC LIMIT :limit"
        ), {"limit": limit}).mappings().all()
    return [dict(r) for r in rows]


def get_complaint(complaint_id: int):
    with engine.begin() as conn:
        row = conn.execute(text(
            "SELECT * FROM complaints WHERE id = :id"
        ), {"id": complaint_id}).mappings().first()
    return dict(row) if row else None
