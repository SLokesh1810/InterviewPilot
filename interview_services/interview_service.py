from datetime import datetime

from database.interview_models import (
    ActiveInterview,
    InterviewReport
)

from report_service import final_score_update

def check_user_in_db(
        db,
        user_id
):
    return (
        db.query(ActiveInterview)
        .filter(
            ActiveInterview.user_id == user_id
        ).first()
    )

def create_interview(
    db,
    user_id,
    position,
    experience_level,
    difficulty_level=None,
    time_duration=1800
):
    
    active = check_user_in_db(
        db,
        user_id
    )
    
    if active:
        return None

    interview = ActiveInterview(
        user_id=user_id,
        position=position,
        experience_level=experience_level,
        difficulty_level=difficulty_level,
        remaining_time=time_duration,
        current_question=' '
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    return interview


def get_interview(
    db,
    interview_id
):
    return (
        db.query(ActiveInterview)
        .filter(
            ActiveInterview.id == interview_id
        )
        .first()
    )


def update_current_question(
    db,
    interview_id,
    question
):
    interview = get_interview(
        db,
        interview_id
    )

    if not interview:
        return None

    interview.current_question = question
    db.commit()
    db.refresh(interview)

    return interview


def save_response(
    db,
    interview_id,
    question,
    transcript,
    technical_evaluation,
    communication_score,
    audio_path=None
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

    history.append(
        {
            "question": question,
            "answer": transcript,
            "audio_path": audio_path,
            "technical_score":
                technical_evaluation[
                    "score"
                ],
            "technical_feedback":
                technical_evaluation[
                    "feedback"
                ],
            "missing_concepts":
                technical_evaluation[
                    "missing_concepts"
                ],
            "communication_score":
                communication_score,
            "timestamp":
                datetime.utcnow()
                .isoformat()
        }
    )

    interview.interview_data = {
        "history": history
    }

    interview.question_count += 1
    db.commit()
    db.refresh(interview)

    return interview


def increment_question_switch(
    db,
    interview_id
):
    interview = get_interview(
        db,
        interview_id
    )

    if not interview:
        return None

    interview.question_switches += 1
    db.commit()
    db.refresh(interview)

    return interview


def update_status(
    db,
    interview_id
):
    interview = get_interview(
        db,
        interview_id
    )

    if not interview:
        return None

    q_count = (
        interview.question_count
    )

    if q_count < 2:
        status = "intro"

    elif q_count < 5:
        status = "basic technical"

    elif q_count < 8:
        status = "advanced technical"

    elif q_count < 10:
        status = "behavioural"

    else:
        status = "final"

    interview.status = status
    db.commit()
    db.refresh(interview)

    return interview


def update_remaining_time(
    db,
    interview_id,
    elapsed_seconds
):
    interview = get_interview(
        db,
        interview_id
    )

    if not interview:
        return None

    interview.remaining_time -= (
        elapsed_seconds
    )

    if interview.remaining_time < 0:
        interview.remaining_time = 0

    db.commit()
    db.refresh(interview)

    return (
        interview.remaining_time
    )


def is_interview_completed(
    db,
    interview_id
):
    interview = get_interview(
        db,
        interview_id
    )

    if not interview:
        return True

    if (
        interview.question_count >= 10
        or
        interview.remaining_time <= 0
    ):
        interview.status = (
            "completed"
        )

        db.commit()
        return True

    return False

def complete_interview(
    db,
    interview_id,
    report_json,
    scores
):
    interview = get_interview(
        db,
        interview_id
    )

    if not interview:
        return None

    ovr = scores["overall"]
    tech = scores["technical"]
    comm = scores["communication"]
    

    final_report = InterviewReport(
        user_id=interview.user_id,
        position=interview.position,
        experience_level=interview.experience_level,
        overall_score=ovr,
        technical_score=tech,
        communication_score=comm,
        report=report_json,
        interview_data=interview.interview_data
    )

    db.add(
        final_report
    )
    db.delete(
        interview
    )
    db.commit()

    return final_report