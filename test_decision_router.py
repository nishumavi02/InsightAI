from src.ai.decision_router import (
    route_question,
)


questions = [

    "What is total revenue?",

    "Which customer generated the highest revenue?",

    "How many paid leave days does an employee receive?",

    "What is the company leave policy?",

]


for question in questions:

    route = route_question(
        question
    )

    print(
        f"\nQuestion: {question}"
    )

    print(
        f"Route: {route}"
    )