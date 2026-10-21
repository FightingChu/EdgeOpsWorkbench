"""CSV event interchange preserves embedded newlines and metadata JSON."""
import csv,io,json
from .records import normalize
FIELDS=['message','severity','service','device_id','recorded_at','kind','metadata']

def encode(rows):
    output=io.StringIO(newline=''); writer=csv.DictWriter(output,fieldnames=FIELDS); writer.writeheader()
    for index,row in enumerate(rows):
        if index>=10000: raise ValueError("too many CSV records")
        item=normalize(row); item['metadata']=json.dumps(item['metadata'],ensure_ascii=False,allow_nan=False); writer.writerow(item)
    return output.getvalue()

def decode(text):
    if not isinstance(text,str) or len(text.encode('utf-8'))>8388608: raise ValueError("CSV exceeds bounds")
    reader=csv.DictReader(io.StringIO(text,newline=''))
    if reader.fieldnames!=FIELDS: raise ValueError("CSV header does not match event schema")
    result=[]
    try:
        for row in reader:
            if len(result)>=10000 or None in row or any(v is None for v in row.values()): raise ValueError("invalid CSV record")
            row['device_id']=row['device_id'] or None; row['recorded_at']=row['recorded_at'] or None
            row['metadata']=json.loads(row['metadata']); result.append(normalize(row))
    except csv.Error as exc: raise ValueError("invalid CSV: "+str(exc)) from None
    return result
