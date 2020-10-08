FROM python:3.8 as dev

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
