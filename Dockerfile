FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Instalamos curl para healthcheck en Docker Compose.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY app /app/app
COPY main.py /app/main.py

# Expose port
EXPOSE 8000

# Run application
# Nota: el puerto puede configurarse con la variable de entorno PORT en Docker Compose.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
