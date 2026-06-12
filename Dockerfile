FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY script.py .
CMD ["flask", "--app", "script", "run", "--host", "0.0.0.0"]