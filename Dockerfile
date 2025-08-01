FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY controller controller
CMD ["uvicorn", "controller.api:app", "--host", "0.0.0.0", "--port", "8000"]
