"""Device sequence windows detect duplicates and gaps without altering persistence."""
class SequenceTracker:
    def __init__(self): self.last={}
    def observe(self,device_id,sequence):
        if not isinstance(device_id,str) or not device_id or len(device_id)>64 or type(sequence) is not int or not 0<=sequence<2**32: raise ValueError("invalid device sequence")
        previous=self.last.get(device_id)
        if previous is None: self.last[device_id]=sequence; return {'status':'first','missing':0}
        delta=(sequence-previous)%(2**32)
        if delta==0: return {'status':'duplicate','missing':0}
        if delta>=2**31: return {'status':'old','missing':0}
        self.last[device_id]=sequence
        return {'status':'gap' if delta>1 else 'next','missing':delta-1}
