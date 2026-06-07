# EDGE BRAIN MESH — Judge Pitch

---

## The Problem

Soldiers in DDIL (Denied, Degraded, Intermittent, Limited) environments lose access to authoritative knowledge exactly when they need it most. A medic treating arterial bleeding on a jammed radio network cannot reach a cloud RAG endpoint. A mechanic clearing a weapon stoppage in a contested zone has no signal. A rifleman asking about escalation of force has thirty seconds and no connectivity.

The bottleneck is not voice. Voice models are cheap and good. **The bottleneck is retrieval at the edge — getting the right answer, to the right person, with the right clearance, when the link is dead.**

---

## The Key Insight

You do not need the cloud in the field. You need the cloud **before** the field.

Every forward asset — a tank, a medic's device, a command post laptop, a hardened comms node — already has compute. That compute sits idle most of the time. The insight is simple: **use garrison time, when comms are available and the full cloud stack is reachable, to pre-position knowledge onto that compute.** Then operate fully local. The cloud does its work once, in advance. The edge carries the result forward.

This is not a new idea in logistics. It is a new idea in knowledge retrieval.

---

## What We Built

**EDGE BRAIN MESH** is a voice-first, comms-denied field-knowledge system in two phases.

**Phase 1 — Deployment (garrison, comms UP):** A provisioning pipeline uses the full sponsor stack to parse field manuals, build semantic indexes, validate doctrine, encode need-to-know access policy, generate on-device voice and reasoning models, and push signed brain bundles to every forward node via a live transport channel. This phase is shown in the demo as a **faithful provisioning simulation** — the animated pipeline accurately represents each sponsor's role; live multi-sponsor integration is beyond a 90-minute hackathon build and we say so plainly.

**Phase 2 — Field operation (comms DOWN): this is real, working code.** `server.py` is a zero-dependency Python server that:
- Enforces the clearance-based access matrix (4 identities x 4 nodes) with real access denial and audit logging
- Retrieves from four on-device brains built from real, public U.S. Army doctrine (TC 4-02.1, ATP 4-25.13, TC 3-22.9, TM 9-1005-313, ATP 3-11.32, GTA 21-08, ATP 6-01.1)
- Phrases answers with an on-device Qwen model via Ollama if available, returns raw doctrine passages if not
- Operates with zero internet, zero API keys, zero pip installs
- Speaks answers back with FM citations and a live audit log

A rifleman gets buddy-aid steps and a MEDEVAC prompt. The same question from a medic gets full TCCC depth. A rifleman who tries the restricted CBRN node gets ACCESS DENIED, and that denial is logged.

---

## Why This Sponsor Stack

This is not a generic LLM demo that could run on any stack. Each sponsor is uniquely suited to its role in the provisioning pipeline.

| Sponsor | Why this one specifically |
|---|---|
| **Unsiloed** | Military doctrine is dense PDFs, tables, torque specs, and diagrams — not clean prose. Unsiloed's document parsing is built for exactly this kind of structured, heterogeneous technical content. |
| **Moss** | Real-time semantic indexing that can be run at provisioning time and embedded on-device. The index ships with the brain bundle. |
| **TrueFoundry** | Governance and access policy are not an afterthought here — they are the system. TrueFoundry's model-governance layer is the right home for encoding clearance tiers, need-to-know rules, and the audit trail that follows every pairing decision. |
| **Qwen** | On-device inference is the entire field-phase value proposition. Qwen2.5:3b via Ollama runs on a soldier's device with no network. The voice packs are generated at provisioning time. This is the only model family designed from the ground up for both on-device deployment and multilingual voice. |
| **Minimax** | Heavy cross-reference validation of doctrine content happens once, at provisioning time, where compute is available. Minimax handles the synthesis that would be too expensive to run on edge hardware. |
| **LiveKit** | The provisioning push is a live channel problem: signed brain bundles being pushed to multiple nodes simultaneously while the link is up. LiveKit's real-time transport layer is the right primitive. |
| **AWS** | Cloud control plane — signs the bundles, tracks which node has which brain version, and orchestrates the push. The garrison infrastructure that makes the field-phase independence possible. |

---

## Defense Impact

**TCCC knowledge at the edge saves lives.** The number-one preventable cause of death on the modern battlefield is hemorrhage. A soldier who knows to apply a tourniquet high and tight, mark the time, and not loosen it — in the first minutes, without radio, without a medic present — survives. This system puts that knowledge on every device, spoken back in clear steps, tiered by training.

Beyond TCCC: equipment availability, ROE compliance, CBRN survival, and accurate reporting all degrade when soldiers cannot access doctrine under stress. EDGE BRAIN MESH addresses all four.

The access matrix is also a force-protection feature. A rifleman cannot accidentally surface controlled COMSEC or CBRN procedures he has no context to handle safely. The system enforces this automatically, every time, and logs it.

---

## Honesty About Real vs. Simulated

We built the hard part first: the **field phase is fully real** — offline, enforced access control, real doctrine, working voice. The provisioning animation is a faithful representation of what a full deployment pipeline would look like using these sponsors; it is not connected to live sponsor APIs in this build. We made this choice deliberately: a hackathon demo that ships real field-phase logic and honest framing is more useful than a demo that claims more than it delivers.

---

## The Ask

Judge this on the insight, not the integration depth. The insight is: **provision with the cloud, operate without it.** The architecture is sound. The field phase works. The sponsor mapping is non-arbitrary. The doctrine is real.

The next step is integrating the provisioning pipeline against live sponsor APIs, deploying to actual edge hardware (Pixel devices, Jetson nodes), and replacing browser Web Speech with fully on-device STT. The foundation is here.

> **Comms denied. Knowledge isn't.**
