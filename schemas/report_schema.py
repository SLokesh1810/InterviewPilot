from pydantic import BaseModel


class InterviewHistoryResponse(BaseModel):
    id: int
    position: str
    role: str
    experience_level: str
    overall_score: float


class FullReportResponse(BaseModel):
    report: dict