from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import os
import logging
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuração de vulnerabilidades (via variáveis de ambiente)
SAST_VULNS = os.getenv('SAST_VULNS', 'false').lower() == 'true'
SCM_VULNS = os.getenv('SCM_VULNS', 'false').lower() == 'true'
DAST_VULNS = os.getenv('DAST_VULNS', 'false').lower() == 'true'

# Vulnerabilidades específicas
XSS_VULN = os.getenv('XSS_VULN', 'false').lower() == 'true'
SQL_INJECTION_VULN = os.getenv('SQL_INJECTION_VULN', 'false').lower() == 'true'
COMMAND_INJECTION_VULN = os.getenv('COMMAND_INJECTION_VULN', 'false').lower() == 'true'
PATH_TRAVERSAL_VULN = os.getenv('PATH_TRAVERSAL_VULN', 'false').lower() == 'true'
HARDCODED_SECRETS_VULN = os.getenv('HARDCODED_SECRETS_VULN', 'false').lower() == 'true'
INSECURE_DEPENDENCIES = os.getenv('INSECURE_DEPENDENCIES', 'false').lower() == 'true'

# Log vulnerability status on startup
logger.info(f"Vulnerability Status:")
logger.info(f"  SAST_VULNS: {SAST_VULNS}")
logger.info(f"  SCM_VULNS: {SCM_VULNS}")
logger.info(f"  DAST_VULNS: {DAST_VULNS}")
logger.info(f"  XSS_VULN: {XSS_VULN}")
logger.info(f"  SQL_INJECTION_VULN: {SQL_INJECTION_VULN}")
logger.info(f"  COMMAND_INJECTION_VULN: {COMMAND_INJECTION_VULN}")
logger.info(f"  PATH_TRAVERSAL_VULN: {PATH_TRAVERSAL_VULN}")
logger.info(f"  HARDCODED_SECRETS_VULN: {HARDCODED_SECRETS_VULN}")
logger.info(f"  INSECURE_DEPENDENCIES: {INSECURE_DEPENDENCIES}")

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
        <p>Endpoints para teste de vulnerabilidades:</p>
        <ul>
            <li><code>/api/user/123</code> - SAST (SQL Injection)</li>
            <li><code>/api/secrets</code> - SCM (Hardcoded Secrets)</li>
            <li><code>/api/headers</code> - DAST (Information Disclosure)</li>
        </ul>
    </body>
    </html>
    """

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.json
    return jsonify({"echo": data})

# ===== SAST VULNERABILITIES =====

@app.route("/api/user/<user_id>")
def get_user(user_id):
    # SAST Vulnerability (SQL Injection) - Comment/Uncomment this line
    if os.getenv('ENABLE_VULNS', 'false').lower() == 'true':
        query = f"SELECT * FROM users WHERE id = {user_id}"  # NOSONAR
        try:
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
            cursor.execute("INSERT INTO users (id, name) VALUES (123, 'test_user')")
            cursor.execute(query)
            result = cursor.fetchall()
            return jsonify({"users": result})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"message": "SQL injection vulnerability disabled"})

@app.route("/api/ping", methods=["POST"])
def ping_host():
    logger.info(f"SAST Command Injection test - SAST_VULNS: {SAST_VULNS}, COMMAND_INJECTION_VULN: {COMMAND_INJECTION_VULN}")
    
    if not SAST_VULNS or not COMMAND_INJECTION_VULN:
        return jsonify({"message": "Command injection vulnerability disabled"})
    
    # NOSONAR - This code is only executed when vulnerabilities are enabled for testing
    if SAST_VULNS and COMMAND_INJECTION_VULN:
        import subprocess
        data = request.json
        host = data.get('host', '')
        command = f"ping -c 1 {host}"  # NOSONAR
        try:
            result = subprocess.check_output(command, shell=True, text=True)  # NOSONAR
            return jsonify({"result": result})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        # Secure version - no vulnerabilities
        return jsonify({"message": "Command injection vulnerability disabled"})

# ===== SCM VULNERABILITIES =====

@app.route("/api/secrets")
def get_secrets():
    # SCM Vulnerability (Hardcoded Secrets) - Comment/Uncomment this line
    if os.getenv('ENABLE_VULNS', 'false').lower() == 'true':
        secrets = {
            "database_password": "super_secret_password_123",  # NOSONAR
            "api_key": "sk_test_51ABCDEFGhijklmnop"  # NOSONAR
        }
        return jsonify(secrets)
    else:
        return jsonify({"message": "Hardcoded secrets vulnerability disabled"})

@app.route("/api/dependencies")
def get_dependencies():
    logger.info(f"SCM Insecure Dependencies test - SCM_VULNS: {SCM_VULNS}, INSECURE_DEPENDENCIES: {INSECURE_DEPENDENCIES}")
    
    if not SCM_VULNS or not INSECURE_DEPENDENCIES:
        return jsonify({"message": "Insecure dependencies vulnerability disabled"})
    
    # NOSONAR - This code is only executed when vulnerabilities are enabled for testing
    if SCM_VULNS and INSECURE_DEPENDENCIES:
        dependencies = {
            "flask": "2.3.3",
            "requests": "2.28.2",  # NOSONAR - Old version for testing
            "gunicorn": "21.2.0"
        }
        return jsonify(dependencies)
    else:
        # Secure version - latest versions
        return jsonify({"message": "Insecure dependencies vulnerability disabled"})

# ===== DAST VULNERABILITIES =====

@app.route("/api/file/<path:file_path>")
def read_file(file_path):
    # Normalize the path by removing trailing slashes
    normalized_path = os.path.normpath(file_path)
    
    logger.info(f"DAST Path Traversal test - DAST_VULNS: {DAST_VULNS}, PATH_TRAVERSAL_VULN: {PATH_TRAVERSAL_VULN}")
    
    if not DAST_VULNS or not PATH_TRAVERSAL_VULN:
        return jsonify({"message": "Path traversal vulnerability disabled"})
    
    # NOSONAR - This code is only executed when vulnerabilities are enabled for testing
    if DAST_VULNS and PATH_TRAVERSAL_VULN:
        try:
            with open(normalized_path, 'r') as f:  # NOSONAR
                content = f.read()
            return jsonify({"content": content})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        # Secure version - path validation
        return jsonify({"message": "Path traversal vulnerability disabled"})

@app.route("/api/headers")
def get_headers():
    # DAST Vulnerability (Information Disclosure) - Comment/Uncomment this line
    if os.getenv('ENABLE_VULNS', 'false').lower() == 'true':
        response = jsonify({"message": "Headers info"})
        response.headers['X-Powered-By'] = 'Flask/2.0.1'  # NOSONAR
        return response
    else:
        response = jsonify({"message": "DAST vulnerabilities disabled"})
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

# ===== CONFIGURATION ENDPOINTS =====

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

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 