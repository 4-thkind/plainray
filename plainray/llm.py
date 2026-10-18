"""Minimal, dependency-free client for a local Ollama server.

PlainRay runs its model OFFLINE on the clinic's own machine via Ollama
(http://127.0.0.1:11434). No report text ever leaves the device.

If your org already runs its own inference server, point OLLAMA_HOST at it:
    set OLLAMA_HOST=http://gpu-box.internal:11434
Everything else is unchanged - the model name, prompt and privacy model stay local.
"""

import json
import os
import urllib.request, urllib.error

__all__ = ["chat", "DEFAULT_MODEL"]

DEFAULT_MODEL = os.environ.get("PLAINRAY_MODEL", "gemma3:4b")


def _host() -> str:
    return os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")


def chat(messages, model: str | None = None, temperature: float = 0.35, num_ctx: int = 4096) -> str:
    """Send a chat request to the local Ollama server and return the reply text."""
    payload = json.dumps({
        "model": model or DEFAULT_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature, "num_ctx": num_ctx},
    }).encode()

    req = urllib.request.Request(
        f"{_host()}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Could not reach the local Ollama server. Is it running? "
            "Start it with: ollama serve"
        ) from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("Ollama returned a malformed response.") from exc

    return (data.get("message") or {}).get("content", "").strip()


def extract_json(text: str) -> dict:
    """Pull the first balanced JSON object out of a model reply."""
    marker = text.find("{")
    if marker < 0:
        raise ValueError("model reply contained no JSON object")
    depth = 0
    for i in range(marker, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[marker:i + 1])
    raise ValueError("model reply contained an unbalanced JSON object")
