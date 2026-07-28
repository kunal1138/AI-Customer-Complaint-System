-- AIVOA Customer Complaint Management System
-- Core schema (Postgres syntax; MySQL-compatible with minor type tweaks)

CREATE TABLE IF NOT EXISTS complaints (
    id                  SERIAL PRIMARY KEY,
    complaint_ref       VARCHAR(30) UNIQUE NOT NULL,       -- e.g. CMP-2026-0001
    source_type         VARCHAR(20) NOT NULL,              -- email | pdf | manual | image
    raw_input_text      TEXT,                              -- original extracted text
    date_received       TIMESTAMP DEFAULT NOW(),

    -- Product / batch identification
    product_name        VARCHAR(255),
    batch_number         VARCHAR(100),
    manufacturing_date  VARCHAR(20),
    expiry_date         VARCHAR(20),
    product_category    VARCHAR(20),                       -- API | FDF

    -- Complainant info
    customer_name       VARCHAR(255),
    customer_email      VARCHAR(255),
    customer_organization VARCHAR(255),

    -- Complaint content
    complaint_type       VARCHAR(50),                       -- Packaging, Quality/Impurity, Adverse Reaction, Efficacy, Labeling, Other
    complaint_description TEXT,
    quantity_affected    VARCHAR(100),

    -- AI-derived fields
    completeness_status VARCHAR(20),                        -- Complete | Incomplete
    missing_fields       TEXT,                               -- JSON array of missing field names
    severity_level       VARCHAR(20),                        -- Critical | Major | Minor
    risk_score          NUMERIC(4,1),                        -- 0.0 - 10.0
    risk_reasoning      TEXT,
    is_duplicate        BOOLEAN DEFAULT FALSE,
    duplicate_of_id     INTEGER REFERENCES complaints(id),
    duplicate_confidence NUMERIC(4,1),
    root_cause_suggestion TEXT,
    capa_recommendation TEXT,
    ai_summary          TEXT,

    -- Workflow status
    status              VARCHAR(30) DEFAULT 'New',           -- New | Under Investigation | CAPA Assigned | Closed
    assigned_to         VARCHAR(255),

    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_complaints_batch ON complaints(batch_number);
CREATE INDEX IF NOT EXISTS idx_complaints_product ON complaints(product_name);
CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status);
