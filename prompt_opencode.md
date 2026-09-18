You are a senior engineer building the system described below, end to end.

# Gestão de Ativos em Obras — Sistema web para controle diário de veículos alocados nas obras da empresa

## Problema
A empresa precisa controlar os veículos (ativos) que ficam alocados em obras diferentes, registrando diariamente onde cada ativo está e seu status de uso, e o administrador precisa verificar se todos os ativos estão alocados e detectar lançamentos duplicados (mesmo veículo em duas obras no mesmo dia)

## Building blocks a implementar
- Autenticação (auth) — automatizável 5/5
- CRUD das entidades (crud) — automatizável 5/5
- Busca (search) — automatizável 5/5
- Upload de arquivos (upload) — automatizável 5/5
- Dashboard (dashboard) — automatizável 4/5
- Jobs em background (jobs) — automatizável 4/5
- Notificações (notificacoes) — automatizável 4/5
- Papéis e permissões (RBAC) (rbac) — automatizável 4/5
- Cobrança / planos (billing) — automatizável 3/5 — EXIGE DECISÃO: Cobrança / planos
- Workflow / máquina de estados (workflow) — automatizável 3/5 — EXIGE DECISÃO: Workflow / máquina de estados

## Dados (tabelas)
- Ativo (veículo) (tabela `ativo`): identificação, status
- Obra (local) (tabela `obra`): nome, localização
- Usuário (tabela `usuario`): nome, perfil, obra vinculada
- Lançamento diário (tabela `lancamento_diario`): data, ativo, obra, status de uso, informações do dia, ativo (código), descrição, tipo, fabricante, modelo, horímetro inicial, horímetro final, total horas, km inicial, km final, total km, descritivo de manutenção e outros, status, condição climática
- Arquivo de propriedade (lista de ativos da empresa) (tabela `arquivo_de_propriedade`): ativo, status

## Regras de negócio
- quando um ativo cadastrado não estiver alocado em nenhuma obra no dia, então o sistema deve sinalizar isso ao administrador
- quando o mesmo veículo for lançado em duas obras no mesmo dia, então o sistema deve detectar e alertar a duplicidade
- quando um usuário de obra acessar os lançamentos, então só pode ver os registros da sua própria localidade
- quando o sistema consolidar os registros diários, então deve comparar a lista de ativos da empresa (arquivo de propriedade) com os registros do dia e apontar as divergências (ativo lançado em duas obras no mesmo dia; ativo da lista que não está registrado em nenhuma obra)
- quando a coluna "Status" do diário da obra estiver preenchida com O, D, P, C ou R, então o sistema considera o ativo como alocado na obra
- quando houver item no diário que não consta no arquivo de propriedade, então o sistema deve incluir o item no arquivo de propriedade identificado com status L (Locado)
- quando o usuário tentar salvar o registro diário, então o sistema só deve permitir se todos os campos estiverem preenchidos, exceto o campo "Descritivo de Manutenção e Outros", que não é obrigatório
- quando o sistema for consolidar (comparar ativos da empresa com os dias lançados), então só deve processar dias menores ou iguais ao dia anterior (ex.: sendo hoje 15/09/2026, processa apenas de 01/09/2026 até 15/09/2026)
- quando alguma obra não tiver efetuado o registro de um dia, então o sistema não pode processar esse dia (pois faltam informações para verificar a totalidade) e deve informar o usuário, identificando as obras sem lançamento

## Padrão Pegada de Silício — regras do projeto (as marcadas "recomendada" são boas práticas;
o restante é não negociável)
### ARQ — Arquitetura e camadas
- [ARQ-01] Backend em Python + FastAPI + SQLAlchemy + Alembic.
- [ARQ-02] Arquitetura Clean com isolamento de domínio, aplicação, infraestrutura e API.
- [ARQ-03] Injetar o serviço no controller e o banco no serviço — sem instanciar dependência dentro da regra de negócio.
- [ARQ-04] Toda regra de negócio, acesso a banco, autenticação e integração externa vive no backend. O frontend é apenas cliente da API.
- [ARQ-05] backend/src/{domain,application,infrastructure,api}, frontend/src/{components,pages,hooks,services}, storage/ e docker/. (recomendada)
- [ARQ-06] Frontend em React + Vite + Tailwind com TypeScript.

