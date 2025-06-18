from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Security Test App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
        </style>
    </head>
    <body>
        <h1>Security Test Application</h1>
        <p>Endpoints seguros:</p>
        <ul>
            <li><code>/api/user/123</code> - Consulta de usuário</li>
            <li><code>/api/secrets</code> - Informações</li>
            <li><code>/api/headers</code> - Headers</li>
        </ul>
    </body>
    </html>
    """

@app.route("/api/user/<user_id>")
def get_user(user_id):
    try:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (123, 'test_user'))
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchall()
        return jsonify({"message": "SQL injection vulnerability disabled"})
    except Exception as e:
        return jsonify({"message": "SQL injection vulnerability disabled"})

@app.route("/api/secrets")
def get_secrets():
    return jsonify({"message": "Hardcoded secrets vulnerability disabled"})

@app.route("/api/headers")
def get_headers():
    response = jsonify({"message": "disabled"})
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 