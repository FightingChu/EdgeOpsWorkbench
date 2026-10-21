"""Telemetry summary combines quantiles and robust anomaly metadata."""
import math
from .samples import numbers
from .quantiles import percentile
from .dispersion import dispersion
from .anomalies import detect

def summarize(values):
    data=numbers(values)
    return {"count":len(data),"minimum":min(data),"maximum":max(data),"mean":math.fsum(data)/len(data),"p50":percentile(data,50),"p95":percentile(data,95),"dispersion":dispersion(data),"anomalies":detect(data)}
