import ollama
from cooper.web_search import search_web

SYSTEM_PROMPT = """
You are COOPER, a professional personal assistant.

Rules:
- Answer clearly and concisely.
- Use memory context if provided.
- Prefer memory information when relevant.
- Do not mention that memory was used.
"""

CURRENT_INFO_KEYWORDS = [
    "latest",
    "today",
    "current",
    "recent",
    "yesterday",
    "news",
    "stock",
    "price",
    "tournament",
    "match",
    "winner"
]

def answer_question(question: str, memories=None) -> str:
    if memories is None:
        memories = []

    memory_context = "\n".join(memories)

    lower_question = question.lower()

    if any(word in lower_question for word in CURRENT_INFO_KEYWORDS):
        search_results = search_web(question)

        prompt = f"""
Memory Context:
{memory_context}

Question:
{question}

Web Results:
{search_results}

Answer the user's question using the memory context and web results.
"""

        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"].strip()

    prompt = f"""
Memory Context:
{memory_context}

Question:
{question}

Answer the question using the memory context if relevant.
"""

    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"].strip()