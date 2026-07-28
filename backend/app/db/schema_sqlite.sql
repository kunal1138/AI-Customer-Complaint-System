-- SQLite-compatible version of the complaints schema.
-- Used for local development so you don't need to install Postgres/MySQL.

CREATE TABLE IF NOT EXISTS complaints (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_ref       TEXT UNIQUE NOT NULL,
    source_type         TEXT NOT NULL,
    raw_input_text      TEXT,
    date_received       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    product_name        TEXT,
    batch_number        TEXT,
    manufacturing_date  TEXT,
    expiry_date         TEXT,
    product_category    TEXT,

    customer_name       TEXT,
    customer_email      TEXT,
    customer_organization TEXT,

    complaint_type       TEXT,
    complaint_description TEXT,
    quantity_affected    TEXT,

    completeness_status  TEXT,
    missing_fields        TEXT,
    severity_level        TEXT,
    risk_score           REAL,
    risk_reasoning        TEXT,
    is_duplicate         INTEGER DEFAULT 0,
    duplicate_of_id       INTEGER REFERENCES complaints(id),
    duplicate_confidence  REAL,
    root_cause_suggestion TEXT,
    capa_recommendation   TEXT,
    ai_summary            TEXT,

    status               TEXT DEFAULT 'New',
    assigned_to          TEXT,

    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_complaints_batch ON complaints(batch_number);
CREATE INDEX IF NOT EXISTS idx_complaints_product ON complaints(product_name);
CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status);