### API — Rotas, prefixo, health, CORS e contrato com o frontend
- [API-01] Todas as rotas públicas sob uma base única, declarada em UM único lugar e consumida pelo frontend e pelo backend. Nunca declarar caminhos absolutos misturando com e sem o prefixo.
- [API-02] O health check (/api/health) responde sem credencial alguma e fica fora do grupo de rotas protegidas — Docker e infraestrutura o consultam antes de existir sessão.
- [API-03] CORS ergonômico em desenvolvimento local e restrito às origens explícitas do domínio real em produção. Nunca curinga combinado com credenciais.
- [API-04] Toda rota de aplicação exige sessão válida (Authorization: Bearer). Sem exceção além do health e do fluxo de login.
- [API-05] VITE_API_BASE_URL inclui o prefixo da API e os serviços acrescentam apenas o caminho relativo — nunca omitir o prefixo nem repeti-lo (…/api/api/…).
- [API-06] Login, cadastro, reset de senha e endpoints públicos têm rate limit; ao exceder, o backend responde 429.
- [API-07] Schemas de entrada validam tipo, tamanho e obrigatoriedade; payload inesperado é rejeitado antes de executar a regra de negócio.

### AUTH — Autenticação, sessão e senha
- [AUTH-01] O projeto nasce com login e cadastro. Nenhuma chave estática no navegador, nenhum cenário sem autenticação — o token é emitido pelo backend, curto e com escopo definido.
- [AUTH-02] Senha armazenada apenas como hash bcrypt ou argon2 — nunca em texto nem com hash reversível.
- [AUTH-03] Token de sessão com expiração explícita; padrão de 1 hora, configurável por ambiente.
- [AUTH-04] Antes de executar qualquer regra de negócio, o backend valida assinatura, expiração e se o usuário está ativo.
- [AUTH-05] Resposta 401 provoca logout e limpeza de sessão no frontend, com redirecionamento para o login.
- [AUTH-06] User com id UUID, email único, password_hash, nome, ativo e timestamps de criação/atualização.
- [AUTH-07] POST /auth/register (409 se e-mail duplicado), POST /auth/token (access_token + token_type) e PUT /auth/password autenticada, exigindo confirmação da nova senha.
- [AUTH-08] Páginas /login e /register, contexto de autenticação com login/logout/atualizar senha e rota privada que redireciona quem não está autenticado. (recomendada)
- [AUTH-09] O segredo que assina os tokens existe apenas no backend, é obrigatório em produção e nunca chega ao bundle do navegador.

### SEG — Segredos, validação de entrada, abuso e logs
- [SEG-01] Nenhum segredo, chave ou credencial hardcoded no código-fonte.
- [SEG-02] Variáveis do frontend carregam apenas configuração pública (URL base, idioma). Nunca segredo, chave, connection string ou token.
- [SEG-03] Connection string do banco, chaves de integração, credenciais de e-mail e tokens privados existem apenas no ambiente do backend.
- [SEG-04] Mensagem de erro amigável ao usuário, sem stack trace, JSON cru, caminho de campo interno ou nome de validação do framework.
- [SEG-05] Logs não contêm senha, token, connection string nem dado sensível; falhas de autenticação e rate limit são registradas com informação suficiente para auditoria.
- [SEG-06] Upload valida tamanho máximo e tipos permitidos antes de gravar. (recomendada; aplica quando: quando o projeto tem upload)
- [SEG-07] Ações públicas sensíveis (cadastro, contato) consideram CAPTCHA/Turnstile quando o sistema está exposto. (recomendada; aplica quando: quando exposto publicamente)
- [SEG-08] O frontend nunca usa SDK, anon key ou service_role de terceiros (Supabase, Firebase e afins). Integração externa passa exclusivamente pelo backend.
- [SEG-09] O README lista as variáveis obrigatórias e como configurá-las, sem revelar nenhum valor real. (recomendada)

