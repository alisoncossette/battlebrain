# EDGE BRAIN MESH — PRD

> **"Provision in garrison with the full cloud stack. Operate at the edge with none of it."**
> Comms are down. The knowledge isn't.

---

## 1. The problem

Voice models are now cheap, fast, and good. In the field the bottleneck is **getting the
right authoritative knowledge to the right person — when comms are denied (DDIL).**
Cloud RAG dies the moment the link drops. Soldiers need first-aid, equipment-repair, and
policy answers *exactly* when they have no connectivity.

## 2. The idea

Knowledge is **pre-positioned onto whatever compute is already forward**:

- The **tank / weapon system** carries its own **repair brain** (its TMs live on its compute).
- The **medic's comms device / air-gapped Pixel** carries the **TCCC brain**.
- The **command node** carries the **policy / ROE / reporting brain**.
- A **hardened node** carries the **CBRN / crypto brain**, locked to clearance.

> Anything with compute holds a brain and can be reached. A soldier **pairs locally**
> (Bluetooth / mesh — no internet) with the nearest node and **talks to its brain**.
> *Who* can pair with *what* is the access-control layer.

## 3. Two phases (this is the whole architecture)

### Phase 1 — DEPLOYMENT / GARRISON (comms UP) — *the first thing that happens*
The load-out. The **entire sponsor stack** runs here to build and push the brains onto the
edge nodes, so loss of comms later is survivable. **All brains are updated at deployment.**

| Step | What happens | Sponsor |
|---|---|---|
| Ingest | Parse FMs / TMs / SOPs (PDF, tables, diagrams, torque specs) into clean chunks | **Unsiloed** |
| Index | Build a real-time semantic index per brain | **Moss** |
| Govern | Decide which brain → which node, and the per-identity need-to-know policy + audit | **TrueFoundry** |
| Voice | Generate per-node voice packs + the on-device reasoning model | **Qwen** |
| Reason | Heavy synthesis / validation at provisioning time | **Minimax** |
| Transport | Live update channel to each node | **LiveKit** |
| Orchestrate | Cloud control plane pushes signed brain bundles to every node | **AWS** |

### Phase 2 — FIELD / MISSION (comms DOWN)
Operate fully local. **Zero internet.**
- Pick identity → pair with nearest node (proximity/Bluetooth, simulated).
- **Push-to-talk voice** → on-node brain answers → **spoken back with a citation** to the real FM.
- Restricted node refuses to pair without clearance → **access-denied + audit log**.
- On-device model (Qwen via Ollama) phrases the answer; if absent, the node returns the
  retrieved doctrine passage directly — still 100% offline.

## 4. Access / need-to-know model

| Identity | Clearance | Can pair with | Restricted node |
|---|---|---|---|
| PVT Reyes (11B Infantry) | UNCLAS | medic*, tank*, command | DENIED |
| SGT Okafor (68W Medic) | CUI | medic (full), tank*, command | DENIED |
| SPC Hahn (91B Mechanic) | CUI | tank (full), medic*, command | DENIED |
| CPT Vance (Cleared / S2) | SECRET | all | **GRANTED** |

\* basic / buddy-aid tier only. Depth unlocks by credential. **Default = the safe
lowest-common-denominator answer for everyone; restricted depth unlocks by need-to-know.**

## 5. The four brains (real, public doctrine)

1. **TCCC** — MARCH, tourniquet, chest seal, 9-line MEDEVAC, TXA  *(TC 4-02.1 / ATP 4-25.13)*
2. **Equipment repair** — SPORTS immediate action, M240 stoppage, vehicle no-start PMCS  *(TC 3-22.9 / TM 9-…)*
3. **Policy/ROE/reporting** — SALUTE, ROE/EOF, SITREP  *(GTA 21-08 / ATP 6-01.1)*
4. **Restricted CBRN/crypto** — CBRN reaction, COMSEC handling  *(ATP 3-11.32)* — clearance-gated

## 6. Demo flow (the 60–90s video)

1. **PROVISIONING** screen: animated pipeline lights up each sponsor pushing brains to 4 nodes.
2. Big toggle: **COMMS → OFFLINE.** (Drop the mic — from here, nothing touches the cloud.)
3. As **Medic**, pair with Medic node, say *"arterial bleeding on the left thigh"* → spoken
   tourniquet steps + citation.
4. As **Rifleman**, ask the same → **basic buddy-aid tier** + "exceeds your scope, initiate MEDEVAC."
5. As **Rifleman**, try the **Restricted** node → **ACCESS DENIED**, audit line appears.
6. As **Officer**, pair with Restricted → CBRN answer. Pan the **audit log**.

## 7. Scope split

| | Full vision (pitch) | 90-min build (record) |
|---|---|---|
| Deployment phase | All 7 sponsors integrated | **Animated simulation** that name-checks each sponsor's job |
| Field phase | On-device Qwen + Moss on real edge HW | **Real, working** local server + browser voice + retrieval; Qwen-on-device if Ollama finishes |
| Voice | LiveKit + Qwen voice packs | Browser Web Speech (STT/TTS), push-to-talk |
| Access control | TrueFoundry gateway | **Real** clearance enforcement + audit in the local server |

## 8. Build (90 min, zero-dependency core)

- `server.py` — Python stdlib HTTP server. Serves UI, enforces access, retrieves from the
  4 brains, optionally phrases via on-device Qwen (Ollama). **No pip installs.**
- `index.html` — tactical dark UI: provisioning animation → COMMS toggle → 4 node cards →
  identity selector → push-to-talk voice → transcript with citations → live audit log.
- Brains = real public FM excerpts embedded in `server.py` (small enough to skip a vector DB).
- Ollama + `qwen2.5:3b` installing in background = on-device brain if it lands in time;
  pure local retrieval if not. **Video records either way.**

## 9. Risks

- **No API keys / no Ollama yet** → core is built to need neither. ✅ insurance.
- **Web Speech STT uses network in Chrome** → push-to-talk works; can fall back to typed
  query for the strict air-gap shot. Mention in script.
- **All-sponsor live integration** is out of 90-min scope → shown as the provisioning
  simulation; clearly framed as such.
