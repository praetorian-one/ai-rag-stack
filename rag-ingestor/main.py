import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from nomic import embed
import uuid

DOCUMENTS_PATH = Path("/app/documents")
QDRANT_COLLECTION = "rag_collection"

client = QdrantClient(host=os.getenv("QDRANT_HOST", "qdrant"), port=int(os.getenv("QDRANT_PORT", 6333)))

# Create the collection if it doesn't exist
if QDRANT_COLLECTION not in [col.name for col in client.get_collections().collections]:
    client.recreate_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )

def embed_and_upload(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
        if not text.strip():
            return

    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    embeds = embed(texts=chunks, model='nomic-embed-text-v1.5')['embeddings']

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vec,
            payload={"text": chunk, "source": str(file_path)}
        ) for vec, chunk in zip(embeds, chunks)
    ]

    client.upsert(collection_name=QDRANT_COLLECTION, points=points)
    print(f"✅ Ingested: {file_path}")

class DocumentHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.txt', '.md', '.pdf', '.html', '.log')):
            embed_and_upload(event.src_path)

if __name__ == "__main__":
    DOCUMENTS_PATH.mkdir(parents=True, exist_ok=True)
    event_handler = DocumentHandler()
    observer = Observer()
    observer.schedule(event_handler, str(DOCUMENTS_PATH), recursive=False)
    observer.start()
    print(f"📂 Watching for new documents in: {DOCUMENTS_PATH}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
