# Architecture

The demo deliberately shares fixtures but not a runtime: `data/demo_deals.json` drives the static frontend; `lib/deal.ts` mirrors the deterministic FastAPI domain operation for Pages. `api/main.py` validates and computes the production-shaped operation; API integration tests cover success and failure. GitHub Pages hosts only the exported frontend.

```text
Next.js UI ──> typed local stress test ──> static export / GitHub Pages
     │
     └── shared fictional fixture semantics
FastAPI POST /deals/stress-test ──> validated earnings bridge + debt math
```

Security boundaries: no secrets or uploads in the demo; all data is fictional; no network calls. Production must separate tenants, encrypt CIMs, scan uploads, log provenance, minimize retention, and keep AI extraction outside deterministic calculations. Node is pinned to 26.12.1, Next to 16.4.3, certifi resolves to 2026.10.23, and Docker refreshes system CA certificates in every external-base stage.
