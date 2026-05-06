# Use a light Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements first (Better for Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]