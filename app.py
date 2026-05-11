import random
import secrets

from flask import Flask, jsonify, send_from_directory, session

from prompts import PROMPTS

app = Flask(__name__, static_folder=".")
app.secret_key = secrets.token_hex(32)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/prompt", methods=["GET"])
def next_prompt():
    used = session.get("used", [])
    remaining = [i for i in range(len(PROMPTS)) if i not in used]
    if not remaining:
        used = []
        remaining = list(range(len(PROMPTS)))
    idx = random.choice(remaining)
    used.append(idx)
    session["used"] = used
    return jsonify({"text": PROMPTS[idx]})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9876, debug=True)
