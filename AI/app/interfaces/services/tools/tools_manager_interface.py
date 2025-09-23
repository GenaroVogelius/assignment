from typing import Protocol

class ToolManagerInterface(Protocol):
    config: dict
    tools: dict

    def __init__(self, config: dict):
        self.config = config
        self.tools = {}
    
    def load_tools(self):
        """
        """
        raise NotImplementedError

    def load_tool(self, tool_name: str, tool_config: dict):
        """
        """
        raise NotImplementedError

    def execute_action(self, tool_name: str, action_name: str, **kwargs):
        """
        """
        raise NotImplementedError

    def get_all_actions_metadata(self):
        """
        """
        raise NotImplementedError