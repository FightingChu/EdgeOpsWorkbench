# Commands

```powershell
python -m edgeops init
python -m edgeops demo
python -m edgeops summary
python -m edgeops import-events fixtures/demo_events.jsonl
python -m edgeops events --severity warning --limit 20
python -m edgeops diagnostics
python -m edgeops backup data/backup-2026-10-19
python -m edgeops cases list
python -m edgeops analytics temperature --device-id press-01
python -m edgeops configuration inspect config.example.json
python -m edgeops evaluate-rules <rules.json> --limit 50
python -m edgeops convert-events <source.json> <new-events.csv> --from-format json --to-format csv
python -m edgeops export-events <new-snapshot.ndjson> --limit 10000
python -m edgeops deployments register <firmware.bin> --version 1.0.0
python -m edgeops deployments create press-01 <artifact-id>
python -m edgeops deployments simulate <deployment-id> <firmware.bin>
python -m edgeops serve --host 127.0.0.1 --port 8877 --open
python -m unittest discover -s tests -v
python scripts/verify.py
python scripts/source_audit.py --minimum 300
```

Use `--data-dir <path>` with any CLI command to isolate runtime data. A local `config.local.json` can provide defaults and is ignored by Git.
