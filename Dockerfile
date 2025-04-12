# Base image: Python 3.10 slim for a lightweight container
FROM python:3.10-slim

# Set the working directory for all subsequent commands
WORKDIR /app

# Install dependencies first (better layer caching)
# Copy only requirements.txt to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# This layer changes only when source code changes
COPY . .

# Document the port FastAPI will listen on
EXPOSE 8000

# Start the FastAPI application with hot-reload enabled
# - host 0.0.0.0: Accept connections from any IP
# - port 8000: Listen on port 8000
# - reload: Enable auto-reload on code changes
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]