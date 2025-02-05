# app.py
from flask import Flask, render_template, request, jsonify
from dataclasses import dataclass, field
import openai
import json
from creds import open_api_key

app = Flask(__name__)
openai.api_key = open_api_key

@dataclass
class CompanyData:
    name: str = "Flyte AI"
    industry: str = "Technology"
    type: str = "SaaS"
    metrics: dict = field(default_factory=lambda: {
        "financial": {
            "revenue": {
                "2023": {
                    "Q1": 2500000,
                    "Q2": 3100000,
                    "Q3": 4200000,
                    "Q4": 5000000
                },
                "growth_rate": 0.35
            },
            "burn_rate": 800000,
            "runway_months": 24,
            "customer_acquisition_cost": 1200,
            "lifetime_value": 45000
        },
        "product": {
            "active_users": 50000,
            "churn_rate": 0.02,
            "nps_score": 72
        },
        "department_costs": {
            "Engineering": 2500000,
            "Marketing": 1200000,
            "Sales": 1500000,
            "Operations": 800000
        }
    })

    def to_prompt(self) -> str:
        return f"""You are a financial analysis assistant for {self.name}, a {self.industry} company.
Consider these metrics:
- Revenue Q4 2023: ${self.metrics['financial']['revenue']['2023']['Q4']:,}
- Growth Rate: {self.metrics['financial']['revenue']['growth_rate']*100}%
- Burn Rate: ${self.metrics['financial']['burn_rate']:,}/month
- Runway: {self.metrics['financial']['runway_months']} months
- Department Costs: {', '.join(f'{k}: ${v:,}' for k, v in self.metrics['department_costs'].items())}

Provide clear, actionable insights about financial metrics while considering the company type and industry context."""

# Initialize with default data
company_data = CompanyData()

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
                {"role": "system", "content": company_data.to_prompt()},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_data', methods=['POST'])
def upload_data():
    try:
        file_data = request.json
        global company_data
        
        # Update company data from uploaded file
        company_data = CompanyData(
            name=file_data.get('company', {}).get('name', company_data.name),
            industry=file_data.get('company', {}).get('industry', company_data.industry),
            type=file_data.get('company', {}).get('type', company_data.type),
            metrics=file_data.get('company', {}).get('metrics', company_data.metrics)
        )
        
        # Return initial metrics and suggested charts
        return jsonify({
            "status": "success",
            "metrics": company_data.metrics,
            "suggested_charts": suggest_charts(company_data.industry)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_metrics', methods=['GET'])
def get_metrics():
    try:
        return jsonify({
            "metrics": company_data.metrics,
            "suggested_charts": suggest_charts(company_data.industry)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def suggest_charts(industry):
    """Suggest appropriate charts based on industry"""
    industry_charts = {
        "Technology": [
            {
                "type": "area",
                "metric": "revenue",
                "title": "Quarterly Revenue Growth",
                "data": list(company_data.metrics['financial']['revenue']['2023'].values())
            },
            {
                "type": "pie",
                "metric": "department_costs",
                "title": "Department Cost Distribution",
                "data": company_data.metrics['department_costs']
            },
            {
                "type": "bar",
                "metric": "unit_economics",
                "title": "Unit Economics",
                "data": {
                    "CAC": company_data.metrics['financial']['customer_acquisition_cost'],
                    "LTV": company_data.metrics['financial']['lifetime_value']
                }
            }
        ],
        # Add more industry-specific chart suggestions here
    }
    
    return industry_charts.get(industry, [])

if __name__ == '__main__':
    app.run(debug=True)