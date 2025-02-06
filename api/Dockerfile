# Imagem oficial baseada em python
FROM python:3.11-slim

# Diretório de trabalho no container
WORKDIR /api

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

# Copiando projeto e instalando pacotes Python
RUN pip install --upgrade pip
COPY . /api
RUN pip install --no-cache-dir -r requirements.txt

# Coletando staticfiles
RUN python manage.py collectstatic --noinput

# Expor a porta 8000
EXPOSE 8000
