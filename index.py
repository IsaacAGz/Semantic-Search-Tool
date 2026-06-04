from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from google import genai
from dotenv import load_dotenv
import numpy as np

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return{"return": "healthy", "message": "FastAPI is running on Vercel!"}

client = None


client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class QueryRequest(BaseModel):
    context: str
    question: str

def get_embedding(text: str):
    """Helper function to generate a text vector using embeddin model"""
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
        )
    
    return response.embedding[0].values

def cosine_similarity(v1, v2):
    """Helper function to calculate cosine similarity between two embedding vectors"""
    dot_product = np.dot(v1,v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)

    return dot_product / (norm_v1 * norm_v2)

@app.post("/api/ask")
async def ask_demini(payload: QueryRequest):
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured on the server.")
    
    if client is None:
        raise HTTPException(status_code=500, detail="AI Client failed to initialize.")
    
    try:
        # Split into distinct lines / paragraphs
        chunks = [c.strip() for c in payload.context.split("\n") if len(c.strip()) > 10]

        if not chunks: 
            raise HTTPException(status_code=400, detail="provide context is too short to parse.")
        
        # Embedded user question 
        question_vector = get_embedding(payload.question)

        # Perform vector search
        scored_chunks = []
        for chunk in chunks:
            chunk_vector = get_embedding(chunk)
            score = cosine_similarity(question_vector, chunk)
            scored_chunks.append((score, chunk))

        # Sort chunks by score and pick top chunks from context to answer user question
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_matches = [item[1] for item in scored_chunks[:2]]

        # Combine matching context
        optimized_context = "\n".join(top_matches)

        prompt = f"""
        You are a lightweight AI assitant. Use the following context to answer the the user's questions concisely.

        Filtered Context Matches: 
        {optimized_context}

        Question: 
        {payload.question}
        Answer:
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return {
            "answer": response.text,
            "chunks_searched": len(chunks),
            "top_match_score": float(scored_chunks[0][0]) if scored_chunks else 0.0
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))