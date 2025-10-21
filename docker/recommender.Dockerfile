# Use official Python slim image
FROM python:3.11-slim

# Prevent Python from writing pyc files and enable unbuffered mode
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install build tools and libraries needed for scientific packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app source code
COPY service/ service/
COPY model_registry/ model_registry/

# Expose the port Cloud Run expects
ENV PORT=8080
EXPOSE 8080

# Launch FastAPI via Uvicorn
CMD ["uvicorn", "service.app:app", "--host", "0.0.0.0", "--port", "8080"]