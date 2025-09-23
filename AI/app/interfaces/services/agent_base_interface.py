from typing import Any, Optional, Protocol


class AgentBaseInterface(Protocol):
    """Interface defining the contract for agents"""

    def chat(
        self,
        prompt: str,
        temperature: float = 0.2,
        tools: Optional[Any] = None,
        output_json: Optional[Any] = None,
        output_pydantic: Optional[Any] = None,
        reasoning_steps: bool = False,
        stream: bool = True,
    ) -> str:
        """
        Send a message to the agent and get a response.

        Args:
            prompt: The message to send to the agent
            temperature: Controls randomness in the response
            tools: Optional tools for the agent
            output_json: Optional JSON output format
            output_pydantic: Optional Pydantic model output
            reasoning_steps: Whether to include reasoning steps
            stream: Whether to stream the response

        Returns:
            str: The response from the agent
        """
        raise NotImplementedError
