"""Alert transitions separate firing, acknowledgement, resolution, and reopening."""
TRANSITIONS={'open':{'ack':'acknowledged','resolve':'resolved'},'acknowledged':{'resolve':'resolved'},'resolved':{'reopen':'open'}}

def transition(state,action):
    if state not in TRANSITIONS or action not in TRANSITIONS[state]: raise ValueError("invalid alert transition")
    return TRANSITIONS[state][action]
