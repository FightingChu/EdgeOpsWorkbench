"""Bounded telemetry reports built from persisted readings and domain statistics."""
from ..domain.analytics.summary import summarize
from ..domain.analytics.rollups import rollup
from ..domain.analytics.regression import fit
from ..domain.models import _text
from ..domain.validation import integer

class AnalyticsService:
    def __init__(self,operations): self.operations=operations; self.database=operations.database
    def readings(self,metric,device_id=None,limit=1000):
        metric=_text(metric,'metric',64); integer(limit,'limit',1,10000)
        clauses=['metric=?']; values=[metric]
        if device_id is not None: clauses.append('device_id=?'); values.append(_text(device_id,'device id',64))
        self.database.initialize()
        with self.database.connect() as connection:
            rows=connection.execute('SELECT id,device_id,metric,value,unit,recorded_at FROM telemetry WHERE '+' AND '.join(clauses)+' ORDER BY id DESC LIMIT ?',(*values,limit)).fetchall()
            return [dict(row) for row in reversed(rows)]
    def report(self,metric,device_id=None,limit=1000):
        rows=self.readings(metric,device_id,limit)
        groups=rollup(rows); series=[]
        for group in groups:
            values=[row['value'] for row in rows if row['device_id']==group['device_id']]
            series.append({'device_id':group['device_id'],'metric':metric,'unit':next(row['unit'] for row in rows if row['device_id']==group['device_id']),'statistics':summarize(values),'trend_per_reading':fit(range(len(values)),values) if len(values)>1 else None})
        return {'metric':metric,'count':len(rows),'limit':limit,'series':series}
