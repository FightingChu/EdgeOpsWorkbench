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
python -m edgeops serve --host 127.0.0.1 --port 8877 --open
python -m unittest discover -s tests -v
python scripts/verify.py
```

Use `--data-dir <path>` with any CLI command to isolate runtime data. A local `config.local.json` can provide defaults and is ignored by Git.
