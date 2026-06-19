import json

from agents.llm_generator import llm_generation

from interview_services import (
    get_interview,
    calculate_scores
)

def generate_report(
    db,
    interview_id
):
    interview = get_interview(
        db,
        interview_id
    )

    if not interview:
        return None

    history = (
        interview.interview_data
        .get("history", [])
    )

    overall_score, technical_score, communication_score = (calculate_scores(interview))
    technical_feedback = []
    missing_concepts = []

    for item in history:
        if item.get("technical_feedback"):
            technical_feedback.append(
                item[
                    "technical_feedback"
                ]
            )

        missing_concepts.extend(
            item.get(
                "missing_concepts",
                []
            )
        )

    missing_concepts = list(
        set(missing_concepts)
    )

    prompt = f"""
    You are a senior hiring manager.

    Position:
    {interview.position}

    Experience Level:
    {interview.experience_level}

    Interview Metrics:

    Overall Score:
    {overall_score}

    Technical Score:
    {technical_score}

    Communication Score:
    {communication_score}

    Technical Feedback:
    {technical_feedback}

    Missing Concepts:
    {missing_concepts}

    Total Questions:
    {interview.question_count}

    Generate a professional interview report.

    Return ONLY valid JSON.

    Example:

    {{
        "summary":
            "Candidate performed well.",

        "strengths": [
            "SQL",
            "Communication"
        ],

        "weaknesses": [
            "System Design"
        ],

        "areas_of_improvement": [
            "Indexing",
            "Transactions"
        ],

        "recommendation":
            "Proceed to technical round"
    }}
    """

    try:

        response = llm_generation(
            prompt,
            temperature=0.3,
            max_output_tokens=600
        )

        report = json.loads(
            response
        )

        report[
            "overall_score"
        ] = overall_score

        report[
            "technical_score"
        ] = technical_score

        report[
            "communication_score"
        ] = communication_score

        return report

    except Exception as e:

        print(
            f"Report Generation Error: {e}"
        )

        return {
            "summary":
                "Report generation failed.",

            "strengths": [],

            "weaknesses": [],

            "areas_of_improvement":
                missing_concepts,

            "recommendation":
                "Manual review required",

            "overall_score":
                overall_score,

            "technical_score":
                technical_score,

            "communication_score":
                communication_score
        }