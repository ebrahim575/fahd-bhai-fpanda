from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import sys
import os
from creds import OPENAI_API_KEY
import pandas as pd
from typing import List, Dict
import json
import re

# Add the parent directory to Python path to import creds
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=OPENAI_API_KEY)

class DataManager:
    def __init__(self):
        # Get the directory where main.py is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct path to CSV file
        csv_path = os.path.join(current_dir, 'Tech_Company_Financials.csv')
        # Read the CSV file
        self.current_data = pd.read_csv(csv_path)
        
    def format_output(self, text):
        # Split into lines and initialize formatted output
        lines = text.split('\n')
        formatted = []
        
        for line in lines:
            # Handle introduction (lines ending with colon)
            if ':' in line and line.strip().endswith(':'):
                formatted.append(f"\n{line.strip()}\n")
                continue
            
            # Handle bullet points or hyphens
            if line.strip().startswith('-') or line.strip().startswith('•'):
                formatted.append(f"  {line.strip()}")
                continue
            
            # Handle monetary values (containing $ symbol)
            if '$' in line:
                # Check if it's a calculation line (contains +, =, or other operators)
                if any(op in line for op in ['+', '=', '*', '/']):
                    formatted.append(f"\n{line.strip()}")
                else:
                    formatted.append(f"  {line.strip()}")
                continue
            
            # Handle regular text
            if line.strip():
                formatted.append(line.strip())
        
        return "\n".join(formatted)

    def get_data_context(self):
        raw_text = str(self.current_data.describe())
        return self.format_output(raw_text)

# Initialize data manager
data_manager = DataManager()

class GraphSpec(BaseModel):
    type: str
    x: str
    y: str
    title: str

class AnalysisResponse(BaseModel):
    response: str
    graphs: List[Dict]

SYSTEM_PROMPT = """You are a sophisticated Financial Planning & Analysis (FP&A) expert with a keen eye for data visualization.
When analyzing financial data, create elegant, executive-ready visualizations that follow modern design principles.
Format your response with:

1. A concise explanation of the strategic insights each visualization reveals
2. A JSON specification for the recommended graphs in this format:
{"graphs": [{"type": "bar|line", "x": "column_name", "y": "column_name", "title": "Clear Professional Title"}]}

Prioritize 2-3 high-impact visualizations that:
- Use a refined, minimalist aesthetic
- Highlight key financial trends and patterns
- Follow best practices for financial data presentation
- Are immediately interpretable by executives and stakeholders

Focus on creating polished, boardroom-ready visualizations that tell a compelling financial story."""

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(message: Message):
    try:
        data_context = data_manager.get_data_context()
        full_data = data_manager.current_data.to_string()
        columns = list(data_manager.current_data.columns)
        
        enhanced_prompt = f"""Available columns: {columns}
Data summary:
{data_context}
User question: {message.text}
Analyze the data and suggest visualizations."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": enhanced_prompt}
            ]
        )
        
        content = response.choices[0].message.content
        
        # Extract JSON graph specifications
        try:
            json_start = content.find('{"graphs":')
            if json_start != -1:
                json_str = content[json_start:]
                graphs = json.loads(json_str)
                analysis = content[:json_start].strip()
            else:
                graphs = {"graphs": []}
                analysis = content
                
            # Get data for graphs
            graph_data = data_manager.current_data.to_dict('records')
            
            return {
                "response": analysis,
                "graphs": graphs["graphs"],
                "data": graph_data
            }
        except json.JSONDecodeError:
            return {"response": content, "graphs": [], "data": []}
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"response": "Error processing request", "graphs": [], "data": []}

@app.post("/analyze")
async def analyze(message: Message):
    try:
        data_context = data_manager.get_data_context()
        columns = list(data_manager.current_data.columns)
        
        enhanced_prompt = f"""Available columns: {columns}

Data summary:
{data_context}

User question: {message.text}

Provide analysis and suggest relevant visualizations."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": enhanced_prompt}
            ]
        )
        
        content = response.choices[0].message.content
        
        # Extract JSON graph specifications
        try:
            json_start = content.find('{"graphs":')
            if json_start != -1:
                json_str = content[json_start:]
                graphs = json.loads(json_str)
                analysis = content[:json_start].strip()
            else:
                graphs = {"graphs": []}
                analysis = content
        except json.JSONDecodeError:
            graphs = {"graphs": []}
            analysis = content
            
        return AnalysisResponse(response=analysis, graphs=graphs["graphs"])
    except Exception as e:
        print(f"Error: {str(e)}")
        return AnalysisResponse(response="Error processing request", graphs=[])

def extract_json_from_response(content: str) -> dict:
    # Find all JSON-like structures in the content
    json_pattern = r'\{[\s\S]*?"graphs"[\s\S]*?\}'
    matches = re.finditer(json_pattern, content)
    
    for match in matches:
        try:
            json_str = match.group()
            parsed = json.loads(json_str)
            if parsed.get("graphs"):
                return parsed
        except json.JSONDecodeError:
            continue
    
    return {"graphs": []}

@app.get("/initial-graphs")
async def get_initial_graphs():
    data = [
        {"Category": "Revenue", "Subcategory": "Product Sales", "Amount (USD)": 50000000},
        {"Category": "Revenue", "Subcategory": "Subscription Revenue", "Amount (USD)": 20000000},
        # ... rest of your data array ...
    ]
    
    graphs = [
        {
            "id": "revenue_chart",
            "type": "bar",
            "title": "Revenue Breakdown",
            "dataFilter": {"Category": "Revenue"},
            "xAxis": "Subcategory",
            "yAxis": "Amount (USD)",
            "layout": {
                "width": 600,
                "height": 400,
                "margin": {"t": 50, "b": 50, "l": 50, "r": 50}
            }
        },
        {
            "id": "expenses_chart",
            "type": "pie",
            "title": "Operating Expenses",
            "dataFilter": {"Category": "Operating Expenses"},
            "values": "Amount (USD)",
            "labels": "Subcategory",
            "layout": {
                "width": 600,
                "height": 400,
                "margin": {"t": 50, "b": 50, "l": 50, "r": 50}
            }
        }
    ]
    
    print("DEBUG: Sending response:", {"graphs": graphs, "data": data})
    return {"graphs": graphs, "data": data} 