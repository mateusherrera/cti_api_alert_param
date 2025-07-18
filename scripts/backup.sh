#!/bin/bash

# Carrega variáveis do .env
set -a
source ../.env
set +a

# Data atual
NOW=$(date +"%Y%m%d_%H%M%S")

# Certifica que diretório de backup existe
mkdir -p "$BACKUP_DIR"

# Caminho final do arquivo
BACKUP_FILE="$BACKUP_DIR/backup_$NOW.sql"

echo "[INFO] Iniciando backup para: $BACKUP_FILE"

# Realiza o dump
docker exec -t "$CONTAINER_NAME" pg_dumpall -c -U "$POSTGRES_USER" > "$BACKUP_FILE"

# Verificação de sucesso
if [ $? -eq 0 ]; then
  echo "[SUCESSO] Backup salvo em: $BACKUP_FILE"
else
  echo "[ERRO] Falha no backup!"
  rm -f "$BACKUP_FILE"
  exit 1
fi
