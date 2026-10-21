"""Firmware lifecycle disallows success before transfer and digest verification."""
TRANSITIONS={'queued':{'start':'transferring','cancel':'cancelled'},'transferring':{'transferred':'verifying','fail':'failed','cancel':'cancelled'},'verifying':{'verified':'applying','fail':'failed','cancel':'cancelled'},'applying':{'applied':'succeeded','fail':'failed'},'succeeded':{'rollback':'rolling_back'},'failed':{'retry':'queued','rollback':'rolling_back'},'rolling_back':{'restored':'rolled_back','fail':'rollback_failed'},'cancelled':{},'rolled_back':{},'rollback_failed':{}}

def transition(state,action):
    if state not in TRANSITIONS or action not in TRANSITIONS[state]: raise ValueError("invalid deployment transition")
    return TRANSITIONS[state][action]

def terminal(state):
    if state not in TRANSITIONS: raise ValueError("unknown deployment state")
    return state in ('succeeded','cancelled','rolled_back','rollback_failed')
