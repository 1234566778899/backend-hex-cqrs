from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.contexts.users.application.command_handlers import CreateUserHandler
from app.contexts.users.application.query_handlers import GetUserByIdHandler

router = APIRouter(prefix="/users", tags=["users"])

class CreateUserDTO(BaseModel):
    name: str
    email: str
    password: str

@router.post("/", status_code=202)
def create_user(dto: CreateUserDTO):
    # Publica comando → evento (async via RabbitMQ). 202 Accepted.
    handler = CreateUserHandler()
    result = handler.handle(dto.name, dto.email, dto.password)
    return {"accepted": True, "id": result["id"]}

@router.get("/{user_id}")
def get_user(user_id: str):
    handler = GetUserByIdHandler()
    user = handler.handle(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user