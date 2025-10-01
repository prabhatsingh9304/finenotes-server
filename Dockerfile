FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/api

EXPOSE 5000

CMD ["uvicorn", "api.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]