# Especificação — Gestão de Ativos em Obras

## Building blocks

- **Autenticação** (`auth`) — automatizável 5/5 — evidência: cadastr (actors); conta (domains); usuário (entities); cadastr (business_rules); cadastr (workflows); cadastr (permissions); login (features); usuário (nfrs); login (constraints)
- **CRUD das entidades** (`crud`) — automatizável 5/5 — evidência: presença de entidades
- **Busca** (`search`) — automatizável 5/5 — evidência: filtro (constraints)
- **Upload de arquivos** (`upload`) — automatizável 5/5 — evidência: arquivo (entities); arquivo (business_rules); arquivo (workflows); arquivo (constraints)
- **Dashboard** (`dashboard`) — automatizável 4/5 — evidência: painel (workflows); painel (features); dashboard (constraints)
- **Jobs em background** (`jobs`) — automatizável 4/5 — evidência: diariament (problem)
- **Notificações** (`notificacoes`) — automatizável 4/5 — evidência: alerta (business_rules)
- **Papéis e permissões (RBAC)** (`rbac`) — automatizável 4/5 — evidência: administrador (problem); administrador (actors); administrador (business_rules); administrador (workflows); administrador (permissions); administrador (features); administrador (nfrs)
- **Cobrança / planos** (`billing`) — automatizável 3/5 — evidência: pagament (integrations)
- **Workflow / máquina de estados** (`workflow`) — automatizável 3/5 — evidência: status (problem); status (entities); status (business_rules); status (workflows); status (constraints)

## Transparência do build

- **sai automático**: auth, crud, search, upload, dashboard, jobs, notificacoes, rbac
- **exige decisão**: billing, workflow
- **fora do escopo automático**: —
- **nota média de automação do produto**: 4.2/5

## Padrão Pegada de Silício — regras aplicadas ao projeto

**ARQ — Arquitetura e camadas**
- `ARQ-01` Backend em Python + FastAPI + SQLAlchemy + Alembic.
- `ARQ-02` Arquitetura Clean com isolamento de domínio, aplicação, infraestrutura e API.
- `ARQ-03` Injetar o serviço no controller e o banco no serviço — sem instanciar dependência dentro da regra de negócio.
- `ARQ-04` Toda regra de negócio, acesso a banco, autenticação e integração externa vive no backend. O frontend é apenas cliente da API.
- `ARQ-05` backend/src/{domain,application,infrastructure,api}, frontend/src/{components,pages,hooks,services}, storage/ e docker/.
- `ARQ-06` Frontend em React + Vite + Tailwind com TypeScript.

**API — Rotas, prefixo, health, CORS e contrato com o frontend**
- `API-01` Todas as rotas públicas sob uma base única, declarada em UM único lugar e consumida pelo frontend e pelo backend. Nunca declarar caminhos absolutos misturando com e sem o prefixo.
- `API-02` O health check (/api/health) responde sem credencial alguma e fica fora do grupo de rotas protegidas — Docker e infraestrutura o consultam antes de existir sessão.
- `API-03` CORS ergonômico em desenvolvimento local e restrito às origens explícitas do domínio real em produção. Nunca curinga combinado com credenciais.
- `API-04` Toda rota de aplicação exige sessão válida (Authorization: Bearer). Sem exceção além do health e do fluxo de login.
- `API-05` VITE_API_BASE_URL inclui o prefixo da API e os serviços acrescentam apenas o caminho relativo — nunca omitir o prefixo nem repeti-lo (…/api/api/…).
- `API-06` Login, cadastro, reset de senha e endpoints públicos têm rate limit; ao exceder, o backend responde 429.
- `API-07` Schemas de entrada validam tipo, tamanho e obrigatoriedade; payload inesperado é rejeitado antes de executar a regra de negócio.

**AUTH — Autenticação, sessão e senha**
- `AUTH-01` O projeto nasce com login e cadastro. Nenhuma chave estática no navegador, nenhum cenário sem autenticação — o token é emitido pelo backend, curto e com escopo definido.
- `AUTH-02` Senha armazenada apenas como hash bcrypt ou argon2 — nunca em texto nem com hash reversível.
- `AUTH-03` Token de sessão com expiração explícita; padrão de 1 hora, configurável por ambiente.
- `AUTH-04` Antes de executar qualquer regra de negócio, o backend valida assinatura, expiração e se o usuário está ativo.
- `AUTH-05` Resposta 401 provoca logout e limpeza de sessão no frontend, com redirecionamento para o login.
- `AUTH-06` User com id UUID, email único, password_hash, nome, ativo e timestamps de criação/atualização.
- `AUTH-07` POST /auth/register (409 se e-mail duplicado), POST /auth/token (access_token + token_type) e PUT /auth/password autenticada, exigindo confirmação da nova senha.
- `AUTH-08` Páginas /login e /register, contexto de autenticação com login/logout/atualizar senha e rota privada que redireciona quem não está autenticado.
- `AUTH-09` O segredo que assina os tokens existe apenas no backend, é obrigatório em produção e nunca chega ao bundle do navegador.

