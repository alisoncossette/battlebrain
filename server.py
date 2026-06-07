#!/usr/bin/env python3
"""
EDGE BRAIN MESH - field knowledge server
Runs 100% locally. No internet required at demo time.

Each "node" (tank, medic device, command post, restricted) holds its own BRAIN:
a small corpus of real, public U.S. Army field-manual excerpts. A soldier pairs
locally (simulated Bluetooth/mesh) and queries the nearest node's brain by voice.

If Ollama (with a Qwen model) is running on localhost:11434 the answer is phrased
by an ON-DEVICE model. Otherwise the server returns the retrieved passage directly
-- so the demo works fully air-gapped with zero dependencies.
"""
import json, re, urllib.request, http.server, socketserver
from pathlib import Path

PORT = 8000
ROOT = Path(__file__).parent
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"  # on-device Qwen brain (optional)

# ---------------------------------------------------------------------------
# CLEARANCE LEVELS  (higher = more access)
CLEAR = {"UNCLAS": 0, "CUI": 1, "SECRET": 2}

# WHO is in the field. Each profile -> role, MOS, clearance.
IDENTITIES = {
    "rifleman": {"label": "PVT Reyes - 11B Infantry",  "clearance": "UNCLAS"},
    "medic":    {"label": "SGT Okafor - 68W Combat Medic", "clearance": "CUI"},
    "mechanic": {"label": "SPC Hahn - 91B Wheeled Mechanic", "clearance": "CUI"},
    "officer":  {"label": "CPT Vance - Cleared / S2", "clearance": "SECRET"},
    "pilot":    {"label": "CW2 Lang - DOWNED AVIATOR (151A)", "clearance": "CUI"},
}

