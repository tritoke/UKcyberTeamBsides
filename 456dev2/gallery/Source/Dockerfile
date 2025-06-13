FROM python:3.12-trixie AS builder
WORKDIR /app

RUN pip install jinja2

# Copy the rest of the application code to the container
COPY public public
COPY build.py .
COPY templates templates

# builds output dist/
RUN python3 build.py

# caddy layer for static files
FROM caddy:2.10

# Copy the static files from the builder image
COPY Caddyfile /etc/caddy/Caddyfile
COPY list.html /usr/share/caddy/listing-template.html
COPY --from=builder /app/dist /usr/share/caddy

ARG FLAG=flag{test_flag}
ENV flag=$FLAG

EXPOSE 80