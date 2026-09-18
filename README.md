# Gestão de Ativos em Obras

Sistema web para controle diário dos veículos e equipamentos (ativos) alocados às
obras de uma empresa. Permite registrar o lançamento diário de cada ativo, verificar
duplicidades e ativos não alocados, acompanhar o painel gerencial, receber
notificações e consolidar os dados do período de forma automática.

## Stack

| Camada | Tecnologia |
| ------ | ---------- |
| Frontend | React 18 · Vite · TypeScript · Tailwind CSS |
| Backend | Python 3.12+ · FastAPI · SQLAlchemy (async) · Alembic |
| Banco | PostgreSQL 16 |
| Infra | Docker · Docker Compose |
| Extras | APScheduler · slowapi (rate limit) · JWT (python-jose) · bcrypt |

## Funcionalidades

- **Autenticação & RBAC**: login/registro com JWT; perfis `admin` (visão global) e
  `obra` (escopo limitado à sua obra); rate limit em rotas de autenticação.
- **CRUD de entidades**: usuários (admin), obras, ativos, lançamentos diários,
  arquivo de propriedade, notificações.
- **Regras de negócio**:
  - Status de locação: `O` (operando), `D` (disponível), `P` (parado), `C` (em
    manutenção), `R` (reserva).
  - Detecção de duplicidade: mesmo ativo lançado em mais de uma obra na mesma data.
  - Usuários de obra só registram/veem dados da própria obra.
  - Lançamento exige todos os campos exceto `descritivo_manutencao`.
  - Ativos lançados são incluídos automaticamente no arquivo de propriedade
    (`status = L`).
- **Busca**: filtros por termo em ativos e obras.
- **Upload**: importação de arquivos (CSV/XLSX/PDF/PDF/imagens) com validação de
  extensão e tamanho.
- **Dashboard**: totais, ativos alocados/não alocados, duplicidades do dia e
  últimos lançamentos.
- **Jobs em background**: consolidação diária automática (23:30) que identifica
  obras sem registro, ativos não alocados e duplicidades, gerando notificações ao
  admin.
- **Notificações**: central de notificações com contador de não lidas e ação
  "marcar todas como lidas".

## Requisitos

- Docker 20.10+ com Docker Compose v2
- (Opcional) Python 3.12+ e Node 20+ para desenvolvimento local

## Execução com Docker

```bash
# 1. Configure as variáveis de ambiente
cp .env.example .env
#    Edite SECRET_KEY com um valor forte em produção!

# 2. Suba a aplicação
docker compose up -d --build

# 3. Acesse
#    Frontend: http://localhost:5173
#    API/docs: http://localhost:8000/docs
```

Usuário administrador inicial (criado automaticamente):

- **E-mail**: `admin@sistema.com`
- **Senha**: `admin123`

> Troque estas credenciais em produção via variáveis `ADMIN_EMAIL`/`ADMIN_PASSWORD`.

### Comandos úteis

```bash
docker compose logs -f backend     # logs da API
docker compose ps                  # status dos serviços
docker compose down                # para tudo
docker compose down -v             # para tudo e destrói o volume do banco
```

## Desenvolvimento local

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # Linux/macOS

pip install -r requirements.txt
pip install pytest pytest-asyncio

alembic upgrade head              # aplica migrações
uvicorn src.api.main:app --reload --port 8000
```

Para rodar localmente sem Docker, crie um `.env` na pasta `backend` apontando
`DATABASE_URL` para o seu Postgres e ajuste `STORAGE_PATH`.

### Frontend

```bash
cd frontend
npm install
npm run dev                        # http://localhost:5173
```

Em desenvolvimento o frontend chama a API em `http://localhost:8000/api` por padrão.
Ajuste com `VITE_API_BASE_URL` se necessário (produção usa `/api` via nginx).

### Testes

```bash
cd backend
.venv\Scripts\python.exe -m pytest tests -v
```

## Estrutura do projeto

```
gestaofrotas/
├── backend/
│   ├── alembic/                # migrações de banco
│   ├── src/
│   │   ├── api/                # routers, schemas, dependencies, rate_limit
│   │   ├── application/        # services (casos de uso e regras de negócio)
│   │   ├── infrastructure/     # database, repositories, security, jobs, storage
│   │   └── config.py
│   ├── tests/                  # testes unitários (auth, regras de negócio)
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/         # ui (Button, Modal, Badge...) e layout (Sidebar, Header)
│       ├── hooks/              # useAuth, useAtivos, useObras, useUI, ...
│       ├── pages/              # Dashboard, Ativos, Obras, Lançamentos, ...
│       ├── services/           # clientes HTTP (axios)
│       └── types/
├── storage/uploads/            # arquivos enviados (volume docker)
├── docker-compose.yml
├── .env.example
└── README.md
```

## Variáveis de ambiente

| Variável | Padrão | Descrição |
| -------- | ------ | --------- |
| `POSTGRES_USER` | `postgres` | Usuário do banco |
| `POSTGRES_PASSWORD` | `postgres` | Senha do banco |
| `POSTGRES_DB` | `gestao_ativos` | Nome do banco |
| `DATABASE_URL` | `postgresql+asyncpg://...` | DSN usado pelo backend |
| `SECRET_KEY` | `change-me-in-production` | Segredo para assinar JWT (mude!) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Expiração do token |
| `CORS_ORIGINS` | `http://localhost:5173,...` | Origens permitidas (vírgula) |
| `STORAGE_PATH` | `/app/storage` | Pasta de uploads |
| `VITE_API_BASE_URL` | `/api` | Base da API para o frontend |
| `FRONTEND_PORT` | `5173` | Porta exposta do frontend |
| `ADMIN_EMAIL` | `admin@sistema.com` | E-mail do admin inicial |
| `ADMIN_PASSWORD` | `admin123` | Senha do admin inicial |

## API (principais rotas)

| Método | Rota | Descrição |
| ------ | ---- | --------- |
| POST | `/api/auth/token` | Login (JWT) |
| POST | `/api/auth/register` | Cadastro de usuário |
| GET | `/api/auth/me` | Usuário logado |
| GET/POST | `/api/ativos` | Listar/criar ativos |
| GET/POST | `/api/obras` | Listar/criar obras |
| GET/POST | `/api/usuarios` | Listar/criar usuários (admin) |
| GET/POST | `/api/lancamentos` | Listar/criar lançamentos diários |
| GET/POST | `/api/arquivo-propriedade` | Listar/criar registros de propriedade |
| GET | `/api/dashboard` | Resumo do painel |
| POST | `/api/consolidacao/executar` | Executa consolidação (admin) |
| POST | `/api/upload` | Upload de arquivo |
| GET | `/api/notificacoes` | Listar notificações |
| GET | `/api/health` | Health check |

Documentação interativa disponível em `http://localhost:8000/docs`.