FROM python:3.11

WORKDIR /sdk

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl unzip groff less \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

# Optional: install Python SDKs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Entrypoint (optional)
CMD ["aws", "--version"]
