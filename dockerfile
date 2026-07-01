# Use official Python image
FROM python:3.12

# Set working directory inside container
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script into the container
COPY test.py .

# Run the script when container starts
CMD ["python", "test.py"]