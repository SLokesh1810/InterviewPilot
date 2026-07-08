from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )
    name = Column(
        String,
        nullable=False
    )
    email = Column(
        String,
        unique=True,
        nullable=False
    )
    hashed_password = Column(
        String,
        nullable=False
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

class ActiveInterview(Base):
    __tablename__ = "ongoing_interviews"

    id = Column(
        Integer,
        primary_key=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    position = Column(
        String,
        nullable=False
    )
    role = Column(
        String,
        nullable=False
    )
    experience_level = Column(
        String,
        nullable=False
    )
    status = Column(
        String,
        default="intro"
    )
    question_count = Column(
        Integer,
        default=0
    )
    question_switches = Column(
        Integer,
        default=0
    )
    remaining_time = Column(
        Integer,
        default=1800
    )
    current_question = Column(
        String
    )
    report_data = Column(
        MutableDict.as_mutable(JSONB),
        nullable=False,
        default=dict
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

class InterviewHistory(Base):
    __tablename__ = "interview_history"

    id = Column(
        Integer,
        primary_key=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    position = Column(
        String,
        nullable=False
    )
    role = Column(
        String,
        nullable=False
    )
    experience_level = Column(
        String,
        nullable=False
    )
    overall_score = Column(
        Float
    )
    technical_score = Column(
        Float
    )
    communication_score = Column(
        Float
    )
    report = Column(
        JSONB,
        nullable=False
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )