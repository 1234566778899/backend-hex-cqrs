from app.shared.di import container
from app.contexts.users.infrastructure.db import SessionLocal
from app.contexts.users.infrastructure.repositories import UserReadRepository

# Repos de lectura (consultas directas)
container.register("users.read_repo", lambda: UserReadRepository(SessionLocal))