# ---------------------------------------------------------------------------
# THE BRAINS. One corpus per node. Each chunk is written as spoken, step-by-step
# field guidance with a real source citation. Content is public doctrine.
BRAINS = {
    "medic": {
        "name": "COMBAT CASUALTY CARE BRAIN",
        "device": "Medic comms device / air-gapped Pixel",
        "icon": "⚕️",
        "min_clearance": "UNCLAS",     # everyone may pair...
        "full_clearance": "CUI",       # ...but full depth needs medic-tier
        "chunks": [
            {"id":"m1","src":"TCCC Guidelines / TC 4-02.1, MARCH",
             "kw":"bleeding hemorrhage blood arterial tourniquet limb leg arm wound massive",
             "tier":"basic",
             "text":"Massive hemorrhage. Apply a CoTCCC tourniquet high and tight on the limb, over the uniform, two to three inches above the wound. Tighten until bright red bleeding stops and the distal pulse is gone. Mark the time on the tourniquet. Do not loosen it."},
            {"id":"m2","src":"TCCC Guidelines / TC 4-02.1, MARCH",
             "kw":"airway breathing choke unconscious nasal chest seal sucking",
             "tier":"basic",
             "text":"Airway. If unconscious, open the airway with a chin lift or insert a nasopharyngeal airway and place the casualty in the recovery position. Breathing. For a penetrating chest wound, apply a vented chest seal and monitor for tension pneumothorax."},
            {"id":"m3","src":"ATP 4-25.13, 9-Line MEDEVAC",
             "kw":"medevac evacuate evacuation nine line casualty pickup helicopter",
             "tier":"basic",
             "text":"To request evacuation, transmit the nine line MEDEVAC: Line 1 location, Line 2 your callsign and frequency, Line 3 number of patients by precedence, Line 4 special equipment, Line 5 patients by type litter or ambulatory, Line 6 security at pickup site, Line 7 method of marking, Line 8 patient nationality, Line 9 terrain or CBRN contamination."},
            {"id":"m4","src":"TCCC Guidelines, Circulation / TXA",
             "kw":"shock tranexamic txa fluid hypothermia circulation pale cold",
             "tier":"advanced",
             "text":"Circulation. If the casualty is in hemorrhagic shock, establish IV or IO access and give tranexamic acid as soon as possible, ideally within one hour, but not after three hours from injury. Prevent hypothermia: remove wet gear and wrap the casualty in a warming blanket."},
        ],
    },
    "tank": {
        "name": "EQUIPMENT & WEAPONS REPAIR BRAIN",
        "device": "On-platform compute (vehicle / weapon system)",
        "icon": "\U0001f527",
        "min_clearance": "UNCLAS",
        "full_clearance": "CUI",
        "chunks": [
            {"id":"t1","src":"TC 3-22.9, Immediate Action (SPORTS)",
             "kw":"weapon jam stoppage stovepipe rifle m4 wont fire feed misfire malfunction",
             "tier":"basic",
             "text":"Weapon stoppage. Perform immediate action - SPORTS. Slap the bottom of the magazine to seat it. Pull the charging handle to the rear. Observe for an ejected round and chamber. Release the charging handle to chamber a fresh round. Tap the forward assist. Squeeze the trigger to fire."},
            {"id":"t2","src":"TM 9-1005-313, M240 Stoppage",
             "kw":"m240 machine gun belt feed runaway stoppage tray cover crew served",
             "tier":"advanced",
             "text":"M240 stoppage. Pull and lock the charging handle to the rear and place the weapon on safe. Open the feed tray cover and inspect for a ruptured cartridge or a broken link. Clear the chamber, reload a fresh belt, close the cover, and resume firing. For a runaway gun, break the belt to stop feeding."},
            {"id":"t3","src":"TM 9-2320, PMCS",
             "kw":"vehicle engine wont start battery pmcs maintenance fuel hmmwv truck",
             "tier":"basic",
             "text":"Vehicle no-start. Run before-operation PMCS. Check the battery connections are tight and not corroded, confirm the fuel shutoff is open and there is fuel, and verify the master switch is on. If the engine cranks but will not start, prime the fuel system and bleed air from the fuel filter."},
        ],
    },
    "command": {
        "name": "POLICY, ROE & REPORTING BRAIN",
        "device": "Command post node / leader's device",
        "icon": "\U0001f4cb",
        "min_clearance": "UNCLAS",
        "full_clearance": "UNCLAS",
        "chunks": [
            {"id":"c1","src":"GTA 21-08, SALUTE Report",
             "kw":"report enemy spot contact salute observe sighting",
             "tier":"basic",
             "text":"Report enemy activity with SALUTE: Size of the element, Activity they are doing, Location grid, Unit or uniform identification, Time observed, and Equipment they carry. Send it to higher immediately."},
            {"id":"c2","src":"Standing ROE / EOF",
             "kw":"roe rules engagement fire escalation force hostile shoot permission",
             "tier":"basic",
             "text":"Rules of engagement. You always retain the right of self defense against a hostile act or demonstrated hostile intent. Escalation of force: shout a warning, show your weapon, shove or use a physical barrier, then fire only as a last resort and only proportionally. Positively identify the target before engaging."},
            {"id":"c3","src":"ATP 6-01.1, SITREP",
             "kw":"sitrep situation update status higher net report routine",
             "tier":"basic",
             "text":"Situation report. Transmit your callsign, current location, enemy situation, your unit status and combat effectiveness, and any logistics or medical needs. Keep it brief and end with any request for guidance."},
        ],
    },
    "restricted": {
        "name": "CBRN & CONTROLLED CRYPTO BRAIN",
        "device": "Hardened node - clearance gated",
        "icon": "\U0001f512",
        "min_clearance": "SECRET",   # <-- must hold SECRET even to PAIR
        "full_clearance": "SECRET",
        "chunks": [
            {"id":"r1","src":"ATP 3-11.32, CBRN Reaction",
             "kw":"gas chemical cbrn mask attack nerve agent contamination decon",
             "tier":"advanced",
             "text":"CBRN attack. Stop breathing, don and clear your protective mask within nine seconds, give the alarm by shouting Gas Gas Gas, and assume MOPP 4. Begin immediate decontamination of exposed skin with the decon kit and report the attack to higher."},
            {"id":"r2","src":"Controlled - COMSEC handling",
             "kw":"crypto comsec key fill load radio secure sincgars frequency hopping",
             "tier":"advanced",
             "text":"COMSEC. Load the cryptographic key into the radio with the fill device, verify the key with the receiving station, and zeroize the device if capture is imminent. Handle and store keying material per controlled cryptographic item procedures."},
        ],
    },
}

# ---------------------------------------------------------------------------
# GARRISON-PROVISIONED CACHE. The comms-up build (`python ingest.py`) runs the
# REAL Unsiloed parse + Moss index over corpus/*.pdf and writes brains_cache.json.
# Downrange (comms-down) the server reads that cache offline. Falls back to the
# inline BRAINS above if no cache exists, so the demo always works.
try:
    from config import load_env
    load_env()
