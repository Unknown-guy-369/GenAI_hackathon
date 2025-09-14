from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import json
import os

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
def handle_input(data: InputData):
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
    new_record = {
        "type": input_type,
        "content": content
    }
    records.append(new_record)

    # Save back to file
    with open(DATA_PATH, "w") as f:
        json.dump(records, f, indent=4)

    return {
        "status": "saved",
        "input_type": input_type,
        "content": content,
        "pipeline_status": "processing pipeline..."
    }
