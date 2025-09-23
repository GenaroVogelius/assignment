from typing import Any, Optional

from app.interfaces.services.agent_base_interface import AgentBaseInterface


class AgentSimpleChatUseCase:
    """Use case for interacting with Agent."""

    def __init__(self, agent: AgentBaseInterface):
        """
        Initialize the use case

        Args:
            agent: An instance of AgentBaseInterface
        """
        self.agent = agent

    def execute(
        self,
        message: str,
        output_pydantic: Optional[Any] = None,
        output_json: Optional[bool] = None,
    ) -> Any:
        """
        Execute the use case

        Args:
            message: The message to send to the agent
            output_pydantic: Optional Pydantic model for structured output
            output_json: Optional boolean to request JSON output
        """
        return self.agent.chat(
            prompt=message, output_pydantic=output_pydantic, output_json=output_json
        )
