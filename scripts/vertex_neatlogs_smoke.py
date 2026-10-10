"""One-shot real Vertex AI -> Neatlogs connectivity check. NOT a product agent.

Run only after reading docs/vertex-neatlogs-smoke.md. No credentials in code.
Uses an explicitly isolated billing project; safe synthetic prompt only.
"""
import os
import sys


def main() -> int:
    if not os.environ.get("NEATLOGS_API_KEY"):
        print("ERROR: Set NEATLOGS_API_KEY privately in this shell, not in Git.", file=sys.stderr)
        return 2

    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "matchday-pulse")
    if project != "matchday-pulse":
        print("ERROR: expected explicitly tested billing project matchday-pulse; review before changing.", file=sys.stderr)
        return 2

    import neatlogs

    # Important: initialize before constructing the google-genai client.
    neatlogs.init(
        api_key=os.environ["NEATLOGS_API_KEY"],
        endpoint="https://ingest.neatlogs.com",
        workflow_name="vertex-connectivity-check",
    )
    try:
        from google import genai
        from google.genai import types

        # ADC from Google Cloud Shell; NO Google API key/JSON credential is stored.
        client = neatlogs.wrap(
            genai.Client(
                vertexai=True,
                project=project,
                location="global",
                http_options=types.HttpOptions(api_version="v1"),
            )
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                "Reply with exactly: Vertex Gemini connectivity confirmed. "
                "This is a synthetic non-sensitive infrastructure test."
            ),
            config=types.GenerateContentConfig(
                max_output_tokens=128,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )
        print("Text:", response.text or "(empty response)")
        print("Finish reason:", getattr(response.candidates[0], "finish_reason", "unknown") if response.candidates else "no candidates")
        if response.usage_metadata:
            print("Usage:", response.usage_metadata.model_dump(exclude_none=True))
        return 0 if response.text else 1
    finally:
        # Required for short-lived scripts: avoid silently losing buffered spans.
        neatlogs.flush()
        neatlogs.shutdown()


if __name__ == "__main__":
    sys.exit(main())
