from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# DeepSeek uses OpenAI-compatible API
openai.api_key = os.getenv("DEEPSEEK_API_KEY")
openai.api_base = "https://api.deepseek.com/v1"

app = FastAPI()

class QueryRequest(BaseModel):
    topic: str

@app.post("/generate")
def generate(request: QueryRequest):
    topic = request.topic
    
    # Thesis
    thesis = openai.ChatCompletion.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": f"Write a well-cited academic thesis arguing FOR: {topic}. Cite 2-3 credible sources."}]
    )["choices"][0]["message"]["content"]
    
    # Antithesis
    antithesis = openai.ChatCompletion.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": f"Write a well-cited academic antithesis arguing AGAINST: {topic}. Cite 2-3 credible sources."}]
    )["choices"][0]["message"]["content"]
    
    # Synthesis
    synthesis = openai.ChatCompletion.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": f"Synthesize these two views into a balanced academic conclusion:\n\nThesis:\n{thesis}\n\nAntithesis:\n{antithesis}"}]
    )["choices"][0]["message"]["content"]
    
    return {
        "thesis": thesis,
        "antithesis": antithesis,
        "synthesis": synthesis
    }
