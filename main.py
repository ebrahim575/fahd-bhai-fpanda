# app.py
from flask import Flask, render_template, request, jsonify
from dataclasses import dataclass
import openai
from creds import open_api_key

app = Flask(__name__)
openai.api_key = open_api_key


@dataclass
class FPAConstraints:
    budget_limit: float = 1000000
    departments: list = None
    fiscal_year: str = "2024"
    currency: str = "USD"

    def to_prompt(self) -> str:
        return f"""You are a financial analysis assistant for a startup. 
Consider these constraints:
- Budget Limit: {self.budget_limit:,} {self.currency}
- Fiscal Year: {self.fiscal_year}
- Departments: {', '.join(self.departments) if self.departments else 'All'}

Provide clear, actionable insights about financial metrics while respecting these constraints."""


constraints = FPAConstraints(
    departments=["Engineering", "Marketing", "Sales", "Operations"],
    budget_limit=5000000
)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get('query')

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": constraints.to_prompt()},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update_constraints', methods=['POST'])
def update_constraints():
    data = request.json
    global constraints

    try:
        constraints = FPAConstraints(
            budget_limit=float(data.get('budget_limit', constraints.budget_limit)),
            departments=data.get('departments', constraints.departments),
            fiscal_year=data.get('fiscal_year', constraints.fiscal_year),
            currency=data.get('currency', constraints.currency)
        )
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)