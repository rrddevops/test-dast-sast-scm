from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Test App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
        </style>
    </head>
    <body>
        <h1>Simple Test Application</h1>
        <p>Endpoints disponíveis:</p>
        <ul>
            <li><code>/api/user/123</code> - Consulta de usuário</li>
            <li><code>/api/secrets</code> - Informações</li>
            <li><code>/api/headers</code> - Headers</li>
            <li><code>/health</code> - Status da aplicação</li>
        </ul>
    </body>
    </html>
    """

@app.route("/api/echo", methods=["POST"])
def echo():
    if not request.content_type or 'application/json' not in request.content_type:
        return '', 415
    try:
        data = request.get_json(force=True)
    except Exception:
        return '', 400
    return jsonify({"echo": data})

@app.route("/api/config")
def get_config():
    return jsonify({
        "sast_vulns": False,
        "scm_vulns": False,
        "dast_vulns": False,
        "xss_vuln": False,
        "sql_injection_vuln": False,
        "command_injection_vuln": False,
        "path_traversal_vuln": False,
        "hardcoded_secrets_vuln": False,
        "insecure_dependencies_vuln": False
    })

@app.route("/api/user/<user_id>")
def get_user(user_id):
    try:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (123, 'test_user'))
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchall()
        return jsonify({"users": result})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/ping", methods=["POST"])
def ping_host():
    data = request.get_json(force=True)
    host = data.get('host', '')
    return jsonify({"result": f"Pinging {host} (simulado)"})

@app.route("/api/secrets")
def get_secrets():
    return jsonify({"message": "Hardcoded secrets vulnerability disabled"})

@app.route("/api/dependencies")
def get_dependencies():
    return jsonify({"message": "Insecure dependencies vulnerability disabled"})

@app.route("/api/file/<path:file_path>")
def read_file(file_path):
    return jsonify({"message": "Path traversal vulnerability disabled"})

@app.route("/api/headers")
def get_headers():
    response = jsonify({"message": "disabled"})
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "vulnerabilities": {
            "sast_vulns": False,
            "scm_vulns": False,
            "dast_vulns": False,
            "xss_vuln": False,
            "sql_injection_vuln": False,
            "command_injection_vuln": False,
            "path_traversal_vuln": False,
            "hardcoded_secrets_vuln": False,
            "insecure_dependencies_vuln": False
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 