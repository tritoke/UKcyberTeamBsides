FROM python:3.12-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ARG FLAG="ctf{this_is_a_fake_flag}"
ENV flag=${FLAG}
ARG JWT_SECRETS="example,secret2"
ENV jwt_secrets=${JWT_SECRETS}
EXPOSE 8085
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8085" ]