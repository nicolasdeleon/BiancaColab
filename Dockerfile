FROM python:3.7.5
MAINTAINER nicolasmatiasdeleon@gmail.com

# Set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_COLORS light

# Install dependencies
RUN pip install --upgrade --no-cache-dir pip

COPY requirements.txt prod-requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -r prod-requirements.txt
# Copy project
COPY . /app/

EXPOSE 8000

RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
