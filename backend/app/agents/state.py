"""
Shared state object passed between every node in the LangGraph complaint pipeline.
Each node reads from and writes to this state — think of it as the "form"
that gets progressively filled in as the complaint moves through the workflow.
"""
from typing import TypedDict, Optional, List


class ComplaintState(TypedDict, total=False):
    # ---- Input ----
    raw_text: str                     # extracted text from email/pdf/manual entry
    source_type: str                  # "email" | "pdf" | "manual"

    # ---- Step 1: Extraction ----
    product_name: Optional[str]
    batch_number: Optional[str]
    manufacturing_date: Optional[str]
    expiry_date: Optional[str]
    customer_name: Optional[str]
    customer_organization: Optional[str]
    complaint_type: Optional[str]      # Packaging | Quality/Impurity | Adverse Reaction | Efficacy | Labeling | Other
    complaint_description: Optional[str]
    quantity_affected: Optional[str]
    product_category: Optional[str]    # API | FDF

    # ---- Step 2: Completeness check ----
    completeness_status: Optional[str]  # "Complete" | "Incomplete"
    missing_fields: Optional[List[str]]

    # ---- Step 3: Duplicate check ----
    is_duplicate: Optional[bool]
    duplicate_of_id: Optional[int]
    duplicate_confidence: Optional[float]

    # ---- Step 4: Risk classification ----
    severity_level: Optional[str]       # Critical | Major | Minor
    risk_score: Optional[float]         # 0-10
    risk_reasoning: Optional[str]

    # ---- Step 5: Root cause + CAPA (bonus) ----
    root_cause_suggestion: Optional[str]
    capa_recommendation: Optional[str]

    # ---- Step 6: Summary ----
    ai_summary: Optional[str]

    # ---- Bookkeeping ----
    errors: Optional[List[str]]
