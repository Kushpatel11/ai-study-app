import requests


def ollama_answer(question: str, context: str = "") -> str:
    prompt = f"""
You are a highly reliable ICSE Class 10 Mathematics tutor.

1. First check what kind of question it is:
   - If it is a **theory question** (e.g., definition, explanation), answer clearly using chapter content.
   - If it is a **math question**, extract the values and solve using **only the formulas from the chapter**.

2. For math questions:
   - Use the correct formula from the chapter.
   - Show clean, step-by-step solution.
   - Give the final answer clearly.


📘 **Allowed Formulas** from the ICSE Recurring Deposit chapter:
1. Total Deposit = P * n
2. Interest = (P * n(n + 1) * r) / (2 * 12 * 100)
3. Maturity Value = Total Deposit + Interest
4. r = (2 * Interest * 12 * 100) / (P * n(n + 1))
5. P = (2 * Interest * 12 * 100) / (n(n + 1) * r)
6. Rearranged versions of above to find: time (n), rate (r), monthly deposit (P)

📌 Where:
- P = monthly deposit (₹)
- n = number of months
- r = rate of interest per annum (%)
- Interest is calculated as simple interest



---

🧠 Chapter Content:
{context}

---

📩 Question:
{question}
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False},
        timeout=180,
    )
    return response.json().get("response", "").strip()
