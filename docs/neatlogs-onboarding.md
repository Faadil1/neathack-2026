# Neatlogs onboarding — 2026-10-10

**Status: PROJECT CREATED / FIRST TRACE WAITING / SDK NOT INSTALLED / AGENT NOT IMPLEMENTED.**

The neatlogs workspace signup/onboarding is complete through "send your first trace"; the page is waiting. The account-specific copied setup prompt supplied by the owner includes a **project ID** and an API-key **placeholder**, not a usable key. Do not publish an actual API key or paste it into GitHub, ChatGPT, or logs.

## Repository inventory (checked)

- `main`: README only.
- `research/technical-reality-2026-10-10`: `src/recovery.py` + six tests against a local HTTP/SQLite stand-in; **zero actual model calls or model-backed agent entry points**.
- Under the Neatlogs setup instructions, skip services that never make model/agent/tool calls. Therefore **do not artificially instrument the recovery spike or submit a fake trace** just to complete the setup wizard.

## Next eligible implementation task

Once a real application entry point with model calls exists:
1. Identify language, framework, LLM client, actual entry-point triggers and long-running vs one-shot lifetime.
2. Read the latest corresponding SDK instructions at https://docs.neatlogs.com/sdk/python (or TypeScript/Go as appropriate). Use its exact provider-specific wrapping vs instrumentations mechanism and ingestion endpoint `https://ingest.neatlogs.com`.
3. Set `NEATLOGS_API_KEY` privately in the process environment or ignored local `.env`, never in git.
4. Add **tracing only** for the actual model/tool actions. Initialize once per service and ensure flush/shutdown if one-shot.
5. Let the owner run the real agent with their own credentials and inspect the first visible dashboard trace. Verify spans, model/tool details and workflow attribution; never report a trace as observed without seeing it.

**Not done:** no SDK install, actual outbound trace, workflow trace ID, or evidence of partner compliance. Do not add alerts, detections, evaluations or unrelated runtime changes as part of this tracing-only step.

Workspace URL: https://app.neatlogs.com/