### DADOS — Banco, migrações, IDs e storage
- [DADOS-01] Todo identificador de entidade é UUID — nunca sequencial exposto em rota (elimina acesso a registro alheio por troca do número na URL).
- [DADOS-02] Criação e alteração estrutural do banco sempre por migração Alembic, nunca alterando o esquema à mão.
- [DADOS-03] Antes de abrir a conexão ou rodar migração em banco de arquivo, garantir que o diretório pai existe. (aplica quando: banco em arquivo)
- [DADOS-04] A pasta de dados do runtime nunca é criada ou editada manualmente no código: é onde ficam os dados sensíveis do usuário.
- [DADOS-05] Arquivos enviados ficam em subpasta por identificador da entidade de origem. (recomendada; aplica quando: quando o projeto tem upload)
- [DADOS-06] Banco gerenciado é usado apenas como PostgreSQL via connection string (driver assíncrono), com SSL quando o provedor exigir; sem SDK do provedor. (aplica quando: quando o banco é gerenciado)
- [DADOS-07] Existe teste garantindo que registros-chave não podem ser duplicados. (recomendada)
- [DADOS-08] As migrações executam com sucesso contra o banco de produção antes da entrega.

### UI — Frontend, responsividade, formatos e navegação
- [UI-01] Todas as páginas, menus, formulários, tabelas, modais e ações principais continuam acessíveis e utilizáveis a partir de 360 px, preservando a funcionalidade da versão desktop.
- [UI-02] Navegação, colunas e espaçamentos se adaptam à largura; componente largo usa tratamento contido, nunca rolagem horizontal da página.
- [UI-03] Comunicação com o usuário via componente Modal do próprio design — nunca alert() ou confirm().
- [UI-04] Datas e horas exibidas no formato brasileiro, respeitando o fuso do Brasil.
- [UI-05] Números e valores monetários exibidos no padrão brasileiro.
- [UI-06] Campo de descrição oferece edição em markdown (negrito, títulos, listas), exibindo formatado e editando em texto puro. (recomendada; aplica quando: quando há campo de descrição)
- [UI-07] A página inicial autenticada é o dashboard, com menu lateral contendo as opções definidas nos requisitos visuais do projeto.
- [UI-08] Menu lateral apenas em páginas internas/administrativas. Landing, login e fluxos de entrada não usam sidebar. (recomendada)
- [UI-09] Cores, tipografia, modo (claro/escuro) e espaçamento seguem os requisitos visuais declarados no Product Model.
- [UI-10] O frontend recebe configuração apenas por variáveis públicas do Vite; nada de segredo.
- [UI-11] Interface sem os marcadores visuais de "conteúdo de IA": fundo de página com cor SÓLIDA (nenhum degradê de superfície), bordas e sombras NEUTRAS (sem tonalidade colorida, sem glow — o acento da marca entra como cor de ação, nunca como luz), e gradiente permitido somente quando FUNCIONAL (ex.: régua de progresso). Verificação automática: no HTML servido, nenhum `box-shadow` de luz colorida e nenhum gradiente no fundo da página; só gradientes funcionais sobram (smoke `scripts/smoke_contexto_ui.py` no Pegada, ou `grep -c gradient` + lista de exceções).

### INFRA — Docker, compose, portas e entrega em VPS
- [INFRA-01] Dockerfile dedicado para backend e para frontend.
- [INFRA-02] Um docker compose na raiz sobe backend, frontend e banco do zero, sem passo manual.
- [INFRA-03] Volume de storage compartilhado com o host por bind mount, usando a pasta do projeto como ponto de montagem.
- [INFRA-04] O frontend só sobe depois do health check da API passar; a imagem do backend traz a ferramenta de checagem instalada.
- [INFRA-05] Portas e URLs vêm de variáveis de ambiente. O backend não usa a porta 80; o frontend usa porta alta.
- [INFRA-06] A imagem do backend cria o diretório de dados antes de iniciar, sem gravar dado sensível dentro da imagem. (recomendada)
- [INFRA-07] Build do frontend servido por nginx em imagem multi-stage. (recomendada)
- [INFRA-08] O pacote entregue é dockerizado e implantável em VPS alugada: compose, template de variáveis de ambiente e README de deploy, sem dependência da plataforma Pegada.
- [INFRA-09] O README explica como rodar em desenvolvimento e em produção, incluindo configuração de variáveis e comandos.

