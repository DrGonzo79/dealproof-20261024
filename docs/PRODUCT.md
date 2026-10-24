# Product plan

## ICP and JTBD
Start with self-funded searchers evaluating $3M–$5M acquisition prices under time pressure. JTBD: “Before I sign an LOI, turn a promotional CIM number into a defendable lender scenario and tell me what evidence changes the decision.” The partner ICP is a lender/broker team that wants fewer dead LOIs.

## MVP
The prototype proves one vertical slice: choose a fictional deal, change price/equity, challenge addbacks, calculate normalized earnings/debt service/DSCR/max loan/equity gap, inspect risks, and stage a local memo. Production MVP adds secure CIM parsing, evidence citations, scenario history, expert review, and a PDF bridge. It explicitly does not provide a QoE, valuation, approval, or investment advice.

## Data model
`Deal` owns purchase/debt assumptions, reported earnings, concentration and `Adjustment[]`. Each `Adjustment` records seller claim, supported amount, replacement cost, evidence, reviewer, and provenance. `Scenario` versions assumptions/results. `Review` stores human disposition and rationale. `Event` captures model, rule, user override, and export for auditability.

## Technical architecture and AI strategy
Next.js App Router supplies the accessible workflow and static demo. FastAPI owns deterministic underwriting math with Pydantic validation. Production uses Postgres, encrypted object storage, a background parser, and append-only audit events. AI may extract candidate fields and cite exact pages; deterministic code calculates money and thresholds. Human reviewers approve mappings and risk language. Evaluate extraction precision/recall on a consented redacted set, measure calibration by adjustment type, and fall back to manual entry on low confidence.

## Economics
Beachhead: $0 screen → $99 reviewed report → $99–$149/mo searcher plan. Better business: $500–$2,000/mo lender/broker workspace. Report anchors suggest ~25K reachable community members, but the published 8% upload, 10% one-off, 3% subscription, seven-month tenure, and five partner assumptions are unvalidated. At $99, human review must stay under ~45 minutes to preserve margin. Do not underwrite a $3M–$6M ARR ceiling until retention and partner distribution exist.

## Validation and moat
Run the 20-person test in OFFICE_HOURS.md. The leading metric is completed real/redacted screens; conversion metrics are forward-to-lender intent and explicit $99 acceptance. The moat, if earned, is a reviewed corpus of addback decisions linked to evidence, industry, lender feedback, and final QoE outcomes, plus workflow integration. Parsing/UI alone has no moat.

## Risks
Wrong financial guidance, sensitive documents, false confidence, SBA rule drift, CPA/valuation boundary confusion, free competitors, selection bias, and low searcher close rate. Controls: disclaimer, provenance, human review, versioned rules, tenant isolation, retention limits, no autonomous lending decision, and third-party compliance review.

## 30 / 60 / 90 days
- **30:** 20 observations, 8 completed redacted screens, interview 3 SBA lenders, manually review every output, record explicit price decisions.
- **60:** if thresholds pass, secure upload + citations + review queue; 25 screens, 5 paid reports, 2 lender/broker design partners; measure false extraction and override rates.
- **90:** add versioned memo/PDF and partner intake; target 15 paid reports or 3 partner pilots with ≥40% monthly reuse. Otherwise pivot to a service-led lender intake product or stop.
