from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Request(BaseModel):
    name: str
    type: str
    years: str = ""

@app.post("/generate")
def generate(req: Request):

    if req.type == "birthday":
        prompt = f"""
        Write a professional and warm birthday email for employee {req.name}.
        Keep it short and positive.
        """
    else:
        prompt = f"""
        Write a professional work anniversary email for employee {req.name}
        who completed {req.years} years in the company.
        Keep it formal but warm.
        """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    content = result["response"]

    return {
        "subject": f"Celebrating {req.name}! 🎉",
        "body": content.strip()
    }