**SEG — Segredos, validação de entrada, abuso e logs**
- `SEG-01` Nenhum segredo, chave ou credencial hardcoded no código-fonte.
- `SEG-02` Variáveis do frontend carregam apenas configuração pública (URL base, idioma). Nunca segredo, chave, connection string ou token.
- `SEG-03` Connection string do banco, chaves de integração, credenciais de e-mail e tokens privados existem apenas no ambiente do backend.
- `SEG-04` Mensagem de erro amigável ao usuário, sem stack trace, JSON cru, caminho de campo interno ou nome de validação do framework.
- `SEG-05` Logs não contêm senha, token, connection string nem dado sensível; falhas de autenticação e rate limit são registradas com informação suficiente para auditoria.
- `SEG-06` Upload valida tamanho máximo e tipos permitidos antes de gravar.
- `SEG-07` Ações públicas sensíveis (cadastro, contato) consideram CAPTCHA/Turnstile quando o sistema está exposto.
- `SEG-08` O frontend nunca usa SDK, anon key ou service_role de terceiros (Supabase, Firebase e afins). Integração externa passa exclusivamente pelo backend.
- `SEG-09` O README lista as variáveis obrigatórias e como configurá-las, sem revelar nenhum valor real.

**DADOS — Banco, migrações, IDs e storage**
- `DADOS-01` Todo identificador de entidade é UUID — nunca sequencial exposto em rota (elimina acesso a registro alheio por troca do número na URL).
- `DADOS-02` Criação e alteração estrutural do banco sempre por migração Alembic, nunca alterando o esquema à mão.
- `DADOS-03` Antes de abrir a conexão ou rodar migração em banco de arquivo, garantir que o diretório pai existe.
- `DADOS-04` A pasta de dados do runtime nunca é criada ou editada manualmente no código: é onde ficam os dados sensíveis do usuário.
- `DADOS-05` Arquivos enviados ficam em subpasta por identificador da entidade de origem.
- `DADOS-06` Banco gerenciado é usado apenas como PostgreSQL via connection string (driver assíncrono), com SSL quando o provedor exigir; sem SDK do provedor.
- `DADOS-07` Existe teste garantindo que registros-chave não podem ser duplicados.
- `DADOS-08` As migrações executam com sucesso contra o banco de produção antes da entrega.

**UI — Frontend, responsividade, formatos e navegação**
- `UI-01` Todas as páginas, menus, formulários, tabelas, modais e ações principais continuam acessíveis e utilizáveis a partir de 360 px, preservando a funcionalidade da versão desktop.
- `UI-02` Navegação, colunas e espaçamentos se adaptam à largura; componente largo usa tratamento contido, nunca rolagem horizontal da página.
- `UI-03` Comunicação com o usuário via componente Modal do próprio design — nunca alert() ou confirm().
- `UI-04` Datas e horas exibidas no formato brasileiro, respeitando o fuso do Brasil.
- `UI-05` Números e valores monetários exibidos no padrão brasileiro.
- `UI-06` Campo de descrição oferece edição em markdown (negrito, títulos, listas), exibindo formatado e editando em texto puro.
- `UI-07` A página inicial autenticada é o dashboard, com menu lateral contendo as opções definidas nos requisitos visuais do projeto.
- `UI-08` Menu lateral apenas em páginas internas/administrativas. Landing, login e fluxos de entrada não usam sidebar.
- `UI-09` Cores, tipografia, modo (claro/escuro) e espaçamento seguem os requisitos visuais declarados no Product Model.
- `UI-10` O frontend recebe configuração apenas por variáveis públicas do Vite; nada de segredo.
- `UI-11` Interface sem os marcadores visuais de "conteúdo de IA": fundo de página com cor SÓLIDA (nenhum degradê de superfície), bordas e sombras NEUTRAS (sem tonalidade colorida, sem glow — o acento da marca entra como cor de ação, nunca como luz), e gradiente permitido somente quando FUNCIONAL (ex.: régua de progresso). Verificação automática: no HTML servido, nenhum `box-shadow` de luz colorida e nenhum gradiente no fundo da página; só gradientes funcionais sobram (smoke `scripts/smoke_contexto_ui.py` no Pegada, ou `grep -c gradient` + lista de exceções).

