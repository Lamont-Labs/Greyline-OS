# Runbook — Greyline OS Demo Operations

## Roles
- Author/Owner: Jesse J. Lamont
- Reviewer: Demo Evaluator or Investor

## Commands
| Task | Command |
|------|----------|
| Validate | `make validate` |
| Render   | `make render` |
| Verify   | `make verify` |

## GitHub Upload Steps
1. Create empty repo on GitHub (e.g. `Greyline-OS`).
2. Add remote: `git remote add origin ...`
3. Push these demo files.
4. CI workflow runs automatically on `main`.

## Rollback Plan
If a demo render fails:
```bash
git checkout HEAD~1
make demo
