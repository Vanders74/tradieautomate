"""Shared module: calls the local Ternary Bonsai 2 27B model via the PrismML llama.cpp fork server.

All 5 Bonsai-pattern workflows use this. The model runs locally on M2 Pro
at port 8080, $0/token.

Server start (PrismML fork, Metal):
    llama-server -m ~/models/bonsai/Ternary-Bonsai-2-27B-PQ2_0.gguf \
      -ngl 99 -fa on -c 65536 --host 127.0.0.1 --port 8080 \
      --temp 1.0 --top-p 0.95 --top-k 20

Usage:
    from .local_model import ask, system_prompt
    reply = ask(messages, temperature=0.1, max_tokens=1024)
"""

import json
import urllib.request
import urllib.error

SERVER_URL = "http://127.0.0.1:8080/v1/chat/completions"
MODEL = "Ternary-Bonsai-2-27B"  # name is arbitrary for llama.cpp server

def ask(messages, temperature=0.1, max_tokens=2048, timeout=120):
    """Send a chat request to the local Bonsai server. Returns the response text.

    messages: list of {"role": "system"|"user"|"assistant", "content": str}
    temperature: 0.1 = deterministic (structured tasks), 0.7 = creative
    max_tokens: max output tokens
    timeout: request timeout in seconds (Bonsai 27B is ~13 tok/s on M2 Pro)
    """
    body = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(
        SERVER_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = json.loads(resp.read().decode("utf-8"))
        msg = data["choices"][0]["message"]
        content = msg.get("content", "").strip()
        if not content:
            # Reasoning model: answer may land in reasoning_content.
            # Return it (may include chain-of-thought; acceptable for analysis workflows).
            content = msg.get("reasoning_content", "").strip()
        return content
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError) as e:
        return f"[MODEL ERROR: {e}]"


def system_prompt(text):
    return {"role": "system", "content": text}


def user_prompt(text):
    return {"role": "user", "content": text}


def assistant_prompt(text):
    return {"role": "assistant", "content": text}
