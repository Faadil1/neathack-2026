# Live Product Gate — BLOCKED

## Acceptable evidence

A functioning goal-directed model/agent chooses among constrained, auditable tools based on changing input. The authorized tool makes a real external write in a safe isolated environment. The product independently reads an authoritative downstream state and attributes a durable receipt to the corresponding business obligation. A real operator can review, approve, refuse, resume, and inspect the result.

## Required scenario progression

| Case | Required result | Current status |
|---|---|---|
| One success | external state change + source-of-truth read-back | NOT_IMPLEMENTED |
| Temporary 503 | bounded retry and idempotency | LOCAL_VERIFIED / LOCAL_STUB |
| 401 / 403 | refuse write and request authorization | LOCAL_VERIFIED 401 / LOCAL_STUB |
| Invalid schema | stop unsafe correction / escalate | LOCAL_VERIFIED 400 / LOCAL_STUB |
| 200 without downstream receipt | never mark as success | LOCAL_VERIFIED / LOCAL_STUB |
| Restart | durable resume without repeated delivery | LOCAL_VERIFIED / LOCAL_STUB |
| Forbidden model tool suggestion | deny and retain reason | NOT_IMPLEMENTED |
| Concurrent/repeated attempts | provider-level deduplication / proven recovery | NOT_IMPLEMENTED |
| Rollback / irreversible boundary | operator has truthful options | NOT_IMPLEMENTED |
| Independent user/judge clean-room | execute without developer | NOT_IMPLEMENTED |
| neatlogs spans/traces | actual agent and tool traces in account | NOT_IMPLEMENTED |
| Entire checkpoint | sanitized record linked to repo commit | NOT_IMPLEMENTED |
| cfo.ai plan | real pricing, cost and runway output | NOT_IMPLEMENTED |

## Post-slice product depth

First live success is an entry point, not Definition of Done. Continue failure/recovery, role permissions, uncertainty, observability, multiple business cases, durable operator UI, user onboarding, cost/economics, clean-room execution and repeated evaluations. Predeclare thresholds for AI/stochastic runs; one green trace does not prove reliability.

## Safety and confidentiality

Keep credentials server-side. Don't commit secrets or customer data; inspect Entire checkpoint contents before public sharing. Limit tools to least privilege; for ambiguous external responses, abstain and reconcile rather than blindly retry.
