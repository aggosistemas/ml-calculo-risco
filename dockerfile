# Usa imagem leve do Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia a aplicação
COPY app/ ./app/

# Copia o modelo treinado (model.pkl deve estar na raiz do projeto antes do build)
COPY model.pkl ./app/

# Expondo a porta da API
EXPOSE 8000

# Comando para iniciar o FastAPI com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
