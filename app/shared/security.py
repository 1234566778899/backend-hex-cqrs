from passlib.hash import bcrypt

class PasswordHasher:
    @staticmethod
    def hash(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def verify(password: str, password_hash: str) -> bool:
        return bcrypt.verify(password, password_hash)