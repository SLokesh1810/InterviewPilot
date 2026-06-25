import json

from agents.llm_generator import llm_generation

def generate_question(
    position,
    experience_level,
    question_type,
    current_stage
):
    """
    Generate a single interview question.
    """

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


def scoring_system(
    technical_scores,
    communication_scores
):
    """
    Calculate overall interview score.

    Both inputs should contain values
    between 0 and 10.
    """

    technical_avg = (
        sum(technical_scores)
        / len(technical_scores)
        if technical_scores
        else 0
    )

    communication_avg = (
        sum(communication_scores)
        / len(communication_scores)
        if communication_scores
        else 0
    )

    overall_score = (
        technical_avg * 0.6
        +
        communication_avg * 0.4
    ) * 10

    return {
        "overall_score":
            round(overall_score, 2),

        "technical_score":
            round(technical_avg, 2),

        "communication_score":
            round(
                communication_avg,
                2
            )
    }