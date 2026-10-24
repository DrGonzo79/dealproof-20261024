# DealProof

Runnable prototype for an evidence-linked, pre-LOI small-business acquisition stress test. It converts fictional CIM earnings into normalized earnings, debt service, DSCR, supported loan, equity gap, risks, and a go/renegotiate/walk call.

## Run
Requirements: Node 26.12.1 and `uv`.

```bash
npm ci
npm run typecheck
npm run test:e2e
npm run build
uv sync --project api --locked --dev
uv run --project api pytest api/tests
uv run --project api uvicorn api.main:app --reload
```

`POST /deals/stress-test` is a real deterministic domain operation with validation and failure tests. GitHub Pages deploys only the static frontend; the Python backend is tested source and is not publicly hosted.

## Safety
All fixtures and verdicts are fictional and simulated. This is educational software, not a QoE, valuation, credit decision, accounting opinion, or investment advice. See `research/notes.md` for derived source analysis and `docs/` for the product, architecture, review, score, and phased prompts.
