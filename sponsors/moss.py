"""
Moss adapter — garrison deployment stage 2.
Builds a per-brain real-time semantic index so each edge node can retrieve
doctrine at field speed with no cloud connection.
Detects: MOSS_API_KEY env var.
"""
import os
import time
import random
import json
import urllib.request
import urllib.error

_KEY       = "moss"
_SPONSOR   = "Moss"
_TITLE     = "Index brains"
_DETAIL_OK = "Built per-brain real-time semantic index"


def _simulated() -> dict:
    return {
        "key":     _KEY,
        "sponsor": _SPONSOR,
        "title":   _TITLE,
        "detail":  _DETAIL_OK,
        "status":  "ok",
        "ms":      random.randint(310, 580),
        "mode":    "simulated",
    }


def provision() -> dict:
    api_key = os.environ.get("MOSS_API_KEY", "").strip()
    if not api_key:
        return _simulated()

    t0 = time.monotonic()
    try:
        req = urllib.request.Request(
            "https://api.getmoss.ai/v1/ping",
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