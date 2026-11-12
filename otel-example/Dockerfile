FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Installs the instrumentation packages matching the libraries above (Flask, etc.)
RUN opentelemetry-bootstrap -a install

COPY app.py .

EXPOSE 5001

CMD ["opentelemetry-instrument", "python", "app.py"]
