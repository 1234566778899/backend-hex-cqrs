from app.shared.di import container
from app.contexts.users.domain.ports import IUserReadRepository

class GetUserByIdHandler:
    def __init__(self):
        self.read_repo: IUserReadRepository = container.resolve("users.read_repo")

    def handle(self, user_id: str):
        return self.read_repo.get_by_id(user_id)