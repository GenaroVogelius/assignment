import json
from datetime import datetime

from app.config.settings import Settings
from app.core.enums import ConfigLLm
from app.core.models.review import CodeReviewIAResponse
from app.infrastructure.logger import logger
from app.infrastructure.services.praison_agent import PraisonAgent
from app.interfaces.repositories.review_repository_interface import (
    ReviewRepositoryInterface,
)
from app.use_cases.agent_simple_chat_use_case import AgentSimpleChatUseCase
from app.use_cases.review_use_case import ReviewUseCase


class IATasks:
    def __init__(self, review_repository: ReviewRepositoryInterface):
        self.settings = Settings()
        self.review_repository = review_repository
        self.review_use_case = ReviewUseCase(review_repository)

    async def process_review_with_agent(
        self,
        review_id: str,
        code_submission: str,
        language: str,
    ):
        """
        Background task to process review with AI agent and update the review

        Args:
            review_id: ID of the review to update
            code_submission: Code to be reviewed
            language: Programming language of the code
        """
        try:
            # Initialize agent and use case
            agent = PraisonAgent(
                instructions=self.settings.llm_config[ConfigLLm.INSTRUCTIONS].format(
                    language=language
                )
            )
            agent_use_case = AgentSimpleChatUseCase(agent)

            code_review_response = agent_use_case.execute(
                message=code_submission,
                output_pydantic=CodeReviewIAResponse,
                output_json=True,
            )
            # Get the existing review
            existing_review = await self.review_use_case.get_review_by_id(review_id)
            if not existing_review:
                logger.error(f"Review with id {review_id} not found")
                return

            # Parse JSON response and validate against Pydantic model
            try:
                # Check if code_review_response is None or empty
                if code_review_response is None:
                    raise ValueError("Agent response is None")

                if isinstance(code_review_response, str):
                    # Clean the response by removing markdown code blocks
                    cleaned_response = code_review_response.strip()

                    # Check if cleaned response is empty
                    if not cleaned_response:
                        raise ValueError("Agent response is empty after cleaning")

                    # Remove markdown code blocks (```json or ```)
                    if cleaned_response.startswith("```"):
                        # Find the first newline after the opening ```
                        first_newline = cleaned_response.find("\n")
                        if first_newline != -1:
                            # Remove everything before the first newline (including ```)
                            cleaned_response = cleaned_response[first_newline + 1 :]

                        # Remove closing ``` if present
                        if cleaned_response.endswith("```"):
                            cleaned_response = cleaned_response[:-3]

                        # Strip any remaining whitespace
                        cleaned_response = cleaned_response.strip()

                        # Check if response is empty after removing markdown
                        if not cleaned_response:
                            raise ValueError(
                                "Agent response is empty after removing markdown"
                            )

                    # Parse JSON string
                    json_data = json.loads(cleaned_response)
                else:
                    # Already a dict
                    json_data = code_review_response

                # Check if json_data is None or not a dict
                if json_data is None:
                    raise ValueError("Parsed JSON data is None")

                if not isinstance(json_data, dict):
                    raise ValueError(f"Expected dict, got {type(json_data)}")

                # Validate against Pydantic model
                validated_response = CodeReviewIAResponse(**json_data)
                code_review = validated_response
            except (json.JSONDecodeError, ValueError, TypeError) as e:
                # Fallback to storing as CodeReviewIAResponse
                code_review = None

            existing_review.code_review = code_review
            existing_review.status = "completed" if code_review else "rejected"
            existing_review.updated_at = datetime.utcnow()

            # Save updated review
            await self.review_use_case.update_review(existing_review)

            logger.info(f"Review {review_id} updated with AI review successfully")

        except Exception as e:
            logger.error(f"Error processing review {review_id}: {str(e)}")
