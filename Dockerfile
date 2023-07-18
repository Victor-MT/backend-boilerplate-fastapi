# Imagem base
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 8000
