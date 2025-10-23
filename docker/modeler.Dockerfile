FROM python:3.11
WORKDIR /model
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-model.txt .
RUN pip install --no-cache-dir -r requirements-model.txt

COPY model/ model/
CMD ["python", "model/run.py"]
