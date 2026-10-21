"""Byte-size settings distinguish decimal and binary units."""
import re

def parse_size(value):
    if not isinstance(value,str): raise ValueError("size must be text")
    match=re.fullmatch(r'([0-9]{1,12})(B|KB|MB|GB|KiB|MiB|GiB)',value)
    if not match: raise ValueError("invalid byte size")
    scale={'B':1,'KB':1000,'MB':1000000,'GB':1000000000,'KiB':1024,'MiB':1048576,'GiB':1073741824}[match[2]]
    result=int(match[1])*scale
    if not 1<=result<=1073741824: raise ValueError("size outside bounds")
    return result
