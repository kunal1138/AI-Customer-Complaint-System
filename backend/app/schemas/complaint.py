from pydantic import BaseModel
from typing import Optional, List


class ComplaintTextInput(BaseModel):
    """Used when the user pastes complaint text directly (email body, manual entry)."""
    text: str
    source_type: str = "manual"  # "manual" | "email"


class ComplaintResponse(BaseModel):
    """What the frontend receives back — maps directly onto the
    'Log Customer Complaint' form + 'AI Copilot Risk Assessment' panel."""
    id: Optional[int] = None
    complaint_ref: Optional[str] = None

    product_name: Optional[str] = None
    batch_number: Optional[str] = None
    manufacturing_date: Optional[str] = None
    expiry_date: Optional[str] = None
    customer_name: Optional[str] = None
    customer_organization: Optional[str] = None
    complaint_type: Optional[str] = None
    complaint_description: Optional[str] = None
    quantity_affected: Optional[str] = None
    product_category: Optional[str] = None

    completeness_status: Optional[str] = None
    missing_fields: Optional[List[str]] = None

    is_duplicate: Optional[bool] = None
    duplicate_of_id: Optional[int] = None
    duplicate_confidence: Optional[float] = None

    severity_level: Optional[str] = None
    risk_score: Optional[float] = None
    risk_reasoning: Optional[str] = None

    root_cause_suggestion: Optional[str] = None
    capa_recommendation: Optional[str] = None
    ai_summary: Optional[str] = None
