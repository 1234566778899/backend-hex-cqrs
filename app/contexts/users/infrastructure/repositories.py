from typing import Optional
from sqlalchemy.orm import Session
from app.contexts.users.domain.entities import User
from app.contexts.users.domain.ports import IUserWriteRepository, IUserReadRepository
from .models import UserModel, UserReadModel

class UserWriteRepository(IUserWriteRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> None:
        m = UserModel(
        id=user.id.value,
        name=user.name.value,
        email=user.email.value,
        password_hash=user.password_hash,
        )
        self.session.add(m)

class UserReadRepository(IUserReadRepository):
    def __init__(self, session_factory):
        self._session_factory = session_factory
    def get_by_id(self, user_id: str) -> Optional[dict]:
        session = self._session_factory()
        try:
            row = session.query(UserReadModel).filter(UserReadModel.id == user_id).first()
            if not row:
                return None
            return {"id": row.id, "name": row.name, "email": row.email}
        finally:
            session.close()