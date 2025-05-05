import json
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