from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TAVILY_API_KEY")

print("API KEY FOUND:", API_KEY is not None)

client = TavilyClient(api_key=API_KEY)

def search_web(query: str):
    result = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    text = []

    for item in result.get("results", []):
        title = item.get("title", "")
        content = item.get("content", "")

        text.append(f"{title}\n{content}")

    return "\n\n".join(text)