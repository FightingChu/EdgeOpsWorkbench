"""Device deployment inventories reject duplicate targets and unknown states."""
from copy import deepcopy
from .compatibility import version_tuple

def normalize_devices(devices):
    if not isinstance(devices,list) or not 1<=len(devices)<=10000: raise ValueError("invalid device inventory size")
    result=[]; seen=set()
    for device in devices:
        if not isinstance(device,dict) or set(device)!={'id','kind','version','online'}: raise ValueError("invalid inventory fields")
        identity=device['id']
        if not isinstance(identity,str) or not 1<=len(identity)<=64 or any(ord(c)<32 for c in identity) or identity in seen: raise ValueError("invalid or duplicate device id")
        if not isinstance(device['kind'],str) or not device['kind'] or type(device['online']) is not bool: raise ValueError("invalid device kind or online state")
        version_tuple(device['version']); seen.add(identity); result.append(deepcopy(device))
    return sorted(result,key=lambda item:item['id'])
