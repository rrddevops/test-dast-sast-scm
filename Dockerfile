FROM python:3.11-slim

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy pip configuration
COPY pip.conf /etc/pip.conf

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary=all -r requirements.txt

COPY . .

# Set default vulnerability flags (all disabled by default)
ENV SAST_VULNS=false
ENV SCM_VULNS=false
ENV DAST_VULNS=false
ENV XSS_VULN=false
ENV SQL_INJECTION_VULN=false
ENV COMMAND_INJECTION_VULN=false
ENV PATH_TRAVERSAL_VULN=false
ENV HARDCODED_SECRETS_VULN=false
ENV INSECURE_DEPENDENCIES=false

ENV ENABLE_VULNS=false

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"] 