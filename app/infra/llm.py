from langchain_google_genai.chat_models import ChatGoogleGenerativeAI


def get_gemini_llm(api_key: str) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=1,
        max_output_tokens=7000,
        google_api_key=api_key,
        thinking_budget=0,
    )