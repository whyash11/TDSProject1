import json
import os
import requests
from dotenv import load_dotenv
from utils import search_discourse, extract_text_from_image

# Load environment variables
load_dotenv()
AIPIPE_TOKEN = os.getenv("AIPIPE_TOKEN")  # Save your AI Pipe token here

# Load discourse posts
with open("data/discourse.json", encoding="utf-8") as f:
    discourse = json.load(f)

def answer_question(question, image=None):
    if image:
        question += "\n\n" + extract_text_from_image(image)

    matches = search_discourse(question, discourse)

    # Prepare context from top 3 matches
    context = "\n\n".join([m['content'] for m in matches[:3]])
    prompt = f"""You're a virtual TA. Based on the following forum posts:\n{context}\n\nAnswer this:\n{question}"""

    # Prepare messages in OpenAI-style format
    messages = [
        {"role": "system", "content": "You are a helpful virtual TA for the Tools in Data Science course."},
        {"role": "user", "content": prompt}
    ]

    # Call AI Pipe's OpenAI-compatible chat endpoint
    response = requests.post(
        url="https://aipipe.org/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {AIPIPE_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",  # or "gpt-3.5-turbo", depending on AI Pipe support
            "messages": messages
        }
    )

    if response.status_code != 200:
        raise Exception(f"AI Pipe API error: {response.status_code} - {response.text}")

    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    links = [{"url": m["url"], "text": m["title"]} for m in matches[:3]]

    return {"answer": answer, "links": links}
