"""
llm_client.py

Cliente que habla con un modelo real corriendo local vía Ollama.
Ollama expone una API HTTP en localhost:11434 - este es el mismo
patrón que usarías para llamar a cualquier API de LLM en la nube,
solo que acá es gratis y offline.
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"


def ask_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Envía el system_prompt + user_prompt al modelo corriendo en Ollama
    y devuelve la respuesta como texto.
    """
    full_prompt = f"{system_prompt}\n\nUsuario: {user_prompt}\n\nAsistente:"

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()
    return data.get("response", "").strip()