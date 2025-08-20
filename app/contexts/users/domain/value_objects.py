from dataclasses import dataclass
import re

@dataclass(frozen=True)
class UserId:
    value: str
    def __post_init__(self):
        if not self.value or len(self.value) < 10:
            raise ValueError("UserId inválido")

@dataclass(frozen=True)
class Email:
    value: str
    def __post_init__(self):
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, self.value):
            raise ValueError("Email inválido")

@dataclass(frozen=True)
class Name:
    value: str
    def __post_init__(self):
        if not self.value or len(self.value.strip()) < 2:
            raise ValueError("Nombre inválido")