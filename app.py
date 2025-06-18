from flask import Flask, request, jsonify
import os
import sqlite3

app = Flask(__name__)

# Variáveis globais de configuração de vulnerabilidades
SAST_VULNS = os.getenv('SAST_VULNS', 'false').lower() == 'true'
SCM_VULNS = os.getenv('SCM_VULNS', 'false').lower() == 'true'
DAST_VULNS = os.getenv('DAST_VULNS', 'false').lower() == 'true'
XSS_VULN = os.getenv('XSS_VULN', 'false').lower() == 'true'
SQL_INJECTION_VULN = os.getenv('SQL_INJECTION_VULN', 'false').lower() == 'true'
COMMAND_INJECTION_VULN = os.getenv('COMMAND_INJECTION_VULN', 'false').lower() == 'true'
PATH_TRAVERSAL_VULN = os.getenv('PATH_TRAVERSAL_VULN', 'false').lower() == 'true'
HARDCODED_SECRETS_VULN = os.getenv('HARDCODED_SECRETS_VULN', 'false').lower() == 'true'
INSECURE_DEPENDENCIES = os.getenv('INSECURE_DEPENDENCIES', 'false').lower() == 'true'

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
        "sast_vulns": SAST_VULNS,
        "scm_vulns": SCM_VULNS,
        "dast_vulns": DAST_VULNS,
        "xss_vuln": XSS_VULN,
        "sql_injection_vuln": SQL_INJECTION_VULN,
        "command_injection_vuln": COMMAND_INJECTION_VULN,
        "path_traversal_vuln": PATH_TRAVERSAL_VULN,
        "hardcoded_secrets_vuln": HARDCODED_SECRETS_VULN,
        "insecure_dependencies_vuln": INSECURE_DEPENDENCIES
    })

@app.route("/api/user/<user_id>")
def get_user(user_id):
    if SAST_VULNS and SQL_INJECTION_VULN:
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
    else:
        return jsonify({"message": "SQL injection vulnerability disabled"})

@app.route("/api/ping", methods=["POST"])
def ping_host():
    if SAST_VULNS and COMMAND_INJECTION_VULN:
        data = request.get_json(force=True)
        host = data.get('host', '')
        # Simulação segura
        return jsonify({"result": f"Pinging {host} (simulado)"})
    else:
        return jsonify({"message": "Command injection vulnerability disabled"})

@app.route("/api/secrets")
def get_secrets():
    if SCM_VULNS and HARDCODED_SECRETS_VULN:
        return jsonify({
            "database_password": "super_secret_password_123",
            "api_key": "sk_test_51ABCDEFGhijklmnop"
        })
    else:
        return jsonify({"message": "Hardcoded secrets vulnerability disabled"})

@app.route("/api/dependencies")
def get_dependencies():
    if SCM_VULNS and INSECURE_DEPENDENCIES:
        return jsonify({
            "flask": "2.3.3",
            "requests": "2.28.2",
            "gunicorn": "21.2.0"
        })
    else:
        return jsonify({"message": "Insecure dependencies vulnerability disabled"})

@app.route("/api/file/<path:file_path>")
def read_file(file_path):
    if DAST_VULNS and PATH_TRAVERSAL_VULN:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return jsonify({"content": content})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"message": "Path traversal vulnerability disabled"})

@app.route("/api/headers")
def get_headers():
    if DAST_VULNS:
        response = jsonify({"message": "Headers info"})
        response.headers['X-Powered-By'] = 'Flask/2.0.1'
        return response
    else:
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
            "sast_vulns": SAST_VULNS,
            "scm_vulns": SCM_VULNS,
            "dast_vulns": DAST_VULNS,
            "xss_vuln": XSS_VULN,
            "sql_injection_vuln": SQL_INJECTION_VULN,
            "command_injection_vuln": COMMAND_INJECTION_VULN,
            "path_traversal_vuln": PATH_TRAVERSAL_VULN,
            "hardcoded_secrets_vuln": HARDCODED_SECRETS_VULN,
            "insecure_dependencies_vuln": INSECURE_DEPENDENCIES
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 