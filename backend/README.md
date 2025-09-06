# Backend

This folder contains the core AI + API implementation.  
We use **FastAPI** for REST endpoints, and this is where all the ML models, services, and routes live.

### Structure
- `main.py` → FastAPI entry point
- `routes/` → API endpoints grouped by features
- `models/` → AI/NLP models (classifier, NLI, summarizer, embeddings)
- `utils/` → Helper modules (preprocessing, retrieval, logging, policy checks)
- `services/` → Business logic connecting routes and models

