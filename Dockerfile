FROM python:3.9-slim-buster
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y wkhtmltopdf
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .