from src.llm.llm_service import ask_llm

response = ask_llm(
    "Reply with exactly these words and nothing else: Gemini connection successful."
)

print(response)