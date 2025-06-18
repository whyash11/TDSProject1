import json
import os
import requests
from dotenv import load_dotenv
from utils import search_discourse, extract_text_from_image

# Load environment variables
load_dotenv()
AIPIPE_TOKEN = os.getenv("AIPIPE_TOKEN")  # Ensure your .env file has this key

# Load discourse posts into memory
with open("data/discourse.json", encoding="utf-8") as f:
    discourse = json.load(f)

def answer_question(question, image=None):
    # Add OCR'd image text if image is provided
    if image:
        question += "\n\n" + extract_text_from_image(image)

    # Search matching discourse posts
    matches = search_discourse(question, discourse)

    # Prepare context from top 3 matches
    context = "\n\n".join([m['content'] for m in matches[:3]])
    prompt = f"""You're a virtual TA. Based on the following forum posts:\n{context}\n\nAnswer this:\n{question}"""

    # OpenAI-style message format
    messages = [
        {"role": "system", "content": "You are a helpful virtual TA for the Tools in Data Science course."},
        {"role": "user", "content": prompt}
    ]

    # Call AI Pipe endpoint
    try:
        response = requests.post(
            url="https://aipipe.org/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {AIPIPE_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",  # Adjust based on what AI Pipe supports
                "messages": messages
            },
            timeout=30  # Optional timeout for stability
        )

        response.raise_for_status()  # Raises HTTPError for bad status
        result = response.json()

        answer = result["choices"][0]["message"]["content"]
        links = [{"url": m["url"], "text": m["title"]} for m in matches[:3]]

        return {"answer": answer, "links": links}

    except requests.exceptions.RequestException as e:
        return {"answer": f"Error reaching AI Pipe API: {str(e)}", "links": []}
