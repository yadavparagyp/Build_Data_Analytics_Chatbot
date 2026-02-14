from __future__ import annotations
import requests
from typing import List, Dict, Any
from .config import SETTINGS

class OllamaClient:
    def __init__(self, base_url: str = SETTINGS.ollama_base_url, model: str = SETTINGS.ollama_model):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        url = f"{self.base_url}/api/chat"
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "options": {
                "temperature": temperature,
                "num_predict": 1200 
            },
            "stream": False
        }
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["message"]["content"]
