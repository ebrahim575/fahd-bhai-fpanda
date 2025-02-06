from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import sys
import os

# Add the parent directory to Python path to import creds
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from creds import OPENAI_API_KEY

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

SYSTEM_PROMPT = """You are Claude, a helpful and enthusiastic AI assistant. You have a friendly personality and enjoy 
explaining complex topics in simple terms. You're knowledgeable about a wide range of subjects and always try to provide 
accurate, helpful responses while maintaining a conversational tone."""

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(message: Message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"response": "Sorry, I encountered an error processing your request."} 