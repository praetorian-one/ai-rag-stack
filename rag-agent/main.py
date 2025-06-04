from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag_utils import get_context_from_qdrant, query_ollama

app = FastAPI()

# Allow requests from anywhere on LAN for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    model: str = "llama3"
    top_k: int = 5

@app.post("/query")
async def query_rag(req: QueryRequest):
    context_chunks = get_context_from_qdrant(req.query, top_k=req.top_k)
    combined_context = "\n\n".join(context_chunks)
    prompt = f"Use the following documents to answer the question.\n\nContext:\n{combined_context}\n\nQuestion: {req.query}"
    answer = query_ollama(prompt, model=req.model)
    return {"answer": answer, "context": context_chunks}

@app.get("/")
async def root():
    return {"message": "RAG Agent is running."}
