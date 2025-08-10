FROM python:3.9-slim
RUN apt-get update && apt-get install -y build-essential git curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /data/chroma /data/documents /app/scripts /app/config
COPY ./scripts /app/scripts
COPY ./config /app/config
COPY ./data/documents /data/documents
EXPOSE 8000
CMD ["uvicorn", "scripts.process_documents:app", "--host", "0.0.0.0", "--port", "8000"]
