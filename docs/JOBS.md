# Durable jobs

Workers claim one pending job with a lease. Expired leases return to pending until the attempt budget is exhausted. A completion checks the lease token and expiry, so a stale worker cannot commit a result.
