"""JSON pointer traversal implements escaped slash and tilde tokens."""

def tokens(pointer):
    if not isinstance(pointer,str) or len(pointer)>2048 or (pointer and not pointer.startswith('/')): raise ValueError("invalid JSON pointer")
    if pointer=='': return []
    parts=pointer[1:].split('/')
    for item in parts:
        index=0
        while index<len(item):
            if item[index]=='~':
                if index+1>=len(item) or item[index+1] not in '01': raise ValueError("invalid pointer escape")
                index+=1
            index+=1
    return [part.replace('~1','/').replace('~0','~') for part in parts]

def lookup(value,pointer):
    for token in tokens(pointer):
        if not isinstance(value,dict) or token not in value: raise ValueError("JSON pointer not found")
        value=value[token]
    return value
