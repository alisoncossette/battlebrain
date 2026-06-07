"""On-device embeddings via Ollama (nomic-embed-text). Stdlib only.

Used in two places that mirror the two-phase architecture:
  - GARRISON (embed_brains.py): embed each doctrine chunk -> the semantic index.
  - FIELD (server.py): embed the spoken query, cosine-match against the index,
    and FAIL CLOSED if the best match is below threshold.

nomic-embed-text works best with task prefixes, so documents and queries are
embedded asymmetrically ("search_document:" vs "search_query:").
"""
import json, math, urllib.request

OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "nomic-embed-text"

def _embed(text, timeout=30):
    body = json.dumps({"model": EMBED_MODEL, "input": text}).encode()
    try:
        req = urllib.request.Request(OLLAMA_EMBED_URL, data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read())
        embs = data.get("embeddings")
        if embs and isinstance(embs, list):
            return embs[0]
        return data.get("embedding")  # older shape
    except Exception:
        return None

def embed_document(text, timeout=30):
    return _embed("search_document: " + text, timeout)

def embed_query(text, timeout=30):
    return _embed("search_query: " + text, timeout)

def cosine(a, b):
    if not a or not b or len(a) != len(b):
        return -1.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return -1.0
    return dot / (na * nb)
