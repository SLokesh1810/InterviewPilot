from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from database.db import get_db
from models.interview_models import InterviewHistory, User

from security.dependencies import get_current_user

router = APIRouter()


@router.get("/history")
def get_interview_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    interviews = (
        db.query(InterviewHistory)
        .filter(
            InterviewHistory.user_id == current_user.id
        )
        .order_by(
            InterviewHistory.created_at.desc()
        )
        .all()
    )

    return {
        "success": True,
        "count": len(interviews),
        "history": interviews
    }


@router.get("/history/{interview_id}")
def get_interview_report(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    interview = (
        db.query(InterviewHistory)
        .filter(
            InterviewHistory.id == interview_id,
            InterviewHistory.user_id == current_user.id
        )
        .first()
    )

    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found."
        )

    return {
        "success": True,
        "report": interview.report,
        "history": interview.history
    }


@router.delete("/history/{interview_id}")
def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    interview = (
        db.query(InterviewHistory)
        .filter(
            InterviewHistory.id == interview_id,
            InterviewHistory.user_id == current_user.id
        )
        .first()
    )

    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found."
        )

    db.delete(interview)
    db.commit()

    return {
        "success": True,
        "message": "Interview deleted successfully."
    }