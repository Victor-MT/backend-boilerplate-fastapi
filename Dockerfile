# Imagem base
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

COPY . .
# Install core dependencies.
#RUN apt-get update && apt-get install -y libpq-dev build-essential

# Instala as dependências
#RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 8000

# Comando para iniciar o servidor FastAPI
#CMD ["bash", "-c", "source dev.env && uvicorn main:app --host 0.0.0.0 --port 8000"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]