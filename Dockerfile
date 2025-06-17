FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set default vulnerability flags (can be overridden at runtime)
ENV SAST_VULNS=false
ENV SCM_VULNS=false
ENV DAST_VULNS=false
ENV XSS_VULN=false
ENV SQL_INJECTION_VULN=false
ENV COMMAND_INJECTION_VULN=false
ENV PATH_TRAVERSAL_VULN=false
ENV HARDCODED_SECRETS_VULN=false
ENV INSECURE_DEPENDENCIES=false

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"] 