from typing import Protocol

class RetrieverInterface(Protocol):
    def gen(self, *args, **kwargs):
        """
        Generate a response to a query.
        """
        raise NotImplementedError

    def search(self, *args, **kwargs):
        """
        Search in the vector db for relevant data.
        """
        raise NotImplementedError

    def get_params(self):
        """
        Get the parameters of the retriever.
        """
        raise NotImplementedError