**INFRA — Docker, compose, portas e entrega em VPS**
- `INFRA-01` Dockerfile dedicado para backend e para frontend.
- `INFRA-02` Um docker compose na raiz sobe backend, frontend e banco do zero, sem passo manual.
- `INFRA-03` Volume de storage compartilhado com o host por bind mount, usando a pasta do projeto como ponto de montagem.
- `INFRA-04` O frontend só sobe depois do health check da API passar; a imagem do backend traz a ferramenta de checagem instalada.
- `INFRA-05` Portas e URLs vêm de variáveis de ambiente. O backend não usa a porta 80; o frontend usa porta alta.
- `INFRA-06` A imagem do backend cria o diretório de dados antes de iniciar, sem gravar dado sensível dentro da imagem.
- `INFRA-07` Build do frontend servido por nginx em imagem multi-stage.
- `INFRA-08` O pacote entregue é dockerizado e implantável em VPS alugada: compose, template de variáveis de ambiente e README de deploy, sem dependência da plataforma Pegada.
- `INFRA-09` O README explica como rodar em desenvolvimento e em produção, incluindo configuração de variáveis e comandos.

**PROC — Processo de build, testes e validação final**
- `PROC-01` Executar na ordem: ler especificação do produto, criar estrutura, implementar backend em camadas, implementar frontend, configurar Docker, escrever README e validar.
- `PROC-02` Testes unitários das entidades e validações de campo no backend.
- `PROC-03` O build do frontend passa (checagem de tipos + build) sem erro.
- `PROC-04` Antes de considerar pronto: backend inicia, frontend compila, migrações rodam, compose sobe, nenhum segredo no bundle, rotas privadas exigem sessão, CORS de produção configurável e rate limit presente.
- `PROC-05` Arquivos de ambiente reais e dados de runtime nunca entram no repositório; apenas templates.
- `PROC-06` O projeto gerado carrega seus próprios scripts de verificação (contratos de segurança e experiência) para checar o padrão no código.

**PAC — Pacote de entrega e prompt por agente**
- `PAC-01` O pacote contém a especificação do produto, o prompt de build, o README e os documentos de padrão (técnico, segurança, login, docker, banco).
- `PAC-02` O prompt de build existe para o agente que o dono escolher (Claude, Codex, OpenCode), sem prender o projeto a um fornecedor.
- `PAC-03` A especificação entregue ao usuário não carrega metadado interno do gerador (perfil, caminho escolhido, identificadores internos).
- `PAC-04` Diretórios de runtime do pacote são preservados com arquivo de ignore, para o projeto nascer com a estrutura completa.
- `PAC-05` Existe um único caminho de geração: SaaS completo de produção. Não há escolha de perfil MVP nem variação sem autenticação.
- `PAC-06` O pacote roda fora da plataforma: código no repositório do dono, infraestrutura dele, provedor de IA dele. Nenhuma dependência obrigatória do Pegada.

## Dados

- `ativo` — Ativo (veículo): identificação, status
- `obra` — Obra (local): nome, localização
- `usuario` — Usuário: nome, perfil, obra vinculada
- `lancamento_diario` — Lançamento diário: data, ativo, obra, status de uso, informações do dia, ativo (código), descrição, tipo, fabricante, modelo, horímetro inicial, horímetro final, total horas, km inicial, km final, total km, descritivo de manutenção e outros, status, condição climática
- `arquivo_de_propriedade` — Arquivo de propriedade (lista de ativos da empresa): ativo, status

## Perguntas em aberto (não são requisitos)

- Como você imagina o visual das telas além da logo (cores, estilo, algo que devamos registrar)?

## Próximos passos

1. Decidir em conversa: Cobrança / planos, Workflow / máquina de estados
2. Obter credenciais das integrações obrigatórias: não se aplica: o sistema não terá pagamentos
3. Build: gerar o código com o agente escolhido (prompt_*.md do pacote)
4. Publicar: docker-compose na infra do dono (sem depender da plataforma)