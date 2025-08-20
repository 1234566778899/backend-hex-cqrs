from dataclasses import dataclass
from .value_objects import UserId, Email, Name

@dataclass
class User:
    id: UserId
    name: Name
    email: Email
    password_hash: str