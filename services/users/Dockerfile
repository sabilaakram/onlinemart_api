FROM python:3.9

WORKDIR /app

# Install system dependencies if needed (e.g., gcc, libc-dev, curl)
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Dapr CLI
RUN curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | /bin/bash

# Initialize Dapr
RUN dapr init

# Copy the pyproject.toml and poetry.lock files to the container
COPY ./services/users/pyproject.toml ./services/users/poetry.lock /app/

# Install Poetry
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

# Copy the rest of the application code
COPY ./services/users /app

# Create Dapr components directory and copy component files
RUN mkdir -p /root/.dapr/components
COPY ./components /root/.dapr/components

# Run the application with Dapr
CMD ["dapr", "run", "--app-id", "user-service", "--app-port", "8000", "--dapr-http-port", "3500", "--components-path", "/root/.dapr/components", "--", "poetry", "run", "uvicorn", "users.main:app", "--host", "0.0.0.0", "--port", "8000"]
