FROM python:3.11-slim-bookworm

# WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
EXPOSE 8501

CMD ["python", "app/run_pipeline.py"]