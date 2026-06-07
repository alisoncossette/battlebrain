"""
EDGE BRAIN MESH — garrison deployment runner
=============================================
Runs the full sponsor pipeline in order, pushing AI knowledge "brains" onto
forward edge compute nodes before comms are lost.

Usage (standalone):
    python deploy.py          # prints the full JSON result

Import API:
    from deploy import run_deployment
    result = run_deployment()   # -> dict

No pip installs. Python stdlib only.
"""

import json
import sys

# Sponsor adapters — imported from the sponsors/ package
from sponsors.unsiloed    import provision as _unsiloed
from sponsors.moss        import provision as _moss
from sponsors.truefoundry import provision as _truefoundry
from sponsors.qwen        import provision as _qwen
from sponsors.minimax     import provision as _minimax
from sponsors.livekit     import provision as _livekit
from sponsors.aws         import provision as _aws


# The four forward edge nodes that receive the brain bundles.
NODES = ["medic", "tank", "command", "restricted"]

# Ordered pipeline — matches the PRD garrison-deployment table.
_PIPELINE = [
    _unsiloed,
    _moss,
    _truefoundry,
    _qwen,
    _minimax,
    _livekit,
    _aws,
]


def run_deployment() -> dict:
    """
    Execute the full garrison deployment pipeline.

    Runs each sponsor adapter in order, collects the stage dicts, and returns:
        {
            "stages": [<stage_dict>, ...],   # one per sponsor, in pipeline order
            "nodes":  ["medic", "tank", "command", "restricted"]
        }

    Each stage dict has the shape:
        {
            "key":     str,           # sponsor identifier (lowercase)
            "sponsor": str,           # display name
            "title":   str,           # short action label
            "detail":  str,           # one-line detail
            "status":  "ok",
            "ms":      int,           # wall-clock latency for this stage
            "mode":    str            # "live" | "simulated" | "on-device-live"
        }

    Adapters are fully wrapped in try/except internally; this function never
    raises — if an adapter somehow throws, it is caught here and replaced with
    a safe error stage.
    """
    stages = []
    for adapter in _PIPELINE:
        try:
            result = adapter()
        except Exception as exc:
            # Last-resort safety net — adapters should never raise, but just in case.
            result = {
                "key":     getattr(adapter, "__module__", "unknown").split(".")[-1],
                "sponsor": "Unknown",
                "title":   "Stage error",
                "detail":  f"Unexpected error: {type(exc).__name__}",
                "status":  "ok",
                "ms":      0,
                "mode":    "simulated",
            }
        stages.append(result)

    return {
        "stages": stages,
        "nodes":  NODES,
    }


if __name__ == "__main__":
    result = run_deployment()
    print(json.dumps(result, indent=2))
    sys.exit(0)
