"""
Each function here is one LangGraph node. Every node:
  1. Reads what it needs from ComplaintState
  2. Does one job (extraction, completeness check, duplicate check, etc.)
  3. Returns a dict of the fields it updates — LangGraph merges this into state

Keeping nodes single-purpose mirrors the real QMS workflow (intake -> triage ->
investigation support -> CAPA) and makes each step independently testable and
explainable in the demo video.
"""
from app.agents.state import ComplaintState
from app.agents.llm_client import call_llm_json, call_llm, EXTRACTION_MODEL, REASONING_MODEL
from app.db.database import get_recent_complaints_for_dedup


# ---------------------------------------------------------------------------
# Node 1: Extraction
# ---------------------------------------------------------------------------
EXTRACTION_SYSTEM_PROMPT = """You are a data extraction assistant for a pharmaceutical
Quality Management System (QMS). You extract structured fields from raw customer
complaint text (which may come from an email, PDF, or manual entry).

Return ONLY a JSON object with these exact keys (use null for anything not present):
product_name, batch_number, manufacturing_date, expiry_date, customer_name,
customer_organization, complaint_type, complaint_description, quantity_affected,
product_category.

complaint_type must be one of: "Packaging", "Quality/Impurity", "Adverse Reaction",
"Efficacy", "Labeling", "Other".
product_category must be one of: "API", "FDF", or null if unclear.
complaint_description should be a concise 1-3 sentence paraphrase of the actual issue.
"""

def extract_complaint_data(state: ComplaintState) -> dict:
    prompt = f"Extract structured fields from this complaint:\n\n{state['raw_text']}"
    data = call_llm_json(prompt, system=EXTRACTION_SYSTEM_PROMPT, model=EXTRACTION_MODEL)
    return data


# ---------------------------------------------------------------------------
# Node 2: Completeness check
# ---------------------------------------------------------------------------
REQUIRED_FIELDS = ["product_name", "batch_number", "complaint_description"]

def check_completeness(state: ComplaintState) -> dict:
    missing = [f for f in REQUIRED_FIELDS if not state.get(f)]
    return {
        "completeness_status": "Incomplete" if missing else "Complete",
        "missing_fields": missing,
    }


# ---------------------------------------------------------------------------
# Node 3: Duplicate detection
# ---------------------------------------------------------------------------
DUPLICATE_SYSTEM_PROMPT = """You detect duplicate pharmaceutical complaints. You will be
given a NEW complaint and a list of EXISTING complaints. Decide if the new complaint is
very likely describing the same underlying issue as one of the existing ones (same product,
same or overlapping batch, same type of defect).

Return ONLY JSON: {"is_duplicate": bool, "duplicate_of_id": int or null, "confidence": 0-100}
"""

def check_duplicates(state: ComplaintState) -> dict:
    existing = get_recent_complaints_for_dedup(
        product_name=state.get("product_name"),
        batch_number=state.get("batch_number"),
    )
    if not existing:
        return {"is_duplicate": False, "duplicate_of_id": None, "duplicate_confidence": 0.0}

    prompt = f"""NEW COMPLAINT:
Product: {state.get('product_name')}
Batch: {state.get('batch_number')}
Description: {state.get('complaint_description')}

EXISTING COMPLAINTS:
{existing}
"""
    result = call_llm_json(prompt, system=DUPLICATE_SYSTEM_PROMPT, model=EXTRACTION_MODEL)
    return {
        "is_duplicate": result.get("is_duplicate", False),
        "duplicate_of_id": result.get("duplicate_of_id"),
        "duplicate_confidence": result.get("confidence", 0.0),
    }


# ---------------------------------------------------------------------------
# Node 4: Risk classification (AI Copilot Risk Assessment)
# ---------------------------------------------------------------------------
RISK_SYSTEM_PROMPT = """You are a pharmaceutical QMS risk assessment assistant. Classify the
severity of a customer complaint using standard QMS logic:

- "Critical": patient safety risk, adverse reaction, contamination, wrong product/label,
  potency failure that could harm patients.
- "Major": quality defect that could affect efficacy or compliance but no immediate safety
  risk (e.g. significant impurity, dissolution failure).
- "Minor": cosmetic/packaging issues with no impact on safety or efficacy.

Return ONLY JSON: {"severity_level": "Critical"|"Major"|"Minor", "risk_score": 0-10,
"risk_reasoning": "2-3 sentence explanation referencing specific details from the complaint"}
"""

def classify_risk(state: ComplaintState) -> dict:
    prompt = f"""Complaint type: {state.get('complaint_type')}
Product category: {state.get('product_category')}
Description: {state.get('complaint_description')}
Quantity affected: {state.get('quantity_affected')}
"""
    result = call_llm_json(prompt, system=RISK_SYSTEM_PROMPT, model=EXTRACTION_MODEL)
    return {
        "severity_level": result.get("severity_level"),
        "risk_score": result.get("risk_score"),
        "risk_reasoning": result.get("risk_reasoning"),
    }


# ---------------------------------------------------------------------------
# Node 5: Root cause + CAPA recommendation (bonus feature, uses the larger model)
# ---------------------------------------------------------------------------
ROOT_CAUSE_SYSTEM_PROMPT = """You are a QMS investigation assistant helping a Quality
Assurance team think through a pharmaceutical complaint. Based on the complaint details,
suggest 2-3 plausible root cause categories (e.g. process deviation, packaging line issue,
storage/transport condition, raw material variability, analytical method issue) and one
reasonable CAPA (Corrective and Preventive Action) recommendation.

Be clear these are AI-generated hypotheses for the investigator to verify, not conclusions.

Return ONLY JSON: {"root_cause_suggestion": "...", "capa_recommendation": "..."}
"""

def suggest_root_cause(state: ComplaintState) -> dict:
    prompt = f"""Complaint type: {state.get('complaint_type')}
Product category: {state.get('product_category')}
Description: {state.get('complaint_description')}
Severity: {state.get('severity_level')}
"""
    result = call_llm_json(prompt, system=ROOT_CAUSE_SYSTEM_PROMPT, model=REASONING_MODEL)
    return {
        "root_cause_suggestion": result.get("root_cause_suggestion"),
        "capa_recommendation": result.get("capa_recommendation"),
    }


# ---------------------------------------------------------------------------
# Node 6: Summary generation
# ---------------------------------------------------------------------------
def generate_summary(state: ComplaintState) -> dict:
    prompt = f"""Summarize this pharmaceutical complaint in 2 sentences for a QA manager
who needs to quickly triage it:

Product: {state.get('product_name')} | Batch: {state.get('batch_number')}
Type: {state.get('complaint_type')} | Severity: {state.get('severity_level')}
Description: {state.get('complaint_description')}
"""
    summary = call_llm(prompt, model=EXTRACTION_MODEL, temperature=0.3)
    return {"ai_summary": summary.strip()}
