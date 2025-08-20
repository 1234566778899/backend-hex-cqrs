import json
import pika
from app.config import settings
from app.contexts.users.infrastructure.db import SessionLocal, Base, engine
from app.contexts.users.infrastructure.models import UserModel
from app.contexts.users.infrastructure.projections import project_user_created
from sqlalchemy.orm import Session


# Crear tablas si no existen
Base.metadata.create_all(bind=engine)


EXCHANGE = "users"
QUEUE = "users.create.queue"
ROUTING_KEY = "users.create"


connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic', durable=True)
channel.queue_declare(queue=QUEUE, durable=True)
channel.queue_bind(exchange=EXCHANGE, queue=QUEUE, routing_key=ROUTING_KEY)


print("[worker] Esperando mensajes...")


def on_message(ch, method, properties, body):
    data = json.loads(body.decode("utf-8"))
    with SessionLocal() as session: # type: Session
    # Persistir en modelo de escritura
        user = UserModel(
        id=data["user_id"], name=data["name"], email=data["email"], password_hash=data["password_hash"]
        )
        session.add(user)
        # Proyectar al modelo de lectura
        project_user_created(session, user_id=data["user_id"], name=data["name"], email=data["email"])
        session.commit()
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE, on_message_callback=on_message)


if __name__ == "__main__":
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()