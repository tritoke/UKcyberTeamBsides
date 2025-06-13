Generate a CA key and certificate for prod PKI:

openssl req -x509 -newkey rsa:2048 -days 3650 -nodes -keyout ca.key -out ca.crt -subj "/CN=Prod PKI CA"

Place ca.key and ca.crt in this directory. 