from google import genai
from src.config import GEMINI_API_KEY
from src.database import query_historic_facts
from src.search import get_live_news_context

def compile_quiz_data(sport, difficulty):
    # 1. Gather Historical Context
    db_query = f"{sport} history cup championships rules records"
    db_matches = query_historic_facts(sport=sport, query_text=db_query, n_results=2)
    db_context = "\n".join(db_matches) if db_matches else "No offline historic data recorded."

    # 2. Gather Live Context
    web_context = get_live_news_context(sport)

    unified_context = f"=== HISTORICAL FACTS ===\n{db_context}\n\n=== LIVE INTERNET NEWS ===\n{web_context}"

    # 3. Build Prompt
    prompt = f"""
    You are an expert sports quiz creator. Write exactly 4-5 multiple-choice questions relying strictly on the Context below. Do not use outside facts.

    CONTEXT DETAILS:
    {unified_context}

    Task: Generate questions for {sport} at a {difficulty} difficulty level.

    Format exactly like this for each question:
    Question: [Question text]
    A) [Option A]
    B) [Option B]
    C) [Option C]
    D) [Option D]
    Correct Answer: [Single Letter]
    Explanation: [Detailed reasoning based on the context]
    ---
    """

    # 4. Generate Content via the new modern SDK client
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt,
    )

    return response.text, unified_context