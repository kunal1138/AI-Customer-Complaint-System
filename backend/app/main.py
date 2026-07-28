"""
FastAPI entrypoint. Three main endpoints:

  POST /api/complaints/text     -> process pasted/typed complaint text
  POST /api/complaints/upload   -> process an uploaded PDF/email file
  GET  /api/complaints          -> list complaints (for a dashboard view)
  GET  /api/complaints/{id}     -> fetch one complaint (for detail view)

Each processing endpoint runs the LangGraph pipeline end-to-end and persists
the result, then returns a payload shaped to directly populate the frontend's
"Log Customer Complaint" form and "AI Copilot Risk Assessment" panel.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io

from app.schemas.complaint import ComplaintTextInput, ComplaintResponse
from app.agents.graph import complaint_graph
from app.db.database import save_complaint, list_complaints, get_complaint, init_db

app = FastAPI(title="AIVOA Customer Complaint Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite / CRA dev servers
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


def _run_pipeline_and_save(raw_text: str, source_type: str) -> ComplaintResponse:
    initial_state = {"raw_text": raw_text, "source_type": source_type}
    final_state = complaint_graph.invoke(initial_state)

    # The LLM sometimes returns quantity_affected as a number (e.g. 3) instead of
    # text (e.g. "3 boxes") - normalize it to a string either way.
    if final_state.get("quantity_affected") is not None:
        final_state["quantity_affected"] = str(final_state["quantity_affected"])

    complaint_id = save_complaint(final_state, source_type)
    final_state["id"] = complaint_id

    # fetch back the generated complaint_ref for the response
    saved = get_complaint(complaint_id)
    final_state["complaint_ref"] = saved["complaint_ref"] if saved else None

    return ComplaintResponse(**final_state)


@app.post("/api/complaints/text", response_model=ComplaintResponse)
def process_text_complaint(payload: ComplaintTextInput):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Complaint text cannot be empty")
    return _run_pipeline_and_save(payload.text, payload.source_type)


@app.post("/api/complaints/upload", response_model=ComplaintResponse)
async def process_uploaded_complaint(file: UploadFile = File(...)):
    contents = await file.read()

    if file.filename.lower().endswith(".pdf"):
        text_parts = []
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
        raw_text = "\n".join(text_parts)
        source_type = "pdf"
    else:
        # treat as plain text (e.g. .txt email export)
        raw_text = contents.decode("utf-8", errors="ignore")
        source_type = "email"

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from the uploaded file")

    return _run_pipeline_and_save(raw_text, source_type)


@app.get("/api/complaints")
def get_all_complaints(limit: int = 50):
    return list_complaints(limit=limit)


@app.get("/api/complaints/{complaint_id}")
def get_one_complaint(complaint_id: int):
    complaint = get_complaint(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
