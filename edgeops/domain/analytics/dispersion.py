"""Population and sample variance for bounded telemetry samples."""
import statistics
from .samples import numbers

def dispersion(values, sample=False):
    data = numbers(values, minimum=2 if sample else 1)
    return {"variance": statistics.variance(data) if sample else statistics.pvariance(data),
            "stdev": statistics.stdev(data) if sample else statistics.pstdev(data)}
