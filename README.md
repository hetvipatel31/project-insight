# Project Insight: Natural Language-Driven Data Analysis

This project is a no-code, AI-powered data analysis platform that enables users to interact with structured and unstructured datasets (CSV, Excel, PDF, Word) using natural language. It features a Streamlit frontend and a FastAPI backend powered by Google's Gemini LLM.

## Architecture

- **Frontend:** Streamlit (`frontend/`)
- **Backend:** FastAPI (`backend/`)

## Setup and Installation

### 1. Backend (FastAPI)

```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r req.txt
# Create a .env file with your GOOGLE_API_KEY
uvicorn main:app --reload
```

### 2. Frontend (Streamlit)

```
cd frontend
# Activate the same virtual environment
source ../backend/venv/bin/activate
pip install -r req.txt
streamlit run app.py
```
```

