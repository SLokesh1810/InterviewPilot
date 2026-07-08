import json
import os
import random

from .llm_generator import llm_generation
from dotenv import load_dotenv

load_dotenv()

USE_LLM = os.getenv("USE_LLM", "False").lower() == "true"

def answer_evaluation(question, answer):
    """
    Evaluate only technical content.
    Communication metrics will be handled
    by the speech analysis module.
    """

    if not USE_LLM:
        return {
            "score": random.randint(0, 10), 
            "missing_concepts": ['<Dummy concept>']
        }

    prompt = f"""
    You are a senior interviewer.
    Evaluate the answer below.

    Question:
    {question}

    Candidate Answer:
    {answer}

    Ignore:
    - Grammar
    - Pronunciation
    - Fluency
    - Confidence

    Evaluate only:
    - Technical Accuracy
    - Depth
    - Relevance

    Return ONLY valid JSON.
    Example:
    {{
        "score": 8,
        "missing_concepts": [
            "Clustered Index",
            "Non-Clustered Index"
        ]
    }}
    """

    try:
        response = llm_generation(
            prompt,
            temperature=0.3,
            max_output_tokens=250
        )

        response = json.loads(response)

        return {
            "score": int(response.get("score", 0)),
            "missing_concepts": response.get("missing_concepts", [])
        }

    except Exception as e:
        print(f"Answer Evaluation Error: {e}")
        return {
            "score": 0, 
            "missing_concepts": []
        }