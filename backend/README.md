# AIVOA Complaint Management — Backend

## Architecture

```
Frontend (React)
      |
      v
FastAPI (app/main.py)
      |
      v
LangGraph pipeline (app/agents/graph.py)
      |
      +-- extract              (LLM: gemma2-9b-it)  -> pulls structured fields from raw text
      +-- completeness_check   (rule-based)          -> flags missing required fields
      |     |
      |     +--(incomplete)--> END, returned to user for more info
      |
      +-- duplicate_check      (LLM: gemma2-9b-it)   -> compares against recent DB records
      +-- risk_classification  (LLM: gemma2-9b-it)   -> Critical/Major/Minor + risk score
      +-- root_cause_capa      (LLM: llama-3.3-70b)  -> root cause hypotheses + CAPA suggestion
      +-- summary              (LLM: gemma2-9b-it)   -> 2-sentence QA-manager summary
      |
      v
   Postgres/MySQL (app/db/database.py)
```

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in GROQ_API_KEY and DATABASE_URL
```

Create the database (Postgres example):
```bash
createdb aivoa_complaints
```
Tables are auto-created on startup via `init_db()` (see `app/db/schema.sql`).

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## Visualize the LangGraph pipeline

```bash
python -m app.agents.graph
```
Prints an ASCII diagram of the node graph — screenshot this for your demo video
to show the workflow structure alongside the code walkthrough.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/complaints/text` | Process pasted complaint text |
| POST | `/api/complaints/upload` | Process an uploaded PDF/email file |
| GET | `/api/complaints` | List all complaints |
| GET | `/api/complaints/{id}` | Get one complaint |

## Design notes (for your interview)

- **Why split into 6 nodes instead of one big prompt?** Each node maps to a real
  QMS step (intake -> triage -> investigation support), makes failures isolatable
  (e.g. you can see extraction succeeded but risk classification failed), and lets
  you swap/improve one step without touching others.
- **Why gemma2-9b-it for most steps but llama-3.3-70b for root cause/CAPA?**
  Extraction/classification are narrow, well-defined tasks where a smaller/faster
  model is sufficient and cheaper. Root cause reasoning benefits from a larger
  model's broader reasoning ability.
- **Why a conditional edge after completeness_check?** No point spending LLM calls
  on risk/CAPA analysis for a complaint that's missing the batch number — better to
  short-circuit and ask the submitter for more info first, matching real QMS intake
  practice.
- **Known limitation:** PDF parsing uses `pdfplumber` for extractable text only —
  no OCR — per the assignment's note that production-grade parsing isn't required.
