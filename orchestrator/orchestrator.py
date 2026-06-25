
import asyncio

from interview_services.interview_service import(
    create_interview,
    update_current_question,
    update_status,
    get_interview,
    is_interview_completed,
    save_response,
    increment_question_switch,
    increment_question_count,
    complete_interview

)
from interview_services.audio_service import(
    retrieve_transcript,
    analyse_transcript
)
from interview_services.report_service import(
    update_report,
    final_score_update
)

from agents.interview_agent import (
    generate_question,
    follow_up_question
)
from agents.evaluation_agent import (
    answer_evaluation
)

def start_interview(
    db,
    user_id,
    position,
    experience,
    difficulty
):
    interview = create_interview(
        db=db,
        user_id=user_id,
        position=position,
        experience=experience,
        difficulty=difficulty
    )
    
    if interview == None:
        return None

    question = generate_question(
        position=position,
        difficulty=difficulty,
        current_stage=interview.status,
        question_type=interview.status
    )
    
    interview = update_current_question(
        db=db,
        interview_id=interview.id,
        question=question
    )

    return interview

async def next_question_generation(
    db,
    interview,
    answer
):
    
    follow_up = follow_up_question(
        previous_answer=answer,
        previous_question=interview.question
    )

    if follow_up['follow_up']:
        return follow_up['question']
    
    interview = increment_question_switch(
        db=db,
        interview_id=interview.id
    )

    interview = update_status(
        db=db,
        interview_id=interview.id
    )

    if is_interview_completed(
        db=db,
        interview_id=interview.id
    ):
        finalize_report()  
        
    
    nxt_question = generate_question(
        position=interview.position,
        experience_level=interview.experience_level,
        question_type=interview.status,
        current_stage=interview.status
    )
    
    return nxt_question
    

async def update_question(
    db,
    interview_id,
    audio_name
):
    interview = increment_question_count(
        db=db,
        interview_id=interview_id
    )

    current_question = interview.question
    
    transcript_details = retrieve_transcript(
        audio_filename=audio_name
    )

    question = await next_question_generation(
        db=db,
        question=interview.current_question,
        answer=transcript_details['transcript']
    )

    analysis_report = await analyse_transcript(
        transcript=transcript_details['transcript'],
        audio_name=audio_name,
        audio_duration_sec=transcript_details['audio_duration_sec'],
        pause_data=transcript_details['pause_data']
    )

    technical_score = answer_evaluation(
        question=current_question,
        answer=transcript_details['answer']
    )
    
    new_report = update_report(
        analyser_report=analysis_report,
        current_report=interview.report,
        technical_evaluation=technical_score
    )
    
    interview = save_response(
        interview_id=interview.id,
        question=current_question,
        transcript=transcript_details['transcript'],
        technical_evaluation=technical_score,
        communication_score=new_report['score']['communication'],
        report=new_report,
        audio_path=audio_name
    )

    return question

def finalize_report(
    db,
    interview_id
):
    interview = get_interview(
        interview_id=interview_id,
        db=db
    )

    report = final_score_update(
        report=interview.id,
        question_count=interview_id.question_count
    )

    final_report = complete_interview(
        db=db,
        interview_id=interview_id,
        report_json=report
    )

    return final_report