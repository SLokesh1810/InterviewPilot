from pydantic import BaseModel, Field


class StartInterviewRequest(BaseModel):
    position: str = Field(..., min_length=2)
    role: str = Field(..., min_length=2)
    experience_level: str
    difficulty: str


class InterviewResponse(BaseModel):
    interview_id: int
    question: str

class ResumeInterviewResponse(BaseModel):
    interview_id: int
    question: str
    status: str
    remaining_time: int