# Base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into container
COPY src/ ./src/

# Default command to run CLI
CMD ["python", "src/cli.py"]
