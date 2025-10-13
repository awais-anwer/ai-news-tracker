FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Copy environment variables (optional for debugging)
COPY .env ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Command to start FastAPI
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
