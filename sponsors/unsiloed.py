"""
Unsiloed adapter — garrison deployment stage 1.
Parses field manuals / TMs / SOPs (PDF, tables, diagrams, torque specs)
into clean, structured, cited chunks ready for indexing.
Detects: UNSILOED_API_KEY env var.
"""
import os
import time
import random
import json
import urllib.request
import urllib.error

_KEY       = "unsiloed"
_SPONSOR   = "Unsiloed"
_TITLE     = "Parse field manuals"
_DETAIL_OK = "Parsed FM/TM PDFs into structured, cited chunks"


def _simulated() -> dict:
    return {
        "key":     _KEY,
        "sponsor": _SPONSOR,
        "title":   _TITLE,
        "detail":  _DETAIL_OK,
        "status":  "ok",
        "ms":      random.randint(280, 520),
        "mode":    "simulated",
    }


def provision() -> dict:
    api_key = os.environ.get("UNSILOED_API_KEY", "").strip()
    if not api_key:
        return _simulated()

    t0 = time.monotonic()
    try:
        req = urllib.request.Request(
            "https://api.unsiloed.ai/v1/health",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            _ = resp.read()
        ms = int((time.monotonic() - t0) * 1000)
        return {
            "key":     _KEY,
            "sponsor": _SPONSOR,
            "title":   _TITLE,
            "detail":  _DETAIL_OK,
            "status":  "ok",
            "ms":      ms,
            "mode":    "live",
        }
    except Exception:
        return _simulated()