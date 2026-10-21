"""Loopback endpoint validation rejects credentials, redirects, and fragments."""
from urllib.parse import urlsplit

def local_endpoint(value):
    if not isinstance(value,str) or len(value)>2048 or any(ord(c)<=32 for c in value): raise ValueError("invalid endpoint")
    try:
        parts=urlsplit(value); port=parts.port
    except ValueError: raise ValueError("invalid endpoint") from None
    if parts.scheme!='http' or parts.hostname not in ('127.0.0.1','localhost','::1') or parts.username or parts.password or parts.fragment:
        raise ValueError("endpoint must be credential-free loopback HTTP")
    if port is None or not 1<=port<=65535: raise ValueError("endpoint requires a valid port")
    return parts.geturl()
