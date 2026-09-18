#!/bin/sh
set -e

# Banco + aplicação no mesmo container. O banco é inicializado internamente
# em /var/lib/postgresql (monte aqui um Render Disk para os dados persistirem).

DB_NAME="${DB_NAME:-gestao_ativos}"
DB_PASSWORD="${DB_PASSWORD:-postgres}"
export DATABASE_URL="${DATABASE_URL:-postgresql+asyncpg://postgres:${DB_PASSWORD}@127.0.0.1:5432/${DB_NAME}}"

echo "Iniciando PostgreSQL..."
/etc/init.d/postgresql start 2>/dev/null || true

echo "Aguardando o banco ficar pronto..."
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  [ -S /var/run/postgresql/.s.PGSQL.5432 ] && break
  sleep 1
done

echo "Garantindo banco de dados '$DB_NAME' e senha do usuário postgres..."
su postgres -c "psql -tAc \"SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'\"" | grep -q 1 \
  || su postgres -c "createdb '$DB_NAME'"
su postgres -c "psql -c \"ALTER USER postgres PASSWORD '$DB_PASSWORD'\""

stop_postgres() {
  echo "Parando o PostgreSQL..."
  /etc/init.d/postgresql stop 2>/dev/null || true
}
trap stop_postgres TERM INT

echo "Aplicando migrações (alembic)..."
alembic upgrade head

echo "Iniciando API na porta ${PORT:-8000}..."
uvicorn src.api.main:app --host 0.0.0.0 --port "${PORT:-8000}" &
UV_PID=$!
wait "$UV_PID"