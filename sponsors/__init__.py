"""
sponsors/ — one adapter per sponsor in the EDGE BRAIN MESH garrison deployment pipeline.
Each adapter exposes a single provision() -> dict function.
"""
from .unsiloed   import provision as unsiloed_provision
from .moss       import provision as moss_provision
from .truefoundry import provision as truefoundry_provision
from .qwen       import provision as qwen_provision
from .minimax    import provision as minimax_provision
from .livekit    import provision as livekit_provision
from .aws        import provision as aws_provision

__all__ = [
    "unsiloed_provision",
    "moss_provision",
    "truefoundry_provision",
    "qwen_provision",
    "minimax_provision",
    "livekit_provision",
    "aws_provision",
]