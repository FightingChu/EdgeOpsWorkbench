# Case Authoring

## Workflow

1. Start from a clean tagged project revision.
2. Choose one primary mechanism and one credible product surface.
3. Define observable correct behavior before injecting a defect.
4. Write the verifier and confirm it passes on clean main.
5. Write setup and confirm the verifier fails for the intended reason.
6. Add public checks that reveal enough evidence without giving away the solution.
7. For multi-turn cases, put persistent constraints in the first round and verify them after the final round.
8. Run setup and verification twice in fresh disposable directories.

## Quality rules

- One primary failure mechanism per case.
- The product domain and scenario must be credible together.
- Misleading evidence may exist, but decisive counterevidence must be discoverable.
- A shallow workaround must fail a meaningful verifier check.
- Avoid flaky timing, public internet access, hidden machine state, and destructive setup.
- Record exact target-runtime differences when the case depends on them.

