from openai import OpenAI
import os

# ✅ Create OpenAI client (v2.x compatible)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # recommended
)

SYSTEM_PROMPT = """
You are COOPER, a professional personal assistant.
Answer the user's question clearly and concisely.
If it is a technical question, explain simply.
If it is general knowledge, be accurate.
Do NOT mention that you are an AI model.
"""


def answer_question(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()
