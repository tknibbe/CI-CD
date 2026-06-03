# App/App.py
import string
import random
from flask import Flask, request, jsonify, redirect

App = Flask(__name__)

# --- "database"

db = {}

# ---------- Code generation ----------


def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


# ---------- Routes ----------

@App.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@App.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json(silent=True)
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    original_url = data["url"].strip()
    if not original_url:
        return jsonify({"error": "URL cannot be empty"}), 400

    if not original_url.startswith(("http://", "https://")):
        return jsonify({"error": "URL must start with http(s)://"}), 400

    # Re-use existing code if URL was already shortened
    if original_url in db.values():
        for code, url in db.items():
            if url == original_url:
                return jsonify({"code": code, "short_url": f"/{code}"}), 200

    # Generate a unique code
    for _ in range(10):
        code = generate_code()
        if code not in db.keys():
            break
    else:
        return jsonify({"error": "Could not generate unique code"}), 500

    db[code] = original_url

    return jsonify({"code": code, "short_url": f"/{code}"}), 201


@App.route("/<code>")
def redirect_to_url(code):
    url = db.get(code)
    if not url:
        return jsonify({"error": "Code not found"}), 404
    return redirect(url, code=302)


# ---------- Entry point ----------

if __name__ == "__main__":
    App.run(host="0.0.0.0", debug=True, port=5000)
