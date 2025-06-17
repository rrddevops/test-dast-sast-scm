FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set default vulnerability flags (can be overridden at runtime)
ENV SAST_VULNS=true
ENV SCM_VULNS=true
ENV DAST_VULNS=true
ENV XSS_VULN=true
ENV SQL_INJECTION_VULN=true
ENV COMMAND_INJECTION_VULN=true
ENV PATH_TRAVERSAL_VULN=true
ENV HARDCODED_SECRETS_VULN=true
ENV INSECURE_DEPENDENCIES=true

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"] 