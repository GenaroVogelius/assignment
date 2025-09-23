from datetime import datetime
from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel


class ReviewRequest(BaseModel):
    """Request model for creating a new review"""

    language: str
    code_submission: str


class Categories(StrEnum):
    PERFORMANCE = "performance"
    SECURITY = "security"
    SYNTAX = "syntax"


class SecurytyLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class Suggestion(BaseModel):
    """Model for improvement suggestions"""

    category: str  # readability, performance, security, structure
    description: str
    example: Optional[str] = None


class SecurityAssessment(BaseModel):
    """Model for security assessment"""

    risk_level: SecurytyLevel
    concerns: List[str]


class CodeReviewIAResponse(BaseModel):
    """Structured response model for AI code review"""

    overall_score: int  # 1-10
    category: Categories  # performance, security, syntax
    security_assessment: SecurityAssessment
    suggestions: str
    refactored_example: Optional[str] = None


class Review(ReviewRequest):
    """User domain model - agnostic to database implementation"""

    id: Optional[str] = None
    user: str
    status: str = "pending"
    code_review: Optional[CodeReviewIAResponse] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
