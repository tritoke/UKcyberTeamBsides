# sudo docker build -t rolling-my-own-ctr-mode .
# sudo docker run -p 1337:1337 rolling-my-own-ctr-mode

FROM alpine:latest

RUN apk update && \
    apk add --no-cache python3 py3-pip socat && \
    pip3 install --break-system-packages --no-cache-dir pycryptodome

COPY flag.py /root/flag.py
COPY server.py /root/server.py

CMD socat TCP-LISTEN:1337,fork,reuseaddr EXEC:'python3 /root/server.py',stderr
