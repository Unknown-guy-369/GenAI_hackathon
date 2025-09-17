from transformers import pipeline
import requests  # For making API calls
import spacy
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


# --- Step 1: Source Retrieval (Google PSE API) ---
def retrieve_evidence_google_pse(query, api_key, pse_id, max_results=3):
    """
    Retrieve evidence snippets from Google's Programmable Search Engine API.
    Returns a list of dicts with 'title' and 'url'.
    """
    url = (
        f"https://www.googleapis.com/customsearch/v1?"
        f"key={api_key}&"
        f"cx={pse_id}&"
        f"q={query}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        search_results = response.json().get('items', [])
        print(f"Found {len(search_results)} results from Google PSE.")
        evidence = []
        for item in search_results[:max_results]:
            evidence.append({
                "title": item.get("title", ""),
                "url": item.get("link", "")
            })
        return evidence
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Google PSE API: {e}")
        return []

def extract_search_query(claim):
    """
    Extracts main entity (named entities + proper nouns) and action/context from claim.
    Includes both verb and noun forms for better search accuracy.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(claim)
    entities = [ent.text for ent in doc.ents]
    propn = [token.text for token in doc if token.pos_ == "PROPN"]

    # Collect both verb and noun forms if present
    verbs = [token.text for token in doc if token.pos_ == "VERB" and not token.is_stop]
    nouns = [token.text for token in doc if token.pos_ == "NOUN" and not token.is_stop]
    lemmas = [token.lemma_ for token in doc if token.pos_ in ("VERB", "NOUN") and not token.is_stop]

    # Combine all relevant terms
    search_terms = entities + propn + verbs + nouns + lemmas

    # Remove duplicates while preserving order
    seen = set()
    search_terms = [x for x in search_terms if not (x in seen or seen.add(x))]
    return " ".join(search_terms)

# --- Step 2: Claim-Evidence Consistency Checking ---
def verify_claim(claim, evidence_list):
    """
    Use a pre-trained NLI model to check claim consistency against evidence.
    Accepts evidence_list as list of strings or dicts with 'title'/'url'.
    """
    nli_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    candidate_labels = ["entailment", "neutral", "contradiction"]
    results = []
    print("\n🧐 Checking claim against retrieved evidence...")
    for evidence in evidence_list:
        evidence_text = evidence["title"] if isinstance(evidence, dict) else evidence
        result = nli_classifier(
            evidence_text,
            candidate_labels,
            hypothesis_template=f"This text means that {claim}:{{}}"
        )
        results.append({
            "evidence": evidence_text,
            "url": evidence["url"] if isinstance(evidence, dict) else None,
            "prediction": result['labels'][0],
            "confidence": result['scores'][0]
        })
    return results

 

def generate_search_query_gemini(claim, openrouter_api_key):
    """
    Uses Gemini Flash via OpenRouter API to generate a search query from the claim.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemini-flash-1.5",
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant that generates concise and effective Google search queries from user claims."
            },
            {
                "role": "user",
                "content": claim
            }
        ],
        "max_tokens": 32
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    # Extract the generated search query
    search_query = result["choices"][0]["message"]["content"].strip()
    return search_query

# --- Example Usage ---
if __name__ == "__main__":
    # --- IMPORTANT: Replace with your actual keys ---
    GOOGLE_API_KEY =  os.getenv("GOOGLE_API_KEY")
    GOOGLE_PSE_ID = os.getenv("GOOGLE_PSE_ID")  # Replace with your PSE ID
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Replace with your OpenRouter API key

    user_claim = "does ttf vasan got married"
    search_query = generate_search_query_gemini(user_claim, OPENROUTER_API_KEY)
    print(f"Generated Search Query (Gemini): {search_query}")

    # If the extracted query is too short, fallback to the full claim
    if len(search_query.split()) < 3:
        search_query = user_claim

    print(f"Generated Search Query: {search_query}")

    evidence_snippets = retrieve_evidence_google_pse(search_query, GOOGLE_API_KEY, GOOGLE_PSE_ID)

    if evidence_snippets:
        verification_results = verify_claim(user_claim, evidence_snippets)
        print(verification_results)
        print(evidence_snippets)
        print("\n--- Verification Results ---")
        for res in verification_results:
            print(f"Evidence: \"{res['evidence']}\"")
            if res["url"]:
                print(f"URL: {res['url']}")
            print(f"Conclusion: {res['prediction'].upper()} (Confidence: {res['confidence']:.2f})")
            print("-" * 10)
    else:
        print("No evidence retrieved to verify the claim.")



