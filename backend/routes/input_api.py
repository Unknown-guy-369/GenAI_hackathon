from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import json
import os
from tools.summarization import summarize_entailment_evidence
from tools.fact_verification import summarize_with_gemini,generate_search_query_gemini,retrieve_evidence_google_pse,verify_claim,fetch_page_text


router = APIRouter()

DATA_PATH = "./data/test.json"

# Ensure data directory and file exist
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_PATH):
    with open(DATA_PATH, "w") as f:
        json.dump([], f)  # start with empty list


class InputData(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None
    audio: Optional[str] = None


@router.post("/")
async def handle_input(data: InputData):
    # Detect input type
    if data.text:
        input_type = "text"
        content = data.text
    elif data.url:
        input_type = "url"
        content = data.url
    elif data.image:
        input_type = "image"
        content = data.image
    elif data.audio:
        input_type = "audio"
        content = data.audio
    else:
        return {"error": "No valid input provided"}

    # Load existing records
    with open(DATA_PATH, "r") as f:
        records = json.load(f)

    # Append new record
    # new_record = {
    #     "type": input_type,
    #     "content": content
    # }
    # records.append(new_record)  

    # # Save back to file
    # with open(DATA_PATH, "w") as f:
    #     json.dump(records, f, indent=4)

    # --- AI Pipeline for text input ---
    if input_type == "text":
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        GOOGLE_PSE_ID = os.getenv("GOOGLE_PSE_ID")

        try:
            search_query = generate_search_query_gemini(content, OPENROUTER_API_KEY)
            if len(search_query.split()) < 3:
                search_query = content
        except Exception:
            search_query = content

        evidence = retrieve_evidence_google_pse(search_query, GOOGLE_API_KEY, GOOGLE_PSE_ID)
        print("Retrieved Evidence:", evidence)
        if not evidence:
            return {
                "status": "saved",
                "input_type": input_type,
                "content": "hgff",
                "search_query": evidence,
                "error": "No evidence found."
            }

        results = verify_claim(content, evidence)
        print("Verification Results:", results) 
        summary = summarize_entailment_evidence(results)
        # for ev in results:
        #     page_text = fetch_page_text(ev["url"])
        #     if page_text:
        #         summary = summarize_with_gemini(page_text)
        #     else:
        #         summary = "Could not fetch content."
        #     summarized_evidence.append({
        #         "title": ev["title"],
        #         "url": ev["url"],
        #         "summary": summary
        #     })
            

        return {
            "status": "processed",
            "input_type": input_type,
            "claim": content,
            "search_query": search_query,
            "evidence": evidence,
            "results": results,
            "summarize": summary
        }

    # For other input types, just save and return status
    return {
        "status": "saved",
        "input_type": input_type,
        "content": content,
        "pipeline_status": "not processed (non-text input)"
    }