except Exception:
    pass
try:
    _cache = ROOT / "brains_cache.json"
    if _cache.exists():
        BRAINS = json.loads(_cache.read_text(encoding="utf-8"))
        print(f"[brains] loaded garrison-provisioned cache: {list(BRAINS.keys())}")
except Exception as _e:
    print(f"[brains] using inline doctrine (no cache): {_e}")

# ---------------------------------------------------------------------------
def authorize(node_id, identity_id):
    """Return (can_pair, full_access, reason)."""
    node = BRAINS[node_id]
    me = CLEAR[IDENTITIES[identity_id]["clearance"]]
    need_pair = CLEAR[node["min_clearance"]]
    need_full = CLEAR[node["full_clearance"]]
    if me < need_pair:
        return (False, False,
                f"ACCESS DENIED - {node['min_clearance']} clearance required to pair. "
                f"You hold {IDENTITIES[identity_id]['clearance']}. Need-to-know not established.")
    return (True, me >= need_full, "PAIRED")

def retrieve(node_id, query, full_access):
    """Keyword-score the node's chunks; return best chunk respecting tier."""
    q = set(re.findall(r"[a-z0-9]+", query.lower()))
    best, score = None, 0
    for ch in BRAINS[node_id]["chunks"]:
        if ch["tier"] == "advanced" and not full_access:
            continue
        s = len(q & set(ch["kw"].split()))
        if s > score:
            best, score = ch, s
    if best is None:  # fall back to first allowed chunk
        for ch in BRAINS[node_id]["chunks"]:
            if ch["tier"] == "basic" or full_access:
                best = ch; break
    return best

def phrase_with_ollama(node_name, passage, query):
    """Optional: let an on-device Qwen model phrase the answer. Returns None if unavailable."""
    prompt = (f"You are {node_name}, an offline field-knowledge assistant. "
              f"Answer the soldier's question using ONLY the doctrine passage below. "
              f"Be concise and give clear spoken steps. Do not invent anything.\n\n"
              f"PASSAGE: {passage}\n\nQUESTION: {query}\n\nANSWER:")
    body = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False,
                       "keep_alive": "30m"}).encode()
    try:
        req = urllib.request.Request(OLLAMA_URL, data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read())["response"].strip()
    except Exception:
        return None

# ---------------------------------------------------------------------------
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)

    def log_message(self, *a):  # quiet
        pass

    def do_POST(self):
        if self.path != "/api/ask":
            self.send_error(404); return
        n = int(self.headers.get("Content-Length", 0))
        req = json.loads(self.rfile.read(n) or "{}")
        node_id = req.get("node"); ident = req.get("identity"); query = req.get("query", "")

        can_pair, full, reason = authorize(node_id, ident)
        if not can_pair:
            return self._json({"allowed": False, "reason": reason,
                               "audit": f"DENIED  {IDENTITIES[ident]['label']}  ->  {BRAINS[node_id]['name']}"})

        ch = retrieve(node_id, query, full)
        spoken = phrase_with_ollama(BRAINS[node_id]["name"], ch["text"], query)
        engine = "qwen-on-device" if spoken else "local-retrieval"
        answer = spoken or ch["text"]
        depth = "FULL" if full else "BASIC (buddy-aid tier)"
        self._json({
            "allowed": True, "answer": answer, "citation": ch["src"],
            "depth": depth, "engine": engine,
            "audit": f"SERVED  {IDENTITIES[ident]['label']}  ->  {BRAINS[node_id]['name']}  [{ch['src']}]",
        })

    def _json(self, obj):
        b = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/api/deploy":
            try:
                from deploy import run_deployment
                return self._json(run_deployment())
            except Exception as e:
                # Frontend has its own fallback, but return a usable shape anyway.
                return self._json({"stages": [], "nodes": list(BRAINS.keys()), "error": str(e)})
        if self.path == "/api/config":
            cfg = {"identities": IDENTITIES,
                   "nodes": {k: {"name": v["name"], "device": v["device"], "icon": v["icon"],
                                 "min_clearance": v["min_clearance"]} for k, v in BRAINS.items()}}
            return self._json(cfg)
        return super().do_GET()

if __name__ == "__main__":
    print(f"EDGE BRAIN MESH running -> http://localhost:{PORT}")
    print("Open that URL in Chrome.  Comms can be physically OFF; this is all local.")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
