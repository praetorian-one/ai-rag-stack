# 🧠 Private AI RAG Stack

This repository contains a fully containerized AI stack designed for **self-hosted LLM inference**, **RAG-based document search**, and **LAN-accessible interfaces**. Built on top of [Ollama](https://ollama.com), [Qdrant](https://qdrant.tech), and custom FastAPI + React components, this system provides an extensible base for both research and production use.

---

## 🚀 Stack Overview

| Service       | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| 🧠 **Ollama**        | Hosts LLMs (e.g., LLaMA 3, Deepseek-Coder) for inference. Pulls models from mounted NAS. |
| 🧱 **Qdrant**        | Vector database storing document embeddings for semantic search.       |
| 🤖 **RAG Agent**     | FastAPI backend for answering questions with context via RAG.         |
| 📄 **RAG Ingestor**  | Watches `/documents` folder and auto-embeds new files into Qdrant.    |
| 🧾 **RAG Uploader**  | Simple web UI to upload documents for ingestion.                      |
| 🌐 **RAG UI**        | Full React web interface for querying the RAG system.                 |

---

## 📁 Project Structure

```
.
├── docker-compose.yml
├── .env                         # Defines NFS model path and other settings
├── documents/                   # Document ingest folder (bind-mounted)
├── rag-agent/                   # API backend that powers RAG lookups
├── rag-ingestor/                # Auto-embedding and ingestion service
├── rag-uploader/                # Simple document uploader web service
├── rag-ui/                      # Query UI for users
```

---

## 🔧 Environment Configuration

Create a `.env` file in the root directory:

```env
# NAS-mounted model directory (auto-mounted via fstab)
MODEL_PATH=/mnt/curia/ai/models
```

---

## 📦 Installation & Setup

### 1. Mount your NFS share

On the Docker host, edit `/etc/fstab`:

```fstab
NAS_IP:/exported/path/to/models /mnt/your-folder nfs defaults,_netdev 0 0
```

Then mount:

```bash
sudo mkdir -p /mnt/your-folder
sudo mount -a
```

### 2. Clone this repo and navigate into it

```bash
git clone https://your-git-server/private-ai-stack.git
cd private-ai-stack
```

### 3. Start the stack

```bash
docker compose --env-file .env up -d --build
```

---

## 🌐 Interfaces & Ports

| Component       | URL / Port           |
|----------------|----------------------|
| Ollama API      | `http://localhost:11434` |
| RAG Agent API   | `http://localhost:8082`  |
| RAG Uploader    | `http://localhost:8081`  |
| RAG Web UI      | `http://localhost:3000`  |
| Qdrant Dashboard| `http://localhost:6333`  |

---

## 🧠 Loading and Using Models

Pre-download your LLM models from Ollama and place them in your NAS share:

```bash
ollama pull llama3
ollama pull deepseek-coder:6.7b
# etc...
```

Verify they're mounted in the container at `/root/.ollama/models`.

---

## 📄 Document Ingestion Workflow

1. Drop any supported file (PDF, TXT, DOCX) into `./documents/`.
2. The **rag-ingestor** will automatically detect and embed it.
3. Embeddings are stored in **Qdrant** under the appropriate collection.
4. Queries made via the UI or API will include matching context.

---

## 🧠 RAG Agent Usage

Example query via `curl`:

```bash
curl -X POST http://localhost:8082/query   -H "Content-Type: application/json"   -d '{"query": "What is in the latest project report?"}'
```

Response will include relevant context from embedded documents and model-generated answer.

---

## 🌐 RAG UI

Access the full-featured web app:

```
http://localhost:3000
```

- Enter queries in natural language.
- Results are based on RAG context from uploaded documents.
- Under-the-hood, this talks to the `rag-agent`.

---

## 🛠 Development & Customization

- **Want to use a different embedding model?** Swap it out in `rag-ingestor`.
- **Need GPU acceleration?** Add GPU passthrough in Proxmox + enable CUDA inside Ollama.
- **Want user authentication?** Add middleware to `rag-agent` and/or `rag-ui`.

---

## 📊 Optional: Add Centralized Monitoring

We recommend:
- [Netdata](https://www.netdata.cloud/) or [Grafana + Prometheus](https://grafana.com) to monitor Docker + host performance
- Deploy a Netdata agent on each host and a central Netdata dashboard to observe everything from one interface

---

## 🔐 Security Notes

- Add a reverse proxy like **Traefik**, **Caddy**, or **Nginx** to:
  - Enforce HTTPS
  - Rate limit public endpoints
  - Protect with auth middleware

---

## 📌 Roadmap

- [ ] Add RAG file versioning and metadata tagging
- [ ] Live editing/view of document contents
- [ ] Secure user dashboard + history

---

## 🤝 Credits

- Built on: [Ollama](https://ollama.com), [Qdrant](https://qdrant.tech), [FastAPI](https://fastapi.tiangolo.com), [React](https://reactjs.org)
- Embedding via: [`nomic-embed-text-v1.5`](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5)

---

## 📜 License

This project is self-hosted, for internal use. Attribution to original open-source dependencies is preserved.
