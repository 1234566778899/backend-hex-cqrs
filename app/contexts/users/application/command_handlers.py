import json
import uuid
import pika
from app.config import settings
from app.shared.security import PasswordHasher
from app.contexts.users.domain.events import UserCreated

class CreateUserHandler:
    EXCHANGE = "users"
    ROUTING_KEY = "users.create"

    def __init__(self):
        self._conn = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
        )
        self._channel = self._conn.channel()
        self._channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='topic', durable=True)

    def __del__(self):
        try:
            self._conn.close()
        except Exception:
            pass

    def handle(self, name: str, email: str, password: str) -> dict:
        # Generar ID y hash
        user_id = str(uuid.uuid7()) if hasattr(uuid, 'uuid7') else str(uuid.uuid4())
        password_hash = PasswordHasher.hash(password)
        event = UserCreated(user_id=user_id, name=name, email=email, password_hash=password_hash)

        # Publicar evento a RabbitMQ (topic)
        payload = json.dumps(event.__dict__).encode("utf-8")
        self._channel.basic_publish(
        exchange=self.EXCHANGE,
        routing_key=self.ROUTING_KEY,
        body=payload,
        properties=pika.BasicProperties(delivery_mode=2)
        )
        return {"id": user_id}