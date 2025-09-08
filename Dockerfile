FROM python:3.12-slim
WORKDIR /app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && pip install --upgrade pip \
    && pip install pipenv

COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock


# install Python dependencies
RUN pipenv install --system --deploy --ignore-pipfile \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY . /app


# Collect static files (if needed)
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run migrations, seed data, and start server
CMD ["sh", "-c", "run_command.sh"]
