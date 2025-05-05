import os
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv('GOOGLE_TOKEN')

def fetch_youtube_videos(query, max_result=10):
    url = "https://www.googleapis.com/youtube/v3/search"

    now = datetime.now()
    last_year = now.year - 1
    month = f"{now.month:02d}"
    published_after = f"{last_year}-{month}-01T00:00:00Z"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_result,
        "publishedAfter": published_after,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []

    for item in data.get("items", []):
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        results.append(f"{title} - {video_url}")

    return "\n".join(results)

