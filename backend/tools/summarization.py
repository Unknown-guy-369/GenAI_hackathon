import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
def fetch_page_text(url):
    """
    Fetches and extracts main text from a web page.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        tags = soup.find_all(["p","figcaption","h1","h2","h3","h4","h5","h6","li","span","a","td","th"])
        text = " ".join([tag.get_text(strip=True) for tag in tags])
        print("extracted {len(text)} characters from: {url}")
        return text.strip()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def summarize_with_gemini(text) ->str:
    print("Added")
    """
    Summarizes the given text using Gemini Flash via OpenRouter API.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemini-flash-1.5",
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant that summarizes web page content to answer a user claim."
            },
            {
                "role": "user",
                "content": f"Summarize the following evidence to answer the claim:\n{text}"
            }
        ],
        "max_tokens": 256
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    print("Added")
    summary = result["choices"][0]["message"]["content"].strip()
    print(summary)
    return summary

def summarize_entailment_evidence(evidence_list):
    # Filter only entailment evidence
    entailment_links = [ev["url"] for ev in evidence_list if ev.get("prediction") == "entailment"]
    if not entailment_links:
        return "No entailment evidence found."
    # Fetch and concatenate text
    all_text = ""
    for url in entailment_links:
        page_text = fetch_page_text(url)
        if page_text:
            all_text += page_text + "\n\n"
    if not all_text.strip():
        return "Could not fetch text from entailment evidence."
    # Summarize
    summary = summarize_with_gemini(all_text)
    return summary

if __name__ == "__main__":
    evidence_list = [
        {
            "evidence": "2025 Nepalese Gen Z protests - Wikipedia",
            "url": "https://en.wikipedia.org/wiki/2025_Nepalese_Gen_Z_protests",
            "prediction": "neutral",
            "confidence": 0.43581676483154297
        },
        {
            "evidence": "Photos: Nepal's “Gen Z” Protests - The Atlantic",
            "url": "https://www.theatlantic.com/photography/archive/2025/09/photos-nepal-gen-z-protest/684168/",
            "prediction": "entailment",
            "confidence": 0.5902116894721985
        },
        {
            "evidence": "Nepal Gen-Z protests: Politicians get rich while we suffer - so I ...",
            "url": "https://www.bbc.com/news/articles/cvg9n760gddo",
            "prediction": "contradiction",
            "confidence": 0.6298782229423523
        }
    ]
    summary = summarize_entailment_evidence(evidence_list)
    print("\nFinal Entailment Summary:\n", summary)