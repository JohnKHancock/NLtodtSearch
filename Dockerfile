FROM python:3.11-slim

WORKDIR /app

COPY application/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY application/ ./application/

WORKDIR /app/application

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
