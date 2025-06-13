FROM python:3.11-slim
WORKDIR /app
COPY main.py .
COPY ca.key ca.crt ./
RUN pip install fastapi uvicorn cryptography
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 