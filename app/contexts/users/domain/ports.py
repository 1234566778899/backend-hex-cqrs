from abc import ABC, abstractmethod
from typing import Optional
from .entities import User


class IUserWriteRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        ...

class IUserReadRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[dict]:
        """Devuelve dict proyección de lectura o None"""
        ...