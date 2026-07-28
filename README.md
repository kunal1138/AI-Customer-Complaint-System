## 🎥 Demo Videos

- **Product Demo:** [Watch on YouTube](https://youtu.be/VdAci4ISgwg)
- **Code Walkthrough:** [Watch on YouTube](https://youtu.be/z7xBvKaU78g)

# 🤖 AI Customer Complaint System

An AI-powered customer complaint management system built using **React**, **Redux Toolkit**, **FastAPI**, **LangGraph**, and **Groq LLM**. The system helps collect customer complaints, analyze their severity, and provide AI-assisted responses through an intelligent workflow.

---

## 📌 Features

- 📝 Customer complaint submission
- 🤖 AI-powered complaint analysis using Groq LLM
- ⚡ Intelligent workflow with LangGraph
- 📊 Risk assessment for complaints
- 📂 Complaint history tracking
- 🔄 Redux Toolkit for state management
- 🚀 FastAPI backend with REST APIs
- 💻 Responsive React frontend

---

## 🛠️ Tech Stack

### Frontend
- React.js
- Redux Toolkit
- Vite
- CSS

### Backend
- FastAPI
- Python
- SQLite
- LangGraph
- Groq API

---

## 📂 Project Structure

```
AI-Customer-Complaint-System/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# 🚀 Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/kunal1138/AI-Customer-Complaint-System.git
cd AI-Customer-Complaint-System
```

---

## 2️⃣ Backend Setup

Go to backend folder

```bash
cd backend
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
```

Run Backend

```bash
uvicorn app.main:app --reload
```

Backend will start at

```
http://127.0.0.1:8000
```

---

## 3️⃣ Frontend Setup

Open another terminal

```bash
cd frontend
```

Install packages

```bash
npm install
```

Run frontend

```bash
npm run dev
```

Frontend will start at

```
http://localhost:5173
```

---

# 📷 Application Flow

1. User submits a complaint.
2. Complaint is sent to FastAPI.
3. LangGraph processes the complaint.
4. Groq AI analyzes severity and intent.
5. Risk level is generated.
6. Complaint is stored.
7. User can view complaint history.

---

# 📸 Screenshots

> Add screenshots here after running the project.

Example:

```
screenshots/
    home.png
    complaint-form.png
    history.png
```

---

# 🔐 Environment Variables

Create a `.env` file inside the backend directory.

```env
GROQ_API_KEY=your_api_key
```

Never upload your `.env` file to GitHub.

---

# 📖 API

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/complaints` | Submit Complaint |
| GET | `/complaints` | Get Complaint History |

---

# 🎯 Future Improvements

- User Authentication
- Admin Dashboard
- Email Notifications
- Complaint Categories
- Sentiment Analysis
- Analytics Dashboard
- Cloud Database Integration
- Docker Support

---

# 👨‍💻 Author

**Kunal Choudhari**

- GitHub: https://github.com/kunal1138

---

# 📄 License

This project is developed for learning and demonstration purposes.
