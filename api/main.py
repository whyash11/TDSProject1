from flask import Flask, request, jsonify
from logic import answer_question

app = Flask(__name__)

@app.route("/api/", methods=["POST"])
def handle():
    data = request.get_json()
    q = data.get("question", "")
    image = data.get("image", None)  # Base64 image (if any)

    response = answer_question(q, image)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
