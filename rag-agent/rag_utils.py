import requests
import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, SearchRequest, PointStruct, ScoredPoint
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "nomic-embed-text-v1.5"
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
COLLECTION_NAME = "rag_documents"

embedder = SentenceTransformer(EMBED_MODEL)
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def embed_text(text: str):
    return embedder.encode([text])[0]

def get_context_from_qdrant(query: str, top_k: int = 5):
    query_vector = embed_text(query)
    results: list[ScoredPoint] = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )
    return [point.payload.get("text", "") for point in results if point.payload]

def query_ollama(prompt: str, model: str = "llama3") -> str:
    url = f"{OLLAMA_BASE_URL}/api/generate"
    response = requests.post(url, json={"model": model, "prompt": prompt})
    response.raise_for_status()
    return response.json().get("response", "")
