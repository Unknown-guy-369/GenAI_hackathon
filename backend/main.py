from fastapi import FastAPI
from routes import input_api
# classify_api, verify_api, summarize_api, healthcheck
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Misinformation AI Tool")

# Register routes

origins = [
    "http://localhost:5173",  # Example frontend origin
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allow specific methods
    allow_headers=["Content-Type", "Authorization"], # Allow specific headers
)

# Main route for only input
app.include_router(input_api.router, prefix="/c")

# Routes for seprate debugging to show specific testing
# app.include_router(classify_api.router, prefix="/classify")
# app.include_router(verify_api.router, prefix="/verify")
# app.include_router(summarize_api.router, prefix="/summarize")
# app.include_router(healthcheck.router, prefix="/health")

@app.get("/")
def root():
    return {"status": "running", "message": "Misinformation AI Tool backend is live"}
