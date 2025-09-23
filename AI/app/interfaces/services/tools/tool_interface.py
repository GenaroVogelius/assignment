from typing import Protocol


class Tool(Protocol):
    
    def execute_action(self, action_name: str, **kwargs):
        """
        Execute an action on the tool.
        """
        raise NotImplementedError

    def get_actions_metadata(self):
        """
        Returns a list of JSON objects describing the actions supported by the tool.
        """
        raise NotImplementedError

    
    def get_config_requirements(self):
        """
        Returns a dictionary describing the configuration requirements for the tool.
        """
        raise NotImplementedError