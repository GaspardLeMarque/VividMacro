FROM python:3.10.12-slim

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

EXPOSE 5000

# Run an application using Gunicorn WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]