# Exemplo de uso: ./scripts/restore.sh /dados/backup/backup_20250625_020000.sql

#!/bin/bash

# Carrega variáveis do .env
set -a
source ../.env
set +a

# Verifica se o caminho do arquivo foi passado
if [ -z "$1" ]; then
  echo "[ERRO] Você precisa informar o caminho do arquivo de backup (.sql)"
  echo "Uso: ./restore.sh /dados/backup/backup_YYYYMMDD_HHMMSS.sql"
  exit 1
fi

BACKUP_FILE="$1"

# Verifica se o arquivo existe
if [ ! -f "$BACKUP_FILE" ]; then
  echo "[ERRO] Arquivo $BACKUP_FILE não encontrado!"
  exit 1
fi

echo "[INFO] Restaurando backup de: $BACKUP_FILE"
cat "$BACKUP_FILE" | docker exec -i "$CONTAINER_NAME" psql -U "$POSTGRES_USER"

if [ $? -eq 0 ]; then
  echo "[SUCESSO] Backup restaurado com sucesso."
else
  echo "[ERRO] Falha ao restaurar backup."
  exit 1
fi
