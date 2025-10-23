# Inference of GPT-Sovits via api_v2.py

from httpx import Response
import requests

GPT_SOVITS_API_URL = "http://127.0.0.1:9880"

def get_tts_response(text: str) -> str:
    response = requests.get(f"{GPT_SOVITS_API_URL}/tts", params={"text": text})
    if(response.status_code == 200):
        # wav stream
        return response.content
    else:
        error = response.json()
        print(f"Error: {error}")
        return None