# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install flask requests

RUN FLAG="flag{UKCT-mutt_1AI1NnJWRr5r0RnR}" && \
    echo "$FLAG" > flag.txt

CMD ["python", "-u", "main.py"]
