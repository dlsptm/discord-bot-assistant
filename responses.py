import json
from youtube import *
from news_api import *
import requests

MODEL = "llama3.2"

def call_ollama(prompt):
    response = requests.post(
        "http://bot_ollama:11434/api/generate",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "model": MODEL,
            "prompt": prompt,
            "options": {
                "num_ctx": 4096
            },
            "stream": False,
        })
    )
    return response.json()["response"]


def get_response(user_input: str, channel: str) -> str:
    lowered: str = user_input.strip().lower()

    if lowered.startswith("!ask ") or channel == 'chatbot':
        # Si la commande commence par "!ask ", on la retire
        lowered = lowered[5:] if lowered.startswith("!ask ") else lowered
        return call_ollama(lowered)
    elif lowered.startswith("!yt ") or channel == 'youtube':
        # Même logique pour les commandes YouTube
        lowered = lowered[4:] if lowered.startswith("!yt ") else lowered
        return fetch_youtube_videos(lowered)
    elif channel == 'news':
        return fetch_articles()
    elif lowered.startswith("hello"):
        return 'Hello there'
    return 'yes I am here'