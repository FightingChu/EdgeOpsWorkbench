# Benchmark Cases

Cases create controlled defects or environmental conditions in disposable project copies. The clean repository must remain runnable.

Each case directory will contain:

```text
case-id/
  manifest.json
  rounds.md
  setup.py
  public_tests/
  verify.py
```

`manifest.json` records the domain, subdomain, mechanism, base category, number of turns, persistent constraints, setup command, public validation, and verifier command. `rounds.md` contains only operator-visible prompts. Private expected reasoning or hidden checks must not be placed in public task text.

Setup scripts must:

1. Require an explicit disposable target path.
2. Refuse the repository root, home directory, drive root, and existing non-case directories.
3. Copy or patch only the disposable target.
4. Record the source revision and applied changes.
5. Never alter Git remotes, user configuration, or the clean source database.

Verification scripts should check observable behavior, preserved constraints, requested evidence, and prohibited side effects. They must return a nonzero exit status on failure.

