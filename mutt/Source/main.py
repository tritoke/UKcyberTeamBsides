from flask import Flask, request, render_template_string
import os
import time
import re
from urllib.parse import urlparse
import multiprocessing

app = Flask(__name__)
FLAG_FILE = "flag.txt"

# Landing page
@app.route("/")
def index():
    return render_template_string("""
    <h1>The fastest lil robot!</h1>
    <p>Want the flag? Simple, just go to /flag before my lil robot gets to it! (he gets a 2 second head start tho, he only has small legs!)</p>
    <i>ive even added extra security with ✨gpt✨.. I'm not sure what it did but it looks good!</i> 
    """)

@app.route("/flag", defaults={"path": ""})
@app.route("/flag/<path:path>")
def flag(path):
    bot_proc = multiprocessing.Process(target=bot_visit_flag, args=(request.url,))
    bot_proc.start()
    bot_proc.join(timeout=2)
    if bot_proc.is_alive():
        bot_proc.terminate()
        if os.path.exists(FLAG_FILE):
            return(f"My robot had a head start... and you still beat him??? Fine, here's the flag: <b>{open(FLAG_FILE).read()}</b>")
    time.sleep(3)
    return "The robot wins this time, you weren't fast enough!"

def bot_visit_flag(url):
    try:
        visit_url_with_regex_check(url)
    except Exception as e:
        print(f"[!] Bot error on /flag: {e}")

# I've heard there's hackers about so im doing some checks so you don't hurt my poor lil robot! 
# I'm sure this function does *something*, I asked gpt to secure my code, so it must be safe! right?
def visit_url_with_regex_check(url):
    parsed = urlparse(url)
    full_path = parsed.path + (('#' + parsed.fragment) if parsed.fragment else '')
    path = full_path.lstrip('/').split('/')[-1]
    print(f"[*] Bot visiting: {url}")

    sanitized_path = path.replace("..", "").strip("/")

    start = time.time()
    # Legacy token decoder pattern for internal access keys
    print(f"path is: {path}")
    match = re.match("(a+)+$", path)

    path = path.replace("CT", "LM")
    elapsed = time.time() - start
    print(f"[*] Regex check took {elapsed:.3f} seconds")

    if "X-Trusted-Client" in request.headers:
        print("[*] Trusted client detected")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
