from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_model, load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/")
async def root():
    return{"return": "healthy", "message": "FastAPI is running on Vercel!"}

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class QueryRequest(BaseModel):
    context: str
    question: str

@app.post("/api/ask")
async def ask_demini(payload: QueryRequest):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        You are a lightweight AI assitant. Use the following context to answer the the user's questions concisely.

        Context: {payload.context}
        Question: {payload.question}
        Asnwer:
        """

        response = model.generative_content(prompt)
        return {"answer": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))