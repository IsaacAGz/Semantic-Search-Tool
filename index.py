from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return{"return": "healthy", "message": "FastAPI is running on Vercel!"}

client = None


client = genai.Client(os.environ.get("GEMINI_API_KEY"))

class QueryRequest(BaseModel):
    context: str
    question: str

@app.post("/api/ask")
async def ask_demini(payload: QueryRequest):
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured on the server.")
    
    if client is None:
        raise HTTPException(status_code=500, detail="AI Client failed to initialize.")
    
    try:
        prompt = f"""
        You are a lightweight AI assitant. Use the following context to answer the the user's questions concisely.

        Context: {payload.context}
        Question: {payload.question}
        Asnwer:
        """

        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contenxt=prompt,
        )
        return {"answer": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))