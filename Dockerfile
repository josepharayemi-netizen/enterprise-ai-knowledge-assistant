FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m assistant_app.ingest --source knowledge --output artifacts/index.joblib
USER 65532:65532
CMD ["uvicorn","assistant_app.api:app","--host","0.0.0.0","--port","8000"]
