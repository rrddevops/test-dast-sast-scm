from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Aplicação Flask - SAST, SCM, DAST</h1>"

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.json
    return jsonify({"echo": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 