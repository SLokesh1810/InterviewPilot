from services.interview_service import(
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
from services.file_service import(
    delete_audio_file
)
from services.audio_service import(
    retrieve_transcript,
    analyse_transcript
)
from services.report_service import(
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
    role
):
    exists, interview = create_interview(
        db=db,
        user_id=user_id,
        position=position,
        experience_level=experience,
        role=role
    )
    
    if exists:
        return True, interview

    question = generate_question(
        position=position,
        experience_level=experience,
        current_stage=interview.status,
        question_type=interview.status
    )
    
    interview = update_current_question(
        db=db,
        interview_id=interview.id,
        question=question
    )

    return False, interview

async def next_question_generation(
    db,
    interview,
    answer
):
    
    follow_up = follow_up_question(
        previous_answer=answer,
        previous_question=interview.current_question
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
        finish_interview(
            db=db,
            interview_id=interview.id
        )

        return None
        
    
    nxt_question = generate_question(
        position=interview.position,
        experience_level=interview.experience_level,
        question_type=interview.status,
        current_stage=interview.status
    )
    
    return nxt_question
    

async def submit_question(
    db,
    interview_id,
    audio_name
):
    interview = increment_question_count(
        db=db,
        interview_id=interview_id
    )

    current_question = interview.current_question
    
    try:
        transcript_details = retrieve_transcript(
            audio_name=audio_name
        )

        if transcript_details is None:
            return {
                "success": False,
                "message": "Unable to transcribe audio."
            }

        analysis_report = await analyse_transcript(
            audio_name=transcript_details['audio_path'],
            audio_duration_sec=transcript_details['audio_duration_sec'],
            pause_data=transcript_details['pause_data'],
            transcript=transcript_details['transcript']
        )

        technical_score = answer_evaluation(
            question=current_question,
            answer=transcript_details['transcript']
        )
        
        new_report = await update_report(
            analyser_report=analysis_report,
            current_report=interview.report_data,
            technical_evaluation=technical_score
        )
        
        interview = save_response(
            db=db,
            interview_id=interview.id,
            question=current_question,
            transcript=transcript_details['transcript'],
            technical_evaluation=technical_score,
            communication_score=new_report['score']['communication'],
            report=new_report,
            audio_path=transcript_details['audio_path']
        )

        question = await next_question_generation(
            db=db,
            interview=interview,
            answer=transcript_details['transcript']
        )
        
        delete_audio_file(transcript_details['audio_path'])

        return {
            "next_question": question,
            "question_number": interview.question_count,
            "status": interview.status,
            "remaining_time": interview.remaining_time,
            "completed": interview.status == "completed"
        }
    
    finally:
        delete_audio_file(audio_name)

def finish_interview(
    db,
    interview_id
):
    interview = get_interview(
        interview_id=interview_id,
        db=db
    )

    report = final_score_update(
        report=interview.report_data,
        question_count=interview.question_count
    )

    final_report = complete_interview(
        db=db,
        interview_id=interview_id,
        report_json=report
    )

    return report