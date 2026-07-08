from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    Form,
    File
)

from sqlalchemy.orm import Session

from database.db import get_db

from models.interview_models import User

from schemas.interview_schema import (
    StartInterviewRequest
)

from security.dependencies import (
    get_current_user
)

from orchestrator.orchestrator import (
    start_interview,
    submit_question,
    finish_interview
)

from services.interview_service import (
    get_interview,
    get_user_interviews,
    get_interview_by_id
)
from services.file_service import (
    save_audio_file
)

router = APIRouter()


@router.post("/start")
def start(
    request: StartInterviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    exists, interview = start_interview(
        db=db,
        user_id=current_user.id,
        position=request.position,
        experience=request.experience_level,
        role=request.role
    )

    if exists:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message':"You already have an active interview.",
                'interview_id': interview.id
            },
        )


    return {
        "success": True,
        "interview_id": interview.id,
        "question": interview.current_question
    }


@router.post("/submit-answer")
async def submit_answer(
    interview_id: int = Form(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    interview = get_interview(
        db,
        interview_id
    )

    if interview is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found."
        )

    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )
    
    audio_name = save_audio_file(
        audio=audio
    )

    details = await submit_question(
        db=db,
        interview_id=interview_id,
        audio_name=audio_name
    )

    if not details:
        {
            "success": True,
            "details": {
                "question_number": 13,
                "status": "completed",
                "completed": True
            }
        }

    return {
        "success": True,
        "details": details
    }


@router.post("/finish/{interview_id}")
def finish(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    interview = get_interview(
        db,
        interview_id
    )

    if interview is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found."
        )

    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    report = finish_interview(
        db=db,
        interview_id=interview_id
    )

    return {
        "success": True,
        "report": report
    }


@router.get("/status/{interview_id}")
def interview_status(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    interview = get_interview(
        db,
        interview_id
    )

    if interview is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found."
        )

    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    return {
        "status": interview.status,
        "question_count": interview.question_count,
        "remaining_time": interview.remaining_time
    }

@router.get("/history")
def user_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interviews = get_user_interviews(
        db,
        current_user.id
    )

    return {
        "interviews": [
            {
                "id": interview.id,
                "position": interview.position,
                "role": interview.role,
                "experience_level": interview.experience_level,
                "overall_score": interview.overall_score,
                "technical_score": interview.technical_score,
                "communication_score": interview.communication_score,
                "created_at": interview.created_at,
            }
            for interview in interviews
        ]
    }

@router.get("/history/{interview_id}")
def interview_details(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interview = get_interview_by_id(
        db,
        current_user.id,
        interview_id
    )

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    return {
        "id": interview.id,
        "position": interview.position,
        "role": interview.role,
        "experience_level": interview.experience_level,
        "overall_score": interview.overall_score,
        "technical_score": interview.technical_score,
        "communication_score": interview.communication_score,
        "report": interview.report,
        "created_at": interview.created_at
    }