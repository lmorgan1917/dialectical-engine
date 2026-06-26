from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Use the free model
model = genai.GenerativeModel("gemini-2.0-flash-lite")

class QueryRequest(BaseModel):
    topic: str

@app.post("/generate")
def generate(request: QueryRequest):
    topic = request.topic
    
    # Thesis
    thesis_response = model.generate_content(
        f"Write a well-cited academic thesis arguing FOR: {topic}. Cite 2-3 credible sources with authors and dates."
    )
    thesis = thesis_response.text
    
    # Antithesis
    antithesis_response = model.generate_content(
        f"Write a well-cited academic antithesis arguing AGAINST: {topic}. Cite 2-3 credible sources with authors and dates."
    )
    antithesis = antithesis_response.text
    
    # Synthesis
    synthesis_response = model.generate_content(
        f"Synthesize these two views into a balanced academic conclusion:\n\nThesis:\n{thesis}\n\nAntithesis:\n{antithesis}"
    )
    synthesis = synthesis_response.text
    
    return {
        "thesis": thesis,
        "antithesis": antithesis,
        "synthesis": synthesis
    }
    }
