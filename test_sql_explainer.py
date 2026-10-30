from src.ai.sql_explainer import explain_sql_result


question = "Which customer generated the highest revenue?"

sql_result = """
customer_name | city | total_revenue
Kiara | Pune | 2055531.91
"""


answer = explain_sql_result(
    question,
    sql_result
)


print("\nQuestion:")
print(question)

print("\nSQL Result:")
print(sql_result)

print("\nAI Explanation:")
print(answer)