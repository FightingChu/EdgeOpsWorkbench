"""RFC5424 header extraction preserves priority, structured data, and message text."""
import re
from .records import normalize
PATTERN=re.compile(r'^<([0-9]{1,3})>1 ([^ ]+) ([^ ]+) ([^ ]+) ([^ ]+) ([^ ]+) (.*)$')

def decode(text):
    if not isinstance(text,str) or len(text)>65536: raise ValueError("syslog record exceeds bounds")
    match=PATTERN.fullmatch(text)
    if not match or int(match[1])>191: raise ValueError("invalid RFC5424 header")
    priority=int(match[1]); rest=match[7]
    if rest.startswith('-'): structured='-'; message=rest[1:].removeprefix(' ')
    elif rest.startswith('['):
        depth=0; escaped=False; end=None
        for i,char in enumerate(rest):
            if escaped: escaped=False; continue
            if char==chr(92): escaped=True; continue
            if char=='[': depth+=1
            elif char==']':
                depth-=1
                if depth==0 and (i+1==len(rest) or rest[i+1]!='['): end=i+1; break
        if end is None: raise ValueError("unclosed structured data")
        structured=rest[:end]; message=rest[end:].removeprefix(' ')
    else: raise ValueError("invalid structured data")
    level=('critical','critical','critical','error','warning','info','info','debug')[priority%8]
    return normalize({'message':message or '(empty syslog message)','severity':level,'service':match[4] if match[4]!='-' else 'syslog','device_id':match[3] if match[3]!='-' else None,'recorded_at':match[2] if match[2]!='-' else None,'metadata':{'priority':priority,'facility':priority//8,'process_id':match[5],'message_id':match[6],'structured_data':structured}})
