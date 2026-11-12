FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=notesapp.settings

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
RUN opentelemetry-bootstrap -a install

COPY . /app

EXPOSE 8000

# Plain start first, to get the app working
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]

# Once it works, switch to this to turn OpenTelemetry back on:
# CMD ["sh", "-c", "python manage.py migrate --noinput && opentelemetry-instrument python manage.py runserver 0.0.0.0:8000 --noreload"]
