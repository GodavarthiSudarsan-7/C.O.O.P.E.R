import json
from cooper.ai_answer import ai_client

SYSTEM_PROMPT = """
You are COOPER's planning engine.

Convert the user's request into a JSON list of steps.

Each step must have:
- action: one of [
  open_website,
  open_application,
  google_search,
  youtube_search,
  youtube_play,
  write_text
]
- target: string or null

Rules:
- If user asks to search Google, use google_search with the query
- If user asks to play music or a song on YouTube, use youtube_search with the song name
- If user just says open YouTube, use youtube_play
- Return ONLY valid JSON
- Do not explain anything
"""

def plan_steps(user_input: str):
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        temperature=0
    )

    text = response.choices[0].message.content.strip()
    return json.loads(text)
