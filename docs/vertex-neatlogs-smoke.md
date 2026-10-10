# First real Gemini → Neatlogs trace (infrastructure proof only)

Status: **NOT RUN**, Neatlogs dashboard trace not yet observed. No concept lock. This is one real Gemini call, not an agent or external business transaction.

Billing project: `matchday-pulse`, already demonstrated to serve Gemini 2.5 Flash via Vertex AI with HTTP 200 on 2026-10-10. The new Cloud project `neathack-2026` is not billed, so do NOT set it as the inference project. The Google AI Pro monthly credit balance applied to this billing account has **not been independently verified**.

Uses Neatlogs Python SDK wrapping `google-genai` in Vertex mode, ADC, private project key, explicit regional endpoint, and `flush()/shutdown()`. Source: https://docs.neatlogs.com/integrations/vertex-ai and https://docs.neatlogs.com/sdk/python .

## Cloud Shell instructions

Do **not** paste your Neatlogs key in this repo or into chat. In Google Cloud Shell:

```bash
git clone https://github.com/Faadil1/neathack-2026.git
cd neathack-2026
git fetch origin integration/gemini-neatlogs-first-trace
git checkout integration/gemini-neatlogs-first-trace

python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U "neatlogs[vertex-ai]" google-genai

export GOOGLE_CLOUD_PROJECT=matchday-pulse
export GOOGLE_CLOUD_LOCATION=global
export GOOGLE_GENAI_USE_VERTEXAI=True

# Enter key privately without showing it or storing it in shell history:
read -r -s -p "Neatlogs API key: " NEATLOGS_API_KEY; echo
export NEATLOGS_API_KEY

python scripts/vertex_neatlogs_smoke.py
```

If Python reports missing ADC credentials in Cloud Shell, investigate `google.auth.default()` and Cloud Shell auth; do not expose tokens or credential JSON. Google documents Cloud Shell as normally pre-authenticated for client library use.

Check https://app.neatlogs.com/ dashboard for a trace with workflow **vertex-connectivity-check**, Gemini model and usage. A printed script response does **not** prove telemetry delivery. Capture timestamp, trace link/ID, and presence or absence of LLM span, without secrets.

The model's earlier tiny truncated output ended `MAX_TOKENS` because default thinking used most of the token budget. This test disables thinking using the supported Gemini 2.5 Flash config (not an agent-design default).

## Evidence classification

- Gemini raw REST HTTP 200 with real token metadata: **LIVE MODEL ACCESS** verified on 2026-10-10 (user shared terminal output).
- This script: **SOURCE PREPARED / NOT_EXECUTED**.
- neatlogs first ingested trace: **UNVERIFIED** until dashboard proof.
- Live core product loop, agents, external write + readback: **NOT_IMPLEMENTED**.
- Partner Entire and cfo.ai: **NOT_CONNECTED**.

Never interpret an infrastructure smoke test as product completion. When Concept Lock finishes, instrument the actual tool/agent workflow with real business-state consequences and negative/recovery cases.
