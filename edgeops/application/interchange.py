"""Bounded file conversion translates event formats without altering input evidence."""
from pathlib import Path
from ..codecs.registry import decode_events
from ..codecs.encoding import decode

class InterchangeService:
    def read(self,path,format,encoding='utf-8'):
        with Path(path).open('rb') as stream: data=stream.read(8388609)
        if len(data)>8388608: raise ValueError('event file exceeds 8388608 bytes')
        return decode_events(decode(data,encoding),format)
    def convert(self,source,destination,source_format,target_format='ndjson',encoding='utf-8'):
        from .exports import write_events
        rows=self.read(source,source_format,encoding)
        result=write_events(rows,destination,target_format)
        return {'records':len(rows),**result}
