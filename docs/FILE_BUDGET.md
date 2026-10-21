# Maintained File Inventory

The repository contains 513 maintained files as of 2026-10-21. File inventory and executable-source counts are reported separately.

| Area | Maintained files |
| --- | ---: |
| Repository configuration and entrypoints | 7 |
| Product code and static assets (`edgeops/`) | 191 |
| Unit, integration, HTTP, and regression tests (`tests/`) | 130 |
| Benchmark bundles, schema, and authoring assets (`cases/`) | 129 |
| Curated fixtures (`fixtures/`) | 26 |
| Plugin implementations and manifests (`plugins/`) | 8 |
| Documentation (`docs/`) | 20 |
| Verification and AST audit scripts (`scripts/`) | 2 |
| **Total** | **513** |

Generated data, caches, build products, scenario workspaces, vendored dependencies, and duplicate build output are excluded. Maintained files have a defined product, test, fixture, configuration, or documentation purpose.

```powershell
(git ls-files | Measure-Object).Count
python scripts/source_audit.py --minimum 300
```

## Executable Python files

| Area | Effective Python files |
| --- | ---: |
| Product (`edgeops/`) | 166 |
| Plugins (`plugins/`) | 4 |
| Tools (`scripts/`) | 2 |
| Tests (`tests/`) | 129 |
| **Subtotal excluding cases** | **301** |
| Case tests (`cases/`) | 18 |
| **Total** | **319** |

The audit parses ASTs and requires an implemented function or method. Empty files, pure imports, docstring-only files, constant-return functions, and raise-only functions do not count. Data, documentation, package markers, HTML, CSS, and JavaScript do not contribute to the Python total. This script documents the repository's counting rule; a separate evaluator may use a different rule.

