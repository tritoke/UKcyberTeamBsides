# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyjwt",
# ]
# ///
import jwt

payload = {"count": -1}

print(jwt.encode(payload, ""))
