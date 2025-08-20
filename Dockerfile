FROM python:3.12-slim


WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY app ./app
COPY tests ./tests


# Comando por defecto (API)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]