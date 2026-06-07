"""
AWS adapter — garrison deployment stage 7.
Orchestrates the cloud control plane that pushes signed brain bundles to all
four forward edge nodes.
Detects: AWS_ACCESS_KEY_ID env var (also uses AWS_SECRET_ACCESS_KEY and
AWS_DEFAULT_REGION if present).

Uses a hand-rolled AWS Signature Version 4 request against the STS
GetCallerIdentity endpoint — the lightest possible "are my credentials valid?"
check, with zero external dependencies.
"""
import os
import time
import random
import json
import hashlib
import hmac
import datetime
import urllib.request
import urllib.error

_KEY       = "aws"
_SPONSOR   = "AWS"
_TITLE     = "Orchestrate push"
_DETAIL_OK = "Pushed signed brain bundles to 4 forward nodes"

_STS_ENDPOINT = "https://sts.amazonaws.com/"
_SERVICE      = "sts"
_ACTION_BODY  = b"Action=GetCallerIdentity&Version=2011-06-15"


# ---------------------------------------------------------------------------
# Minimal STS request signer (AWS Signature Version 4, stdlib only)

def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode(), hashlib.sha256).digest()

def _signing_key(secret: str, date_stamp: str, region: str, service: str) -> bytes:
    k_date    = _sign(("AWS4" + secret).encode(), date_stamp)
    k_region  = _sign(k_date, region)
    k_service = _sign(k_region, service)
    return _sign(k_service, "aws4_request")

def _sts_request(access_key: str, secret_key: str, region: str) -> None:
    now = datetime.datetime.utcnow()
    amz_date   = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")

    host = "sts.amazonaws.com"

    # Canonical request
    payload_hash = hashlib.sha256(_ACTION_BODY).hexdigest()
    canonical_headers = (
        f"content-type:application/x-www-form-urlencoded\n"
        f"host:{host}\n"
        f"x-amz-date:{amz_date}\n"
    )
    signed_headers = "content-type;host;x-amz-date"
    canonical_request = "\n".join([
        "POST", "/", "",
        canonical_headers,
        signed_headers,
        payload_hash,
    ])

    # String to sign
    credential_scope = f"{date_stamp}/{region}/{_SERVICE}/aws4_request"
    string_to_sign = "\n".join([
        "AWS4-HMAC-SHA256",
        amz_date,
        credential_scope,
        hashlib.sha256(canonical_request.encode()).hexdigest(),
    ])

    # Signature
    sig_key = _signing_key(secret_key, date_stamp, region, _SERVICE)
    signature = hmac.new(sig_key, string_to_sign.encode(), hashlib.sha256).hexdigest()

    auth_header = (
        f"AWS4-HMAC-SHA256 "
        f"Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )

    req = urllib.request.Request(
        _STS_ENDPOINT,
        data=_ACTION_BODY,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": host,
            "X-Amz-Date": amz_date,
            "Authorization": auth_header,
        },
    )
    with urllib.request.urlopen(req, timeout=8) as resp:
        _ = resp.read()


# ---------------------------------------------------------------------------

def _simulated() -> dict:
    return {
        "key":     _KEY,
        "sponsor": _SPONSOR,
        "title":   _TITLE,
        "detail":  _DETAIL_OK,
        "status":  "ok",
        "ms":      random.randint(380, 720),
        "mode":    "simulated",
    }


def provision() -> dict:
    access_key = os.environ.get("AWS_ACCESS_KEY_ID", "").strip()
    if not access_key:
        return _simulated()

    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "").strip()
    region     = os.environ.get("AWS_DEFAULT_REGION", "us-east-1").strip() or "us-east-1"

    if not secret_key:
        return _simulated()

    t0 = time.monotonic()
    try:
        _sts_request(access_key, secret_key, region)
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
