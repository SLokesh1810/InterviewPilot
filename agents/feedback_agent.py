import json
import os

from llm_generator import llm_generation
from dotenv import load_dotenv

load_dotenv()

USE_LLM = os.getenv("USE_LLM", "False").lower() == "true"

def generate_final_feedback(
    position,
    role,
    experience_level,
    report_data
):
    if not USE_LLM:
        return {
            "summary": "<Dummy feedback from agent>",
            "strengths": ["<Dummy strength>"],
            "weaknesses": ["<Dummy weakness>"],
            "areas_of_improvement": ["<Dummy improvements>"],
            "recommendation": "<Dummy recommendation>"
        }

    prompt = f"""
    You are an experienced technical interviewer.
    Candidate Information:
    Position: {position}
    Role: {role}
    Experience Level: {experience_level}

    Interview Report:
    {json.dumps(report_data, indent=2)}

    Analyze the report and generate professional interview feedback.

    Consider:
    - Communication skills
    - Technical understanding
    - Confidence
    - Clarity
    - Speaking habits
    - Missing technical concepts
    - Overall interview performance

    Return ONLY valid JSON.
    Example:
    {{
        "summary":
            "The candidate demonstrated strong communication and good technical understanding.",

        "strengths": [
            "Clear communication",
            "Good problem solving",
            "Strong technical fundamentals"
        ],

        "weaknesses": [
            "Occasional filler words",
            "Missed some advanced concepts"
        ],

        "areas_of_improvement": [
            "Database indexing",
            "System design",
            "Behavioral storytelling"
        ],

        "recommendation":
            "Recommended for further technical evaluation",
    }}
    """

    try:
        response = llm_generation(
            prompt=prompt,
            temperature=0.3,
            max_output_tokens=700
        )

        return json.loads(response)

    except Exception as e:
        print(
            f"Final Feedback Generation Error: {e}"
        )
        return {
            "summary": "Unable to generate feedback.",
            "strengths": [],
            "weaknesses": [],
            "areas_of_improvement": [],
            "recommendation": "Manual review required."
        }