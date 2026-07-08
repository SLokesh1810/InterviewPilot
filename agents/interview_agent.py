import json
import os
import random

from agents.llm_generator import llm_generation
from dotenv import load_dotenv

load_dotenv()

USE_LLM = os.getenv("USE_LLM", "False").lower() == "true"

def generate_question(
    position,
    experience_level,
    question_type,
    current_stage
):
    """
    Generate a single interview question.
    """

    if not USE_LLM:
        return (
            "<Dummy question generation>"
        )

    prompt = f"""
    You are a senior hiring manager.

    Position: {position}
    Experience Level: {experience_level}
    Interview Stage: {current_stage}
    Question Type: {question_type}

    Generate ONE interview question.
    Return ONLY valid JSON.

    Example:
    {{
        "question": "What is database normalization?"
    }}
    """

    try:
        response = llm_generation(
            prompt,
            temperature=0.7,
            max_output_tokens=200
        )

        response = json.loads(response)

        return response["question"]

    except Exception as e:
        print(f"Question Generation Error: {e}")

        return (
            "Can you tell me about yourself?"
        )

def follow_up_question(
    previous_question,
    previous_answer
):
    """
    Determine whether a follow-up is required.
    """
    if not USE_LLM:
        follow_up = random.randint(0, 1) == 0

        if follow_up:
            return {
                "follow_up": False,
                "question": None
            }
        else:
            return {
                "follow_up": True,
                "question": "<Dummy follow up Question>"
            }
    
    prompt = f"""
    You are a senior technical interviewer.

    Previous Question:
    {previous_question}

    Candidate Answer:
    {previous_answer}

    Determine if a follow-up question is needed.
    Return ONLY valid JSON.

    Example 1:
    {{
        "follow_up": True,
        "question": "Can you explain that in more detail?"
    }}

    Example 2:
    {{
        "follow_up": False,
        "question": None
    }}
    """

    try:
        response = llm_generation(
            prompt,
            temperature=0.6,
            max_output_tokens=150
        )

        response = json.loads(response)

        return {
            "follow_up":bool(response.get("follow_up",False)),
            "question": response.get("question")
        }

    except Exception as e:

        print(
            f"Follow-up Generation Error: {e}"
        )

        return {
            "follow_up": False,
            "question": None
        }