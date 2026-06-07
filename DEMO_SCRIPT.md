# EDGE BRAIN MESH — Demo Script

**Target runtime: 75–90 seconds.**
Format: screen recording of Chrome on localhost:8000. No cuts needed — linear flow.
Narration is spoken over the recording. "Click" annotations indicate what is on screen.

---

## Beat A — Provisioning (0:00 – 0:15) ~15 seconds

**What is on screen:** The provisioning animation. Seven sponsor pipeline stages light up in sequence — Unsiloed, Moss, TrueFoundry, Qwen, Minimax, LiveKit, AWS — and four node cards (Medic, Tank, Command, Restricted) each tick green as their brain bundle lands.

**Narration:**
> "This is garrison. Comms are up. We're using the full stack — Unsiloed parses the field manuals, Moss indexes them, TrueFoundry encodes who can see what, Qwen loads the on-device voice model, Minimax validates the doctrine, LiveKit pushes the bundles, and AWS orchestrates the whole thing. Four edge nodes. Four brains. Fully provisioned."

**Action:** Let the animation complete. All four node cards show a green checkmark.

---

## Beat B — Comms offline (0:15 – 0:22) ~7 seconds

**What is on screen:** The large COMMS toggle at the top of the screen, currently showing ONLINE (green).

**Narration:**
> "Now we go forward. Comms denied."

**Action:** Click the COMMS toggle. It flips to OFFLINE (red). A status banner reads: "Operating fully local — zero internet."

**Narration (immediately after the click):**
> "From this point, nothing touches the cloud. The network cable could be cut. It doesn't matter."

---

## Beat C — Medic asks about arterial bleeding (0:22 – 0:45) ~23 seconds

**What is on screen:** The identity selector showing four options.

**Action:** Click the identity selector and choose **SGT Okafor — 68W Combat Medic**.

**Action:** Click the **Medic node** card (COMBAT CASUALTY CARE BRAIN). The status line shows "PAIRED — full TCCC depth."

**Action:** Click the push-to-talk mic button and speak, or type into the query field:
> "arterial bleeding on the left thigh"

**What is on screen:** The answer panel populates. The system reads back the tourniquet protocol, spoken aloud by the browser TTS.

**Narration (while the answer is being read back):**
> "SGT Okafor. Full medic credentials. Full TCCC depth. The brain walks through MARCH — tourniquet high and tight, mark the time, don't loosen it."

**What is on screen below the answer:** Citation line — `TCCC Guidelines / TC 4-02.1, MARCH` — and depth badge reading `FULL`.

**Narration:**
> "Cited. TC 4-02.1. No internet. No cloud."

---

## Beat D — Rifleman asks the same question (0:45 – 1:02) ~17 seconds

**Action:** Click the identity selector and switch to **PVT Reyes — 11B Infantry**.

**Action:** Click the **Medic node** card again. Status line shows "PAIRED — basic buddy-aid tier."

**Action:** Click push-to-talk and say (or type):
> "arterial bleeding on the left thigh"

**What is on screen:** A different, shorter answer appears and is read aloud.

**Narration (while answer plays):**
> "Same question. Different soldier. PVT Reyes holds UNCLAS — buddy-aid tier only."

**What is on screen:** Answer text ends with: "This exceeds your scope. Initiate MEDEVAC." Depth badge reads `BASIC (buddy-aid tier)`.

**Narration:**
> "The brain knows its audience. It tells him exactly what he can do, and stops there."

---

## Beat E — Rifleman tries the Restricted node (1:02 – 1:12) ~10 seconds

**Action:** With PVT Reyes still selected, click the **Restricted node** card (CBRN & CONTROLLED CRYPTO BRAIN, lock icon).

**What is on screen:** The node card flashes red. A bold denial message appears immediately — no query needed.

**Narration:**
> "Rifleman tries the restricted node."

**What is on screen:** Text reads: `ACCESS DENIED — SECRET clearance required to pair. You hold UNCLAS. Need-to-know not established.`

**What is on screen, audit log panel (bottom of screen):** A new line appears: `DENIED  PVT Reyes - 11B Infantry  ->  CBRN & CONTROLLED CRYPTO BRAIN`

**Narration:**
> "Denied. And logged."

---

## Beat F — Officer pairs with Restricted node (1:12 – 1:28) ~16 seconds

**Action:** Click the identity selector and switch to **CPT Vance — Cleared / S2**.

**Action:** Click the **Restricted node** card.

**What is on screen:** Status line shows "PAIRED — full depth."

**Action:** Click push-to-talk and say (or type):
> "CBRN attack, chemical agent"

**What is on screen:** CBRN reaction protocol appears and is read aloud.

**Narration (while answer plays):**
> "Officer. SECRET. The restricted node opens. CBRN reaction: don the mask in nine seconds, Gas Gas Gas, MOPP 4, decon, report to higher."

**What is on screen:** Citation reads `ATP 3-11.32, CBRN Reaction`.

---

## Beat G — Audit log pan (1:28 – 1:35) ~7 seconds

**Action:** Scroll down to or expand the **AUDIT LOG** panel. Three entries are visible:

```
SERVED  SGT Okafor - 68W Combat Medic  ->  COMBAT CASUALTY CARE BRAIN  [TC 4-02.1, MARCH]
SERVED  PVT Reyes - 11B Infantry       ->  COMBAT CASUALTY CARE BRAIN  [TC 4-02.1, MARCH]
DENIED  PVT Reyes - 11B Infantry       ->  CBRN & CONTROLLED CRYPTO BRAIN
SERVED  CPT Vance - Cleared / S2       ->  CBRN & CONTROLLED CRYPTO BRAIN  [ATP 3-11.32]
```

**Narration:**
> "Every pair, every answer, every denial — logged. Comms come back up, this syncs. Comms stay down, the record is still there. Provision in garrison. Operate at the edge."

**Action:** Hold on the audit log for two seconds. End recording.

---

## Total Runtime

| Beat | Content | Time |
|---|---|---|
| A | Provisioning animation | 0:00 – 0:15 |
| B | COMMS → OFFLINE toggle | 0:15 – 0:22 |
| C | Medic / arterial bleeding / full answer | 0:22 – 0:45 |
| D | Rifleman / same query / buddy-aid tier | 0:45 – 1:02 |
| E | Rifleman denied on Restricted node | 1:02 – 1:12 |
| F | Officer paired, CBRN answer | 1:12 – 1:28 |
| G | Audit log pan and close | 1:28 – 1:35 |
| **Total** | | **~1:35** |

Trim Beat A to 10 seconds to hit 75 seconds tight; the animation can be sped up 1.5x in post if needed.
