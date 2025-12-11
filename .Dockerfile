FROM python:3.11.0

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src ./src

# Expose port
EXPOSE 8080

# If your app entrypoint is src/main.py
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
