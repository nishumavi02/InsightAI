from src.ai.rag.answer_generator import (
    generate_rag_answer,
)


question = (
    "What is the company's stock market price?"
)


retrieved_chunks = [
    {
        "chunk": (
            "Employees are entitled to "
            "18 paid leave days per year."
        ),
        "score": 0.82,
    }
]


answer = generate_rag_answer(
    question,
    retrieved_chunks,
)


print("\n--- RAG ANSWER ---")
print(answer)