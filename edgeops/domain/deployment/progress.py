"""Transfer progress and fleet summaries reject impossible byte counts."""
from ..validation import integer

def transfer(total,received):
    integer(total,'total',1,16777216); integer(received,'received',0,total)
    return {'total_bytes':total,'received_bytes':received,'percent':received*100/total,'complete':received==total}

def fleet(states):
    allowed={'queued','transferring','verifying','applying','succeeded','failed','cancelled','rolling_back','rolled_back','rollback_failed'}
    counts={}
    for state in states:
        if state not in allowed: raise ValueError("unknown deployment state")
        counts[state]=counts.get(state,0)+1
    return {'total':sum(counts.values()),'counts':counts,'succeeded':counts.get('succeeded',0)}
