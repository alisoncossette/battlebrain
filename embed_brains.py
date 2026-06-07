#!/usr/bin/env python3
"""GARRISON STEP: build the semantic index for the brains.

Embeds every doctrine chunk with the on-device embedder and writes
brains_embedded.json (same shape as BRAINS, plus an `emb` vector per chunk).
The field server loads this and matches queries by cosine similarity offline.

Run once with comms up (Ollama reachable):  python embed_brains.py
"""
import json, copy
from pathlib import Path
from embedder import embed_document, EMBED_MODEL

ROOT = Path(__file__).parent

def main():
    # Reuse the server's resolved BRAINS (cache or inline). Importing server is
    # safe: its serve loop is guarded by __main__.
    from server import BRAINS
    brains = copy.deepcopy(BRAINS)

    total, ok = 0, 0
    for node, nb in brains.items():
        for ch in nb["chunks"]:
            total += 1
            v = embed_document(ch["text"])
            ch["emb"] = v
            if v:
                ok += 1
            print(f"  [{node}] {ch['id']}: {'OK dim=' + str(len(v)) if v else 'FAILED (embedder down?)'}")

    out = ROOT / "brains_embedded.json"
    out.write_text(json.dumps(brains, ensure_ascii=False), encoding="utf-8")
    print(f"\nembedded {ok}/{total} chunks with {EMBED_MODEL} -> {out.name}")
    if ok == 0:
        print("WARNING: no embeddings produced. Is `ollama pull nomic-embed-text` done and Ollama running?")

if __name__ == "__main__":
    main()
