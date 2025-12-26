import json
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
You are an intent parser for a voice assistant called COOPER.

Your task:
- Read the user command
- Decide the intent
- Output ONLY valid JSON

Allowed actions:
1. open_website
2. open_application
3. unknown

JSON format:
{
  "action": "<action_name>",
  "target": "<target_value>"
}
"""


def ai_intent(command: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": command}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except Exception:
        return {"action": "unknown", "target": None}
