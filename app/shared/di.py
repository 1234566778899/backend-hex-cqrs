from typing import Any, Dict, Type

class Container:
    def __init__(self) -> None:
        self._registry: Dict[str, Any] = {}


    def register(self, key: str, factory: Any) -> None:
        self._registry[key] = factory


    def resolve(self, key: str) -> Any:
        if key not in self._registry:
            raise KeyError(f"Dependency not found: {key}")
        dep = self._registry[key]
        return dep() if callable(dep) else dep


container = Container()