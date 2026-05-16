#imagem do python

FROM python:3.11-slim

#evita arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

#diretorio de trabalho
WORKDIR /app/

#copia apenas requirements

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copia o resto do codigo
COPY . .

EXPOSE 5000

#comando para inicializar a aplicaçao
CMD ["python", "run.py"]