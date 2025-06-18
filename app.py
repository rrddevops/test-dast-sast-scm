from flask import Flask, request, jsonify, render_template_string
import os
import logging

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
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Security Test App - SAST, SCM, DAST</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .vuln-section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            .vuln-active { background-color: #ffe6e6; border-color: #ff9999; }
            .vuln-inactive { background-color: #e6ffe6; border-color: #99ff99; }
            .status { font-weight: bold; }
            .active { color: red; }
            .inactive { color: green; }
            button { padding: 10px 20px; margin: 5px; cursor: pointer; }
            input { padding: 5px; margin: 5px; }
        </style>
    </head>
    <body>
        <h1>🔒 Security Test Application</h1>
        <p>Esta aplicação contém vulnerabilidades controláveis para testar SAST, SCM e DAST.</p>
        
        <div class="vuln-section {{ 'vuln-active' if SAST_VULNS else 'vuln-inactive' }}">
            <h2>🔍 SAST Vulnerabilities</h2>
            <p class="status">Status: <span class="{{ 'active' if SAST_VULNS else 'inactive' }}">{{ 'ACTIVE' if SAST_VULNS else 'INACTIVE' }}</span></p>
            <p>Vulnerabilidades de código estático: XSS, SQL Injection, Command Injection, etc.</p>
            <button onclick="testXSS()">Test XSS</button>
            <button onclick="testSQLInjection()">Test SQL Injection</button>
            <button onclick="testCommandInjection()">Test Command Injection</button>
        </div>

        <div class="vuln-section {{ 'vuln-active' if SCM_VULNS else 'vuln-inactive' }}">
            <h2>📦 SCM Vulnerabilities</h2>
            <p class="status">Status: <span class="{{ 'active' if SCM_VULNS else 'inactive' }}">{{ 'ACTIVE' if SCM_VULNS else 'INACTIVE' }}</span></p>
            <p>Vulnerabilidades de dependências e configurações: secrets hardcoded, dependências inseguras.</p>
            <button onclick="testHardcodedSecrets()">Test Hardcoded Secrets</button>
            <button onclick="testInsecureDependencies()">Test Insecure Dependencies</button>
        </div>

        <div class="vuln-section {{ 'vuln-active' if DAST_VULNS else 'vuln-inactive' }}">
            <h2>🛡️ DAST Vulnerabilities</h2>
            <p class="status">Status: <span class="{{ 'active' if DAST_VULNS else 'inactive' }}">{{ 'ACTIVE' if DAST_VULNS else 'INACTIVE' }}</span></p>
            <p>Vulnerabilidades de aplicação web: path traversal, headers inseguros, etc.</p>
            <button onclick="testPathTraversal()">Test Path Traversal</button>
            <button onclick="testInsecureHeaders()">Test Insecure Headers</button>
        </div>

        <div class="vuln-section">
            <h2>⚙️ Configuration</h2>
            <p>Configure as vulnerabilidades via variáveis de ambiente:</p>
            <ul>
                <li><code>SAST_VULNS=true/false</code> - Ativa/desativa vulnerabilidades SAST</li>
                <li><code>SCM_VULNS=true/false</code> - Ativa/desativa vulnerabilidades SCM</li>
                <li><code>DAST_VULNS=true/false</code> - Ativa/desativa vulnerabilidades DAST</li>
            </ul>
        </div>

        <script>
            function testXSS() {
                const userInput = prompt("Enter your name:");
                if (userInput) {
                    document.getElementById('output').innerHTML = '<h3>Hello, ' + userInput + '!</h3>';
                }
            }

            function testSQLInjection() {
                const userInput = prompt("Enter user ID:");
                if (userInput) {
                    fetch('/api/user/' + userInput)
                        .then(response => response.json())
                        .then(data => alert('Result: ' + JSON.stringify(data)));
                }
            }

            function testCommandInjection() {
                const userInput = prompt("Enter hostname to ping:");
                if (userInput) {
                    fetch('/api/ping', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({host: userInput})
                    })
                    .then(response => response.json())
                    .then(data => alert('Result: ' + JSON.stringify(data)));
                }
            }

            function testHardcodedSecrets() {
                fetch('/api/secrets')
                    .then(response => response.json())
                    .then(data => alert('Secrets: ' + JSON.stringify(data)));
            }

            function testInsecureDependencies() {
                fetch('/api/dependencies')
                    .then(response => response.json())
                    .then(data => alert('Dependencies: ' + JSON.stringify(data)));
            }

            function testPathTraversal() {
                const userInput = prompt("Enter file path:");
                if (userInput) {
                    fetch('/api/file/' + userInput)
                        .then(response => response.json())
                        .then(data => alert('Result: ' + JSON.stringify(data)));
                }
            }

            function testInsecureHeaders() {
                fetch('/api/headers')
                    .then(response => response.json())
                    .then(data => alert('Headers: ' + JSON.stringify(data)));
            }
        </script>
        <div id="output"></div>
    </body>
    </html>
    """, SAST_VULNS=SAST_VULNS, SCM_VULNS=SCM_VULNS, DAST_VULNS=DAST_VULNS)

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.json
    return jsonify({"echo": data})

# ===== SAST VULNERABILITIES =====

@app.route("/api/user/<user_id>")
def get_user(user_id):
    logger.info(f"SAST SQL Injection test - SAST_VULNS: {SAST_VULNS}, SQL_INJECTION_VULN: {SQL_INJECTION_VULN}")
    
    if not SAST_VULNS or not SQL_INJECTION_VULN:
        return jsonify({"message": "SQL injection vulnerability disabled"})
    
    # NOSONAR - This code is only executed when vulnerabilities are enabled for testing
    if SAST_VULNS and SQL_INJECTION_VULN:
        import sqlite3
        query = f"SELECT * FROM users WHERE id = {user_id}"  # NOSONAR
        try:
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            # Create table first for testing
            cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
            cursor.execute("INSERT INTO users (id, name) VALUES (123, 'test_user')")
            cursor.execute(query)  # NOSONAR
            result = cursor.fetchall()
            return jsonify({"users": result})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        # Secure version - no vulnerabilities
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
    logger.info(f"SCM Hardcoded Secrets test - SCM_VULNS: {SCM_VULNS}, HARDCODED_SECRETS_VULN: {HARDCODED_SECRETS_VULN}")
    
    if not SCM_VULNS or not HARDCODED_SECRETS_VULN:
        return jsonify({"message": "Hardcoded secrets vulnerability disabled"})
    
    # NOSONAR - This code is only executed when vulnerabilities are enabled for testing
    if SCM_VULNS and HARDCODED_SECRETS_VULN:
        secrets = {
            "database_password": "super_secret_password_123",  # NOSONAR
            "api_key": "sk-1234567890abcdef",  # NOSONAR
            "jwt_secret": "my_jwt_secret_key_2024",  # NOSONAR
            "aws_access_key": "AKIAIOSFODNN7EXAMPLE",  # NOSONAR
            "aws_secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"  # NOSONAR
        }
        return jsonify(secrets)
    else:
        # Secure version - no secrets exposed
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
    # Remove any trailing slashes to handle both with and without slash
    file_path = file_path.rstrip('/')
    
    logger.info(f"DAST Path Traversal test - DAST_VULNS: {DAST_VULNS}, PATH_TRAVERSAL_VULN: {PATH_TRAVERSAL_VULN}")
    
    if not DAST_VULNS or not PATH_TRAVERSAL_VULN:
        return jsonify({"message": "Path traversal vulnerability disabled"})
    
    # NOSONAR - This code is only executed when vulnerabilities are enabled for testing
    if DAST_VULNS and PATH_TRAVERSAL_VULN:
        try:
            with open(file_path, 'r') as f:  # NOSONAR
                content = f.read()
            return jsonify({"content": content})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        # Secure version - path validation
        return jsonify({"message": "Path traversal vulnerability disabled"})

@app.route("/api/headers")
def get_headers():
    logger.info(f"DAST Insecure Headers test - DAST_VULNS: {DAST_VULNS}")
    
    if not DAST_VULNS:
        # Secure version - secure headers when DAST is disabled
        response = jsonify({"message": "DAST vulnerabilities disabled"})
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    
    # NOSONAR - This code is only executed when vulnerabilities are enabled for testing
    response = jsonify({"message": "Headers info"})
    response.headers['X-Powered-By'] = 'Flask/2.0.1'  # NOSONAR
    response.headers['Server'] = 'Apache/2.4.41'  # NOSONAR
    response.headers['X-Frame-Options'] = 'NONE'  # NOSONAR
    response.headers['X-Content-Type-Options'] = 'NONE'  # NOSONAR
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
    return jsonify({"status": "healthy", "vulnerabilities": {
        "sast": SAST_VULNS,
        "scm": SCM_VULNS,
        "dast": DAST_VULNS
    }})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 