### PROC — Processo de build, testes e validação final
- [PROC-01] Executar na ordem: ler especificação do produto, criar estrutura, implementar backend em camadas, implementar frontend, configurar Docker, escrever README e validar. (recomendada)
- [PROC-02] Testes unitários das entidades e validações de campo no backend. (recomendada)
- [PROC-03] O build do frontend passa (checagem de tipos + build) sem erro.
- [PROC-04] Antes de considerar pronto: backend inicia, frontend compila, migrações rodam, compose sobe, nenhum segredo no bundle, rotas privadas exigem sessão, CORS de produção configurável e rate limit presente.
- [PROC-05] Arquivos de ambiente reais e dados de runtime nunca entram no repositório; apenas templates.
- [PROC-06] O projeto gerado carrega seus próprios scripts de verificação (contratos de segurança e experiência) para checar o padrão no código. (recomendada)

### PAC — Pacote de entrega e prompt por agente
- [PAC-01] O pacote contém a especificação do produto, o prompt de build, o README e os documentos de padrão (técnico, segurança, login, docker, banco).
- [PAC-02] O prompt de build existe para o agente que o dono escolher (Claude, Codex, OpenCode), sem prender o projeto a um fornecedor.
- [PAC-03] A especificação entregue ao usuário não carrega metadado interno do gerador (perfil, caminho escolhido, identificadores internos). (recomendada)
- [PAC-04] Diretórios de runtime do pacote são preservados com arquivo de ignore, para o projeto nascer com a estrutura completa. (recomendada)
- [PAC-05] Existe um único caminho de geração: SaaS completo de produção. Não há escolha de perfil MVP nem variação sem autenticação.
- [PAC-06] O pacote roda fora da plataforma: código no repositório do dono, infraestrutura dele, provedor de IA dele. Nenhuma dependência obrigatória do Pegada.

## Perguntas EM ABERTO (não implementar como requisito)
- Como você imagina o visual das telas além da logo (cores, estilo, algo que devamos registrar)?

Cada pergunta em aberto é uma pergunta ao usuário, NÃO um requisito: implemente só o que está especificado.

## Stack obrigatória
- Backend: FastAPI (Python) — rotas sob /api, /api/health público
- Frontend: React + Vite — responsivo (celular e desktop obrigatórios)
- Banco: PostgreSQL (migrations versionadas)
- Deploy: Docker + docker-compose local (infra do próprio dono)

## Critérios de aceite
1. Todos os endpoints sob /api, com /api/health público e sem autenticação.
2. Login funcional com papéis/permissões exatamente como especificado.
3. Todas as entidades acima com CRUD e validações das regras de negócio.
4. Interface responsiva: telas, menus, tabelas, formulários e modais usáveis no celular.
5. docker-compose sobe o sistema completo do zero, com migrations.
6. .gitignore correto (Python/FastAPI + React/Vite); nenhum segredo no repositório.
7. O projeto roda na infraestrutura do dono, sem dependência de serviço do Pegada.
8. Identificadores são UUID, nunca sequenciais expostos em rota (DADOS-01).
9. Frontend e backend consomem a mesma base de API, declarada em um único lugar (API-01, API-05).
10. CORS restrito por origem em produção (API-03); health responde sem credencial (API-02);
    o frontend não guarda segredo nem fala com banco/SDK externa (SEG-02, SEG-08).
11. O projeto entrega dockerizado, pronto para VPS (INFRA-02, INFRA-08), com README de deploy.
