from dataclasses import dataclass

@dataclass
class UserCreated:
    user_id: str
    name: str
    email: str
    password_hash: str