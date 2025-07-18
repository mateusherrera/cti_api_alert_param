# Exemplos de uso:
# ./scripts/cleanup_backups.sh        # Remove arquivos com +7 dias
# ./scripts/cleanup_backups.sh 3      # Remove arquivos com +3 dias

#!/bin/bash

# Carrega variáveis do .env
set -a
source ../.env
set +a

# Número de dias (padrão: 7)
DIAS=${1:-7}

echo "[INFO] Removendo backups mais antigos que $DIAS dias em $BACKUP_DIR..."

find "$BACKUP_DIR" -name "*.sql" -type f -mtime +$DIAS -exec rm -v {} \;

echo "[SUCESSO] Limpeza concluída."
