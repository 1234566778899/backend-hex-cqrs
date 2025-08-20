from sqlalchemy.orm import Session
from .models import UserReadModel


def project_user_created(session: Session, user_id: str, name: str, email: str) -> None:
    # upsert simple
    exists = session.query(UserReadModel).filter(UserReadModel.id == user_id).first()
    if exists:
        exists.name = name
        exists.email = email
    else:
        session.add(UserReadModel(id=user_id, name=name, email=email))