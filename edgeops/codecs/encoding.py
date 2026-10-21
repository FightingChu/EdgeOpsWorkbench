"""Explicit text encoding adapter distinguishes BOMs and decode errors."""
import codecs
ALLOWED={'utf-8','utf-8-sig','gb18030','cp1252'}

def decode(data,encoding='utf-8'):
    if not isinstance(data,bytes) or len(data)>8388608: raise ValueError("invalid encoded data")
    try: name=codecs.lookup(encoding).name
    except (LookupError,TypeError): raise ValueError("unknown encoding") from None
    if name not in ALLOWED: raise ValueError("unsupported encoding")
    try: return data.decode(name)
    except UnicodeError: raise ValueError("data does not match encoding") from None
