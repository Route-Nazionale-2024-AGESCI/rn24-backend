FROM python:3.12-slim-bullseye AS python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get --no-install-recommends install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    postgresql-client \
    git \
    vim \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
WORKDIR /app/
# to fix ImproperlyConfigured: The SECRET_KEY setting must not be empty. during collectstatic
ENV DJANGO_SECRET_KEY foo
RUN ./manage.py collectstatic --noinput
CMD ["/bin/bash"]
