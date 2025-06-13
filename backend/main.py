# from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import openai
# import os
# from dotenv import load_dotenv
# import parsers

# load_dotenv()

# # --- THIS IS THE CRITICAL LINE ---
# # Ensure this line exists and is spelled correctly.
# app = FastAPI() 
# # -----------------------------------

# # --- IMPORTANT: CORS Configuration ---
# origins = [
#     "http://localhost:8501",  # The default Streamlit port
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# openai.api_key = os.getenv("OPENAI_API_KEY")

# @app.post("/upload")
# async def upload_and_parse_file(file: UploadFile = File(...)):
#     content = await file.read()
#     parsed_data = parsers.parse_data(content, file.filename)
#     if not parsed_data:
#         raise HTTPException(status_code=400, detail="Unsupported file type")
#     return parsed_data

# @app.post("/chat")
# async def chat_with_llm(message: str = Form(...), context: str = Form(...)):
#     try:
#         prompt = f"Context:\n{context}\n\nUser Query: {message}"
#         response = openai.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}]
#         )
#         return {"reply": response.choices[0].message.content}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# backend_fastapi/main.py

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import parsers

# --- 1. IMPORT THE GOOGLE GEMINI LIBRARY ---
import google.generativeai as genai

load_dotenv()
app = FastAPI()

# --- CORS Configuration (No changes needed) ---
origins = ["http://localhost:8501"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. CONFIGURE THE GEMINI API KEY ---
# This line looks for the GOOGLE_API_KEY in your .env file.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- /upload endpoint (No changes needed) ---
@app.post("/upload")
async def upload_and_parse_file(file: UploadFile = File(...)):
    content = await file.read()
    parsed_data = parsers.parse_data(content, file.filename)
    if not parsed_data:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    return parsed_data

# --- 3. THE UPDATED /chat ENDPOINT FOR GEMINI ---
@app.post("/chat")
async def chat_with_llm(message: str = Form(...), context: str = Form(...)):
    try:
        # Use the 'gemini-pro' model for text tasks.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Based on the following data context, answer the user's query.\n\nContext:\n{context}\n\nUser Query: {message}"
        
        # Generate the response using Gemini's API
        response = model.generate_content(prompt)
        
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google Gemini API Error: {str(e)}")
