# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better cache
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the backend directory
COPY backend/ .

# 認証情報の設定
ARG FIREBASE_CREDENTIALS
ARG DIFY_API_KEY
COPY ${FIREBASE_CREDENTIALS} firebase-credentials.json

# Set environment variables
ENV PORT=8080
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/firebase-credentials.json
ENV DIFY_API_KEY=${DIFY_API_KEY}

# Make port available
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]