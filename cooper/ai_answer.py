import ollama
from cooper.web_search import search_web

SYSTEM_PROMPT = """
You are COOPER, a professional personal assistant.
Answer clearly and concisely.
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

def answer_question(question: str) -> str:
    lower_question = question.lower()

    if any(word in lower_question for word in CURRENT_INFO_KEYWORDS):
        search_results = search_web(question)

        prompt = f"""
Answer the user's question using the web search results.

Question:
{question}

Web Results:
{search_results}
"""

        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"].strip()

    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )

    return response["message"]["content"].strip()