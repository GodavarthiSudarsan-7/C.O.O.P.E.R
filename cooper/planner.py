from cooper.ai_answer import ai_client

SYSTEM_PROMPT = """
You are COOPER's planning engine.

Convert the user's request into a JSON list of steps.
Each step must have:
- action: one of [open_website, open_application, youtube_search, youtube_play, write_text]
- target: string or null

Only return valid JSON.
Do not explain.
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
    return eval(text)
