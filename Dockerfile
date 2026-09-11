FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m playwright install --with-deps chromium

COPY app ./app
COPY sql ./sql
COPY main.py ./

EXPOSE 4159

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4159"]
