import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from tqdm import tqdm
import json

# Your session cookie (_t value only, not the full cookie header)
DISCOURSE_COOKIE = "eEZsgC1wYBDsC8iCbbmh5Te0CTc0O15xBnUeddZkHSMrefNVWfVKh%2Bc4Qi8GcoRsEYmV2uIFCkQa6p6D2ZHExT6L93s7E8t13rwm4e6sNj%2FH%2FCtg0DX%2BPS5Mh%2FFdXt6%2FDeb1q%2BCSqxjp2bjLgDV47wmRXOJvNxtUxlzZl4E4iI%2FA%2F1jxOUKXU38PStSYsarjRRLQKINCqex8ylijlzoYqGyME%2FJX3sjpGnVF37m5NaU64uGupl%2FJmriCAghPvZsXuGUtRBKWVtWI0F%2FHGD1eh4ZKAj%2F5tyKNkstd6XQSFrL9EXueHY1%2BPGUhMLw%3D--HBEZ%2FhVeGgh7c3Yd--yAyqlGMHiwiJgVAZ3ywKAg%3D%3D"


session = requests.Session()
session.cookies.set("_t", DISCOURSE_COOKIE, domain="discourse.onlinedegree.iitm.ac.in")
session.headers.update({"User-Agent": "Mozilla/5.0"})

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"

def get_topic_ids(category_slug="courses/tds-kb", category_id=34):
    topics = []
    for page in tqdm(range(0, 20)):  # Adjust if you want more pages
        url = f"{BASE_URL}/c/{category_slug}/{category_id}.json?page={page}"
        r = session.get(url)
        if r.status_code != 200:
            break
        data = r.json()
        new_topics = data["topic_list"]["topics"]
        if not new_topics:
            break
        topics.extend(new_topics)
    return topics

def get_posts_in_topic(topic_id):
    r = session.get(f"{BASE_URL}/t/{topic_id}.json")
    if r.status_code != 200:
        return []
    data = r.json()
    return [
        {
            "username": post["username"],
            "created_at": post["created_at"],
            "content": BeautifulSoup(post["cooked"], "html.parser").get_text(),
            "post_url": f"{BASE_URL}/t/{topic_id}/{post['post_number']}"
        }
        for post in data["post_stream"]["posts"]
    ]

all_posts = []
topics = get_topic_ids()

for topic in tqdm(topics):
    # Parse created_at as timezone-aware datetime (UTC)
    created_at = datetime.fromisoformat(topic["created_at"].replace("Z", "+00:00"))
    # Compare with a timezone-aware datetime for Jan 1, 2025 UTC
    if created_at >= datetime(2025, 1, 1, tzinfo=timezone.utc) and created_at <= datetime(2025, 4, 15, tzinfo=timezone.utc):
        posts = get_posts_in_topic(topic["id"])
        all_posts.extend(posts)

# Save the scraped posts into a JSON file
with open("tds_discourse_posts.json", "w", encoding="utf-8") as f:
    json.dump(all_posts, f, indent=2, ensure_ascii=False)

print(f"Scraped {len(all_posts)} posts.")
