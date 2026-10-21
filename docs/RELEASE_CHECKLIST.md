# Maintenance checks

The repository provides unit and regression tests, an independent verification script, JavaScript syntax checks, and backup round-trip tests. Database and backup manifests record schema version and integrity information. Generated databases, logs, caches, and local configuration are excluded from Git.

```powershell
python -m unittest discover -s tests -v
python scripts/verify.py
node --check edgeops/static/app.js
node --check edgeops/static/sw.js
node --check edgeops/static/sw-register.js
```
