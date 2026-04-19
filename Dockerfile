FROM python:3.12-slim

# Create working directory for app package
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create app directory for the Python package
RUN mkdir -p /app/app

# Copy app contents
COPY app/ ./app/

# Create non-root user and switch to it
RUN adduser --disabled-password --gecos '' appuser || true
USER appuser

# Expose port
EXPOSE 8000

# Set working directory to match app package location
WORKDIR /app/app

# Run the application - app.is directly accessible as the package
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
