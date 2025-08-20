# Backend INIT – Hexagonal + CQRS (FastAPI, SQLAlchemy, RabbitMQ)

Este proyecto es un esqueleto inicial para levantar un backend con **Arquitectura Hexagonal**, **CQRS** y **bundle-contexts**, listo para ejecutarse en Docker con FastAPI, SQLAlchemy, RabbitMQ y Postgres.

---

## Objetivo
- Garantizar independencia del dominio mediante arquitectura hexagonal.  
- Separar comandos y consultas con **CQRS**.  
- Usar **RabbitMQ** para procesar comandos (escritura).  
- Consultar datos directamente desde el modelo de lectura.  
- Implementar **contexts modulares** (`users` y `auth`) para facilitar la escalabilidad.  

---

## Estructura del proyecto

```
backend-hex-cqrs/
├─ app/
│  ├─ main.py
│  ├─ container.py
│  ├─ config.py
│  ├─ message_bus.py
│  ├─ shared/
│  │  ├─ di.py
│  │  ├─ unit_of_work.py
│  │  └─ security.py
│  ├─ contexts/
│  │  ├─ users/
│  │  │  ├─ domain/
│  │  │  │  ├─ entities.py
│  │  │  │  ├─ value_objects.py
│  │  │  │  ├─ ports.py
│  │  │  │  └─ events.py
│  │  │  ├─ application/
│  │  │  │  ├─ commands.py
│  │  │  │  ├─ command_handlers.py
│  │  │  │  ├─ queries.py
│  │  │  │  └─ query_handlers.py
│  │  │  └─ infrastructure/
│  │  │     ├─ db.py
│  │  │     ├─ models.py
│  │  │     ├─ repositories.py
│  │  │     ├─ projections.py
│  │  │     ├─ rabbitmq_consumer.py
│  │  │     └─ api.py
│  │  └─ auth/
│  │     ├─ domain/
│  │     │  ├─ entities.py
│  │     │  └─ ports.py
│  │     ├─ application/
│  │     │  ├─ commands.py
│  │     │  └─ queries.py
│  │     └─ infrastructure/
│  │        └─ api.py
│  └─ __init__.py
├─ tests/
│  ├─ unit/
│  │  └─ users/
│  │     ├─ test_value_objects.py
│  │     └─ test_create_user_uc.py
│  └─ __init__.py
├─ alembic/ (opcional si deseas migraciones)
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ README.md
```

---

## Dependencias

Archivo `requirements.txt`:

```txt
fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic==2.8.2
SQLAlchemy==2.0.34
psycopg2-binary==2.9.9
passlib[bcrypt]==1.7.4
pika==1.3.2
python-dotenv==1.0.1
pytest==8.3.2
pytest-cov==5.0.0
```

---

## Configuración

Archivo `app/config.py` define las variables de entorno:

```python
class Settings(BaseSettings):
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "appdb"

    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    ...
```

---

## Arquitectura

### Hexagonal
- Dominio: entidades, value objects y puertos sin dependencia externa.  
- Aplicación: casos de uso (commands, queries y handlers).  
- Infraestructura: adaptadores para DB, API REST y RabbitMQ.  

### CQRS
- Comandos (write) → enviados como eventos a RabbitMQ.  
- Consultas (read) → se resuelven directamente contra el modelo de lectura.  

### Bundle-contexts
- `users`: gestión de usuarios (crear y consultar).  
- `auth`: contexto base para autenticación (placeholder).  

---

## Flujo CQRS

1. **Comando** → `POST /api/users`  
   - Se publica evento `users.create` en RabbitMQ.  
   - El worker consume el evento, guarda en `users` (modelo de escritura) y proyecta a `users_read`.  

2. **Consulta** → `GET /api/users/{id}`  
   - Se consulta directamente en la tabla `users_read`.  

---

## Pruebas

Ejecutar pruebas unitarias con cobertura:

```bash
pytest --cov=app/contexts/users/domain
```

Cobertura mínima: **80%** en capa de dominio.

---

## Docker

### Dockerfile
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
version: "3.9"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - rabbitmq

  worker:
    build: .
    command: ["python", "-m", "app.contexts.users.infrastructure.rabbitmq_consumer"]
    depends_on:
      - db
      - rabbitmq

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
```

---

## Cómo probar

1. Levantar el stack:
```bash
docker compose up --build
```

2. Crear un usuario:
```bash
curl -X POST http://localhost:8000/api/users   -H "Content-Type: application/json"   -d '{"name":"Ada","email":"ada@example.com","password":"s3cret"}'
```

3. Ver logs del worker para validar que consumió y proyectó.  

4. Consultar por ID:
```bash
curl http://localhost:8000/api/users/<ID>
```

---

## Decisiones arquitectónicas

- Hexagonal para independencia del dominio.  
- CQRS para separar lectura/escritura.  
- RabbitMQ para comandos y eventos.  
- Proyecciones simples `users → users_read`.  
- Bundle-contexts (`users`, `auth`) para escalabilidad.  
- Inyección de dependencias mediante un contenedor ligero (`shared/di.py`).  

---

## TODO (futuro)

- Migraciones con Alembic.  
- Idempotencia en consumidor RabbitMQ.  
- Validación de duplicados (ej. email único).  
- Logs y métricas para observabilidad.  
- Autenticación real con JWT en `auth`.  
