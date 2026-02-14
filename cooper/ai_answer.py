import ollama

SYSTEM_PROMPT = """
You are COOPER, a professional personal assistant.
Answer clearly and concisely.
"""

def answer_question(question: str) -> str:
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )
    return response["message"]["content"].strip()
