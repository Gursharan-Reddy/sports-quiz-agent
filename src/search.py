from ddgs import DDGS

def get_live_news_context(sport_name):
    search_query = f"{sport_name} latest tournament results championship winners news 2026"
    retrieved_texts = []

    try:
        with DDGS() as ddgs:
            results = ddgs.text(search_query, max_results=3)
            for index, r in enumerate(results, start=1):
                title = r.get("title", "No Title")
                snippet = r.get("body", "No Snippet Content Available")
                retrieved_texts.append(f"Source {index}: {title}\nSnippet: {snippet}")
    except Exception as e:
        return "No recent search engine updates available."

    return "\n\n".join(retrieved_texts)