# EDGE BRAIN MESH

**One line:** Voice-first, comms-denied field-knowledge — AI brains pre-loaded onto forward edge compute in garrison, operated locally by soldiers in the field with zero internet.

> **Thesis:** Provision in garrison with the full cloud stack. Operate at the edge with none of it.

---

## The Problem

Voice models are cheap, fast, and good. That is not the bottleneck.

In a **DDIL (Denied, Degraded, Intermittent, Limited)** environment — a forward patrol, a contested urban block, a medic device with the radio jammed — the bottleneck is **getting authoritative knowledge to the right person, with the right clearance, when the link is dead.** Cloud RAG dies the moment the connection drops. A soldier asking about tourniquet placement or a weapon stoppage cannot wait for a signal.

The problem is not voice. The problem is **retrieval at the edge**.

---

## The Idea

Knowledge is pre-positioned onto whatever compute is already forward:

- The **tank / weapon system** carries its own **repair brain** (TMs live on its platform compute).
- The **medic's air-gapped Pixel** carries the **TCCC brain**.
- The **command post node** carries the **policy / ROE / reporting brain**.
- A **hardened node** carries the **CBRN / crypto brain**, locked to clearance.

Anything with compute holds a brain and can be reached. A soldier **pairs locally** (Bluetooth / mesh — no internet) with the nearest node and **talks to its brain by voice**. Who can pair with what, and at what depth, is the access-control layer.

---

## Architecture: Two Phases

### Phase 1 — Deployment / Garrison (comms UP)

This is the load-out. The full sponsor stack runs **once, in garrison, while comms are available**, to build and push all brains onto every edge node. Loss of comms later is survivable because everything needed is already there.

```
GARRISON (comms UP)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  FMs / TMs / SOPs (PDF, tables, torque specs)                   │
│         │                                                       │
│         ▼                                                       │
│  [Unsiloed] Parse & chunk ──► [Moss] Semantic index             │
│                                      │                          │
│                                      ▼                          │
│                             [Minimax] Validate / synthesize     │
│                                      │                          │
│                                      ▼                          │
│                          [TrueFoundry] Govern → assign brain    │
│                            to node, enforce need-to-know policy │
│                                      │                          │
│                             [Qwen] Voice packs +                │
│                             on-device reasoning model           │
│                                      │                          │
│                             [AWS] Sign + bundle brains          │
│                                      │                          │
│                          [LiveKit] Push bundles live to nodes   │
│                                      │                          │
│               ┌──────────┬───────────┴──────────┬──────────┐   │
│               ▼          ▼                      ▼          ▼   │
│          MEDIC       TANK / WPN            COMMAND    HARDENED  │
│           NODE         NODE                  NODE       NODE    │
└─────────────────────────────────────────────────────────────────┘
```

| Step | What happens | Sponsor |
|---|---|---|
| Ingest | Parse FMs, TMs, SOPs (PDF, tables, diagrams, torque specs) into clean semantic chunks | **Unsiloed** |
| Index | Build a real-time semantic search index per brain | **Moss** |
| Govern | Assign each brain to its node; encode per-identity need-to-know policy + audit trail | **TrueFoundry** |
| Voice + Reason | Generate per-node voice packs; embed the on-device reasoning model | **Qwen** |
| Validate | Heavy synthesis and cross-reference validation at provisioning time | **Minimax** |
| Transport | Live update channel — push signed bundles to each node while link is up | **LiveKit** |
| Orchestrate | Cloud control plane packages and dispatches signed brain bundles | **AWS** |

---

### Phase 2 — Field / Mission (comms DOWN)

From this point forward, **zero internet**. Every node operates autonomously.

```
FIELD (comms DOWN — zero internet)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Soldier ──[voice / push-to-talk]──► nearest node              │
│                │                         │                      │
│                │  Bluetooth / mesh pair   │                      │
│                │  (no internet)           │                      │
│                ▼                         ▼                      │
│        Identity check            Clearance gate                 │
│         (who are you?)         (what can you see?)              │
│                                          │                      │
│                              ┌───────────┴──────────┐          │
│                              │                      │          │
│                          ALLOWED               DENIED           │
│                              │             (audit logged)       │
│                              ▼                                  │
│                    On-node brain retrieval                      │
│                    (keyword-scored FM excerpts)                 │
│                              │                                  │
│                    ┌─────────┴──────────┐                       │
│                    │                   │                        │
│              Ollama present?      Ollama absent?                │
│            Qwen2.5:3b phrases   Raw doctrine passage            │
│               the answer          returned direct               │
│                    │                   │                        │
│                    └─────────┬─────────┘                        │
│                              ▼                                  │
│             Spoken answer + FM citation + depth tier            │
│             + append to audit log                               │
└─────────────────────────────────────────────────────────────────┘
```

- Push-to-talk voice (browser Web Speech API) → on-node brain answers → **spoken back with FM citation**.
- Restricted node refuses to pair without clearance → **ACCESS DENIED + audit log entry**.
- On-device model (Qwen via Ollama) phrases the answer if available; if absent, the retrieved doctrine passage is returned directly. **Both paths are 100% offline.**

---

## The Four Brains

| Brain | Node | Source doctrine | Clearance to pair |
|---|---|---|---|
| Combat Casualty Care (TCCC) | Medic comms device / air-gapped Pixel | TC 4-02.1 (MARCH), ATP 4-25.13 (9-Line MEDEVAC) | UNCLAS (full depth: CUI) |
| Equipment & Weapons Repair | Tank / weapon system on-platform compute | TC 3-22.9 (SPORTS / M4), TM 9-1005-313 (M240), TM 9-2320 (PMCS) | UNCLAS (full depth: CUI) |
| Policy, ROE & Reporting | Command post node | GTA 21-08 (SALUTE), Standing ROE / EOF, ATP 6-01.1 (SITREP) | UNCLAS |
| CBRN & Controlled Crypto | Hardened node (clearance-gated) | ATP 3-11.32 (CBRN), COMSEC handling procedures | SECRET |

---

## Need-to-Know Access Matrix

| Identity | MOS | Clearance | Medic node | Tank node | Command node | Restricted node |
|---|---|---|---|---|---|---|
| PVT Reyes | 11B Infantry | UNCLAS | Basic buddy-aid only | Basic IA drills only | Full | DENIED |
| SGT Okafor | 68W Combat Medic | CUI | Full TCCC depth | Basic only | Full | DENIED |
| SPC Hahn | 91B Wheeled Mechanic | CUI | Basic only | Full repair depth | Full | DENIED |
| CPT Vance | Cleared / S2 | SECRET | Full | Full | Full | GRANTED — full depth |

**Default = the lowest-common-denominator safe answer for everyone. Restricted depth unlocks by credential.** Every pairing attempt, grant, and denial is appended to the live audit log.

---

## How to Run

**Requirements:** Python 3.8+, Chrome (for Web Speech API). No pip installs. No API keys.

```bash
python server.py
```

Then open **http://localhost:8000** in Chrome.

- The provisioning animation runs first, showing the garrison load-out across all 7 sponsors.
- Toggle **COMMS → OFFLINE**. From that point, the machine can be physically disconnected.
- Select an identity, pair with a node, and push-to-talk (or type) a query.
- The answer is retrieved from on-device doctrine, spoken back, and cited to the real FM.

**On-device model (optional):** If Ollama is running on `localhost:11434` with `qwen2.5:3b` pulled, answers are phrased by the on-device Qwen model. If not, the raw retrieved doctrine passage is returned — both paths are fully offline.

```bash
# Optional — pulls ~2 GB, enhances answer phrasing
ollama run qwen2.5:3b
```

---

## Sponsor Credits

| Sponsor | Role in EDGE BRAIN MESH |
|---|---|
| **Unsiloed** | Parses FMs, TMs, and SOPs (PDFs, tables, diagrams, torque specs) into clean semantic chunks at provisioning time |
| **Moss** | Builds and maintains the real-time semantic index for each brain at provisioning time |
| **TrueFoundry** | Governs which brain goes to which node; encodes the per-identity need-to-know policy and produces the audit trail |
| **Qwen** | Provides the on-device voice packs and the on-device reasoning model (qwen2.5:3b via Ollama) that phrases answers in the field |
| **Minimax** | Performs heavy synthesis and cross-reference validation of doctrine content at provisioning time |
| **LiveKit** | Manages the live transport channel that pushes signed brain bundles to each edge node while comms are up |
| **AWS** | Cloud control plane — signs, packages, and orchestrates the push of brain bundles to every forward node |

---

## What Is Real vs. Simulated

This is an honest accounting.

| Component | Status |
|---|---|
| Field phase server (`server.py`) | **Real, working code.** Python stdlib only, no dependencies, runs fully offline. |
| Access control + audit log | **Real.** Enforced in `server.py` per the clearance matrix above. |
| Voice (push-to-talk) | **Real.** Browser Web Speech API (STT/TTS). Note: Chrome's STT makes a brief network call unless the device has an offline speech model installed — typed fallback always works air-gapped. |
| On-device Qwen phrasing | **Real if Ollama is running.** Gracefully degrades to raw retrieval if not. |
| Doctrine content | **Real public U.S. Army field manual excerpts.** TC 4-02.1, ATP 4-25.13, TC 3-22.9, TM 9-1005-313, ATP 3-11.32, GTA 21-08, ATP 6-01.1. |
| Provisioning animation (Phase 1) | **Faithful simulation.** The animation shows each sponsor's role in the pipeline; the full multi-sponsor live integration is out of scope for a 90-minute build. |
| Bluetooth / mesh pairing | **Simulated** in the UI (proximity-pair button). Real BLE/mesh integration is a hardware problem beyond a hackathon scope. |