# Use official Python image
FROM python:3.12

# Set working directory

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY test.py .

CMD ["uvicorn", "test:app", "--host", "0.0.0.0", "--port", "8000"]