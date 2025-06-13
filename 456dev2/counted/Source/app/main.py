from typing import Annotated, Any, Dict
import fastapi
import jwt # PyJWT, 
import os

secrets_env = os.environ.get("jwt_secrets", None)
if secrets_env is None:
    raise ValueError("No jwt_secrets provided")

secrets = list(map(str.strip, secrets_env.split(",")))

print(secrets)

flag = os.environ.get("flag") or "ctf{this_is_a_fake_flag}"

app = fastapi.FastAPI(
    redoc_url=None,
    docs_url=None,
    openapi_url=None,
)

def decode_rotated(c: str, secrets: list[str]) -> Dict[str, Any]:
    for s in secrets:
        try:
            return jwt.decode(c, s, algorithms=["HS256"])
        except jwt.InvalidSignatureError:
            pass
    raise ValueError("Invalid token")


@app.get("/")
def get_root(d : Annotated[str | None, fastapi.Cookie()] = None):

    set_cookie = True
    data = {"count": 0}
    if d is not None:
        try:
            data = decode_rotated(d, secrets)
            set_cookie = False
        except ValueError:
            pass
    
    resp = fastapi.responses.HTMLResponse(content=f"""
<h1>Dashboard</h1>
<p>Count: {data["count"]}</p>
<a href="/add" ><button>Add</button></a>
<a href="/flag" ><button>Get Flag</button></a>
""")
    if set_cookie:
        resp.set_cookie("d", jwt.encode(data, secrets[0], algorithm="HS256"))
    return resp

@app.get("/add")
def add(d : Annotated[str | None, fastapi.Cookie()] = None):
    resp = fastapi.responses.RedirectResponse(url="/")
    data = {"count": 0}
    if d is not None:
        try:
            data = decode_rotated(d, secrets)
        except ValueError:
            pass
    data["count"] += 1
    resp.set_cookie("d", jwt.encode(data, secrets[0], algorithm="HS256"))
    
    return resp

@app.get("/flag")
def get_flag(d : Annotated[str | None, fastapi.Cookie()] = None):
    data = {"count": 0}
    if d is not None:
        try:
            data = decode_rotated(d, secrets)
        except ValueError:
            pass
    if data["count"] < 0:
        response = fastapi.responses.HTMLResponse(content=f"""
<h1>Flag</h1>
<p>Congratulations, on getting here in only {data["count"]} clicks</p>
<p>flag: <pre>{flag}</pre></p>
<a href="/" ><button>Go Back</button></a>
""")
    else:
        response = fastapi.responses.HTMLResponse(content="""
<h1>ERROR</h1>
<p>You have TOO MANY clicks for this :(</p>
<a href="/" ><button>Go Back</button></a>
""")
        response.status_code = 403
    return response