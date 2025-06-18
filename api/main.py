from flask import Flask, request, jsonify
from logic import answer_question
import os

app = Flask(__name__)

@app.route("/api/", methods=["POST"])
def handle():
    data = request.get_json()
    q = data.get("question", "")
    image = data.get("image", None)  # Base64 image (if any)

    response = answer_question(q, image)
    return jsonify(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # AI Pipe / Render will set this
    app.run(host="0.0.0.0", port=port, debug=True)
