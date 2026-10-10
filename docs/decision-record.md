# Decision Record — QUАLIFY → DECIDE (2026-10-10)

**Status: RESEARCH. No Concept Lock.** Keep options open and kill weak positioning early.

## Competitive novelty

**KILL** the broad name/claim "Integration Recovery Desk" as differentiated thesis. Boomi already documents AI investigation, auto-remediation, rerun and terminal-state verification for failing data flows. Workato exposes job retries; Sentry Seer and incident.io also tackle investigation and remediation. The local recovery kernel remains useful as a technical probe, not a standalone product.

Relevant prior-art links:
- https://developer.boomi.com/docs/APIs/DataIntegration/Usecases/Investigate_failed_dataflow_agent_usecase
- https://help.boomi.com/docs/Atomsphere/Data_Integration/Support/ai-troubleshooting-agent
- https://www.workato.com/product-hub/product-scoop-february-2026/
- https://incident.io/resolve-incidents-while-you-sleep
- https://docs.sentry.io/product/ai-in-sentry/seer

These sources show feature overlap, not complete coverage of the 2026 market.

## Narrower candidates (not selected)

**Promise Recovery:** a failed order/customer-service handoff produces an unsatisfied obligation; reconcile downstream outcome, prevent duplicate fulfillment, escalate ambiguity, and keep operator/customer informed.

**Change Aftercare:** after a software release damages a customer-visible transaction flow, detect missed authorized work, propose reversible remediation, replay once, and verify authoritative downstream transaction records.

**Access/Entitlement Recovery:** detect failed paid-service provisioning, compare entitlements with system of record, and safely repair permitted mismatches. Higher risk for payment/authorization correctness.

## Prioritized unknowns

Who is the urgent buyer and operator? What concrete obligation is broken, and which authoritative external service can we safely write to during the event? Is an AI decision actually necessary? Which competitors already close the same loop? How will we provide real receipts and reliable refusal/recovery behavior?

## Pre-build kill conditions

- No lawful, scoped, disposable external writable integration obtainable in time
- No independently readable authoritative outcome
- Problem indistinguishable from existing tools after niche-specific comparison
- Only static story, fake API, seeded data, or proof-first demo available
- Operators unable to complete real task without the developer

## Next gate

Obtain the five external model reviews (Claude, Gemini, Grok, Kimi, Perplexity), verify cited claims, compare alternatives, run an external write + read-back and model decision probe. Proceed/PIVOT/KILL **before** Concept Lock.
