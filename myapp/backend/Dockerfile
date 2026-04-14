# Use Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (adjust if needed)
EXPOSE 5000

# Run app (adjust depending on your framework)
CMD ["python", "src/app.py"]