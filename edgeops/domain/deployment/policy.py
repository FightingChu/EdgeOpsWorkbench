"""Rollout policies bound batch size, failure budget, and transfer chunks."""
from dataclasses import dataclass
from ..validation import integer

@dataclass(frozen=True)
class RolloutPolicy:
    batch_size: int = 10
    max_failures: int = 0
    canary_count: int = 1
    chunk_size: int = 4096
    def __post_init__(self):
        integer(self.batch_size,'batch_size',1,1000)
        integer(self.max_failures,'max_failures',0,10000)
        integer(self.canary_count,'canary_count',0,1000)
        integer(self.chunk_size,'chunk_size',1,65536)

def may_continue(succeeded,failed,policy):
    integer(succeeded,'succeeded',0,10000); integer(failed,'failed',0,10000)
    if not isinstance(policy,RolloutPolicy): raise ValueError("invalid rollout policy")
    return failed<=policy.max_failures
