FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# requirements 먼저 복사해서 캐시 활용
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# backend 전체 복사 (db.sqlite3도 여기 들어있으면 같이 들어감)
COPY backend /app/backend

WORKDIR /app/backend

# Railway는 PORT 환경변수를 줌
CMD ["sh", "-c", "gunicorn universe.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
