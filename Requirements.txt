from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class QueryRequest(BaseModel):
    topic: str

@app.post("/generate")
def generate(request: QueryRequest):
    topic = request.topic
    
    thesis = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Write a thesis arguing FOR: {topic}. Cite sources."}]
    )["choices"][0]["message"]["content"]
    
    antithesis = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Write an antithesis arguing AGAINST: {topic}. Cite sources."}]
    )["choices"][0]["message"]["content"]
    
    synthesis = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Synthesize:\nThesis:{thesis}\nAntithesis:{antithesis}"}]
    )["choices"][0]["message"]["content"]
    
    return {"thesis": thesis, "antithesis": antithesis, "synthesis": synthesis}
