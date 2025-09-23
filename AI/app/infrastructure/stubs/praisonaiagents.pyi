from typing import Any, Optional

class Agent:
    def __init__(
        self,
        instructions: str,
        llm: dict,
        self_reflect: bool = True,
        verbose: bool = True,
    ) -> None: ...
    def chat(
        self,
        prompt: str,
        temperature: float = 0.2,
        tools: Optional[Any] = None,
        output_json: Optional[Any] = None,
        output_pydantic: Optional[Any] = None,
        reasoning_steps: bool = False,
        stream: bool = True,
    ) -> str: ...

# Los stubs son útiles cuando:
# Trabajas con bibliotecas que no tienen tipos
# Quieres definir tipos para código externo
# Necesitas que el verificador de tipos entienda mejor tu código
# Es como una "documentación de tipos" que ayuda a mypy a verificar que estás usando la biblioteca correctamente.