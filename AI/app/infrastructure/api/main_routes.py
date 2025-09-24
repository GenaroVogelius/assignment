import csv
import io
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Path, Query, Request, Response

from app.config.settings import Settings
from app.core.models.review import Review, ReviewRequest
from app.core.models.user import User
from app.infrastructure.api.auth_routes import AuthRoutes
from app.infrastructure.db.mongo.mongo_repository import MongoReviewRepository
from app.infrastructure.dependencies import get_review_repository, limiter
from app.infrastructure.jobs.tasks import IATasks
from app.interfaces.repositories.review_repository_interface import (
    ReviewRepositoryInterface,
)
from app.use_cases.review_use_case import ReviewUseCase


class MainRoutes:
    def __init__(self):
        self.router = APIRouter()
        self.settings = Settings()

        # implementations
        self.review_repository = MongoReviewRepository()

        # use cases
        self.review_use_case = ReviewUseCase(self.review_repository)
        self.ia_tasks = IATasks(self.review_repository)
        self.auth_routes = AuthRoutes()

        self._setup_routes()

    def _setup_routes(self):
        @self.router.get("/")
        async def root():
            """Root endpoint - Public access"""
            return {
                "message": f"Welcome to {self.settings.APP_NAME}",
                "version": self.settings.VERSION,
                "status": "running",
                "docs": "/docs",
                "health": f"{self.settings.API_PREFIX}/health",
                "auth": f"{self.settings.API_PREFIX}/auth/login",
            }

        @self.router.get("/health")
        async def health_check():
            """Health check endpoint - Public access"""
            return {
                "status": "healthy",
                "service": self.settings.APP_NAME,
                "version": self.settings.VERSION,
            }

        @self.router.get("/reviews")
        async def get_reviews(
            request: Request,
            current_user: User = Depends(
                self.auth_routes.get_current_active_user_dependency
            ),
            language: Optional[str] = Query(
                None, description="Filter by programming language"
            ),
            status: Optional[str] = Query(
                None,
                description="Filter by review status (pending, in_progress, completed, rejected)",
            ),
            score: Optional[int] = Query(
                None, ge=1, le=10, description="Filter by score (1-10)"
            ),
            csv: bool = Query(False, description="Return data in CSV format"),
        ):
            """Get reviews for authenticated user with optional filters - Protected endpoint - Requires authentication - Rate limited to 10 requests per hour per IP - Supports CSV export when csv=True"""

            language, status, score = self._clean_filters(language, status, score)

            # Get reviews with filters
            reviews: List[
                Review
            ] = await self.review_use_case.get_reviews_by_user_with_filters(
                user_id=str(current_user.id),
                language=language,
                status=status,
                score=score,
            )

            # Filter by score if provided (score is in code_review.overall_score)
            filtered_reviews = []
            for review in reviews:
                if score is not None:
                    # If score filter is provided, only include reviews with matching score
                    if review.code_review and hasattr(
                        review.code_review, "overall_score"
                    ):
                        overall_score = review.code_review.overall_score
                        if score == overall_score:
                            filtered_reviews.append(review)
                else:
                    # If no score filter, include all reviews
                    filtered_reviews.append(review)

            # Sort reviews by newest first (created_at descending)
            filtered_reviews.sort(key=lambda x: x.created_at, reverse=True)

            # Determine if any filters were applied
            filters_applied = {
                "language": language or "all",
                "status": status or "all",
                "score": score if score is not None else "all",
            }

            if csv:
                # Return CSV format
                csv_bytes = self._generate_csv_response(
                    filtered_reviews, current_user, filters_applied
                )
                return Response(
                    content=csv_bytes,
                    media_type="text/csv; charset=utf-8",
                    headers={
                        "Content-Disposition": f"attachment; filename=reviews_{current_user.username}.csv",
                        "Content-Type": "text/csv; charset=utf-8",
                    },
                )
            else:
                # Return JSON format
                return {
                    "message": f"Retrieved {len(filtered_reviews)} reviews for {current_user.username}",
                    "username": current_user.username,
                    "email": current_user.email,
                    "filters_applied": filters_applied,
                    "total_reviews": len(filtered_reviews),
                    "reviews": filtered_reviews,
                }

        @self.router.post("/reviews")
        @limiter.limit("10/hour")
        async def create_review(
            request: Request,
            review_request: ReviewRequest,
            background_tasks: BackgroundTasks,
            current_user: User = Depends(
                self.auth_routes.get_current_active_user_dependency
            ),
            review_repository: ReviewRepositoryInterface = Depends(
                get_review_repository
            ),
        ):
            """Create a new review - Protected endpoint - Requires authentication"""

            if not current_user.id:
                return {"message": "User not found", "error": "authentication_error"}

            # Create review with pending status
            review = Review(
                user=current_user.id,
                language=review_request.language,
                status="pending",
                code_submission=review_request.code_submission,
            )

            created_review = await self.review_use_case.create_review(review)

            if not created_review.id:
                return {"message": "Failed to create review", "error": "creation_error"}

            # Add background task to process review with AI agent
            background_tasks.add_task(
                self.ia_tasks.process_review_with_agent,
                created_review.id,
                review_request.code_submission,
                review_request.language,
            )

            return {
                "message": "Review created successfully",
                "review_id": created_review.id,
            }

        @self.router.get("/reviews/{review_id}")
        async def get_review_by_id(
            current_user: User = Depends(
                self.auth_routes.get_current_active_user_dependency
            ),
            review_id: str = Path(..., description="The ID of the review to get"),
        ):
            """Get a review by id - Protected endpoint - Requires authentication"""

            # Strip whitespace from review_id to handle URL encoding issues
            review_id = review_id.strip()

            review = await self.review_use_case.get_review_by_id(review_id)

            if not review:
                return {"message": "Review not found"}

            return {
                "message": "Review retrieved successfully",
                "id": review.id,
                "language": review.language,
                "code_submission": review.code_submission,
                "code_review": review.code_review,
                "status": review.status,
                "created_at": review.created_at,
                "updated_at": review.updated_at,
            }

    def _clean_filters(self, *args):
        """Clean the filters - converts 'all' values to None"""
        cleaned_args = []
        for value in args:
            if value == "all":
                cleaned_args.append(None)
            else:
                cleaned_args.append(value)
        return cleaned_args

    def _generate_csv_response(
        self, reviews: List[Review], user: User, filters_applied: dict
    ) -> bytes:
        """Generate CSV content from reviews data"""
        # Convert reviews to dictionaries
        dicts = [self._convert_review_to_dict(review) for review in reviews]

        # Define fieldnames (headers)
        fieldnames = [
            "Review ID",
            "Language",
            "Status",
            "Overall Score",
            "Category",
            "Security Risk Level",
            "Security Concerns",
            "Suggestions",
            "Code Submission",
            "Refactored Example",
            "Created At",
            "Updated At",
        ]

        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=fieldnames,
            delimiter=";",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\n",
        )

        writer.writeheader()
        writer.writerows(dicts)

        # Get the CSV content and encode it with UTF-8 BOM
        csv_content = output.getvalue()
        # Add UTF-8 BOM and encode to bytes
        csv_bytes = ("\ufeff" + csv_content).encode("utf-8")
        return csv_bytes

    def _convert_review_to_dict(self, review: Review) -> dict:
        """Convert a Review object to a dictionary for CSV export"""
        # Extract code review data safely
        overall_score = ""
        category = ""
        security_risk_level = ""
        security_concerns = ""
        suggestions = ""
        refactored_example = ""

        if review.code_review:
            overall_score = (
                str(review.code_review.overall_score)
                if review.code_review.overall_score is not None
                else ""
            )
            category = review.code_review.category or ""
            suggestions = review.code_review.suggestions or ""
            refactored_example = review.code_review.refactored_example or ""

            if review.code_review.security_assessment:
                security_risk_level = (
                    review.code_review.security_assessment.risk_level or ""
                )
                security_concerns = (
                    "; ".join(review.code_review.security_assessment.concerns)
                    if review.code_review.security_assessment.concerns
                    else ""
                )

        # Clean code submission for CSV (remove newlines and limit length)
        code_submission = (
            review.code_submission.replace("\n", " ").replace("\r", " ")[:500]
            if review.code_submission
            else ""
        )

        return {
            "Review ID": review.id or "",
            "Language": review.language or "",
            "Status": review.status or "",
            "Overall Score": overall_score,
            "Category": category,
            "Security Risk Level": security_risk_level,
            "Security Concerns": security_concerns,
            "Suggestions": suggestions.replace("\n", " ").replace("\r", " ")
            if suggestions
            else "",
            "Code Submission": code_submission,
            "Refactored Example": refactored_example.replace("\n", " ").replace(
                "\r", " "
            )
            if refactored_example
            else "",
            "Created At": review.created_at.isoformat() if review.created_at else "",
            "Updated At": review.updated_at.isoformat() if review.updated_at else "",
        }
