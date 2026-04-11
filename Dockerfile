FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . . 

# Installing the package itself so src is importable from anywhere
# Fix for ModuleNotFoundError: No module named 'src'
RUN pip install -e .

# Default: run full analysis
CMD ["python", "run_analysis.py"]