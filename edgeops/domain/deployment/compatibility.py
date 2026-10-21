"""Release compatibility uses numeric versions and explicit downgrade permission."""
import re

def version_tuple(value):
    if not isinstance(value,str) or not re.fullmatch(r'[0-9]{1,6}[.][0-9]{1,6}[.][0-9]{1,6}',value): raise ValueError("invalid semantic version")
    return tuple(int(part) for part in value.split('.'))

def check(device,manifest,allow_downgrade=False):
    if type(allow_downgrade) is not bool: raise ValueError("downgrade permission must be boolean")
    current=version_tuple(device['version']); target=version_tuple(manifest['artifact']['version']); minimum=version_tuple(manifest['minimum_version'])
    if device['kind']!=manifest['device_kind']: return {'compatible':False,'reason':'device kind differs'}
    if not device['online']: return {'compatible':False,'reason':'device is offline'}
    if current<minimum: return {'compatible':False,'reason':'current version below minimum'}
    if target<current and not allow_downgrade: return {'compatible':False,'reason':'downgrade disabled'}
    return {'compatible':True,'reason':'compatible'}
