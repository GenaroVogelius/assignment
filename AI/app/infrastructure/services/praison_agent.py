from pickle import FALSE
from typing import Any, Optional

from praisonaiagents import Agent

from app.config.settings import Settings
from app.core.enums import ConfigLLm
from app.interfaces.services.agent_base_interface import AgentBaseInterface


class PraisonAgent(AgentBaseInterface):
    def __init__(self, instructions: str = "You are a helpful AI assistant"):
        self.instructions = instructions
        self.settings = Settings()
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Create and configure the Praison agent with full LLM configuration"""
        
        llm_config = self.settings.llm_config

        # Create agent with basic configuration
        agent = Agent(
            instructions=self.instructions,
            llm=llm_config[ConfigLLm.MODEL],
            self_reflect=False,
            verbose=False,
            api_key=self.settings.llm_config[ConfigLLm.API_KEY],
            base_url=self.settings.llm_config[ConfigLLm.OPENAI_BASE_URL],
        )

        return agent

    def chat(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        tools: Optional[Any] = None,
        output_json: Optional[Any] = None,
        output_pydantic: Optional[Any] = None,
        reasoning_steps: bool = False,
        stream: bool = False,
    ) -> str:
        """
        Send a message to the agent and get a response.

        Args:
            prompt: The message to send to the agent
            temperature: Controls randomness in the response (overrides config if provided)
            tools: Optional tools for the agent
            output_json: Optional JSON output format
            output_pydantic: Optional Pydantic model output
            reasoning_steps: Whether to include reasoning steps
            stream: Whether to stream the response

        Returns:
            str: The response from the agent
        """
        # Use provided temperature or fall back to config

        return self.agent.chat(
            prompt,
            temperature,
            tools,
            output_json,
            output_pydantic,
            reasoning_steps,
            stream,
        )