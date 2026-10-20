# Sistema de Gestão de Eventos Institucionais

Plataforma para planejar, executar e certificar eventos acadêmicos: coordenadores cadastram eventos e atividades, participantes se inscrevem, a presença é registrada por check-in e os certificados são emitidos em PDF/A com validação pública por QR Code.

**Equipe:** Anderson Gabriel · José Nogueira · Pedro Santos · Thayná Carnaúba — Maceió/AL, 2026.

## Documentação

| Documento | Conteúdo |
|---|---|
| [Documento de requisitos (PDF)](Documento_Requisitos_Gestao_Eventos.pdf) | Documento oficial |
| [01 — Visão geral](docs/01-visao-geral.md) | Atores, RF/RNF, mapa RF ↔ UC ↔ telas ↔ módulos |
| [02 — Arquitetura](docs/02-arquitetura.md) | Camadas, stack, decisões (ADRs), fluxos de auth/auditoria/certificados |
| [03 — Modelo de dados](docs/03-modelo-de-dados.md) | Diagrama ER, tabelas, máquinas de estado |
| [04 — Regras de negócio](docs/04-regras-de-negocio.md) | RN 1.1–10.3 reconstruídas (✅ aprovadas pelo professor) |
| [05 — API](docs/05-api.md) | Endpoints planejados |
| [06 — Frontend](docs/06-frontend.md) | Rotas e telas T01–T17 |
| [07 — Lacunas e perguntas](docs/07-lacunas-e-perguntas.md) | O que o PDF não define |
| [**Backlog**](docs/BACKLOG.md) | Cards por sprint e responsáveis (espelho do Trello) |
| [**08 — Dependências**](docs/08-dependencias.md) | Quem depende de quem, por sprint, e prazos de entrega entre a equipe |

## Stack

React + Vite + TypeScript · FastAPI + Pydantic · SQLAlchemy async · Supabase (PostgreSQL, Auth, Storage, RLS) · WeasyPrint + pikepdf + qrcode.

```
backend/    API FastAPI (app/) + worker de certificados (worker/)
frontend/   SPA React
supabase/   migrations (fonte da verdade do schema), seed e config local
docs/       documentação e backlog
```

## Como rodar

Pré-requisitos: Python 3.12 e Node 22. O banco é o **projeto Supabase da equipe na nuvem**, então não precisa de Docker. O Docker só é usado pelo worker de certificados (veja o passo 4).

### 1. Chaves do projeto Supabase

Peça ao Anderson as chaves do projeto dev. Elas são enviadas por canal seguro e **nunca vão para o Git**. Você vai precisar de:

| Variável | Onde fica no painel do Supabase | Vai em |
|---|---|---|
| `SUPABASE_URL` / `VITE_SUPABASE_URL` | Project Settings → API → Project URL | backend e frontend |
| `VITE_SUPABASE_ANON_KEY` | Project Settings → API Keys → `anon` / publishable | frontend |
| `SUPABASE_SERVICE_ROLE_KEY` | Project Settings → API Keys → `service_role` / secret (**só no backend**) | backend |
| `DATABASE_URL` | Connect → **Session pooler** (porta 5432), trocando `postgresql://` por `postgresql+asyncpg://` | backend |

`SUPABASE_JWT_SECRET` fica vazio: o projeto assina os tokens com ES256 e a API valida pelas chaves públicas (JWKS).

⚠️ `CHAVE_CIFRAGEM_DADOS` e `CHAVE_HMAC_DADOS` também vêm do Anderson e **precisam ser as mesmas para todos**. O banco é compartilhado, e um CPF cifrado com uma chave não abre com outra.

### 2. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
copy .env.example .env          # Linux/macOS: cp .env.example .env  — preencha os valores
uvicorn app.main:app --reload
```

API em http://localhost:8000 · documentação interativa em http://localhost:8000/docs.

Testes e lint:

```bash
pytest --cov
ruff check . && ruff format --check .
```

### 3. Frontend

```bash
cd frontend
npm install
copy .env.example .env.local    # preencha VITE_SUPABASE_URL e VITE_SUPABASE_ANON_KEY
npm run dev
```

App em http://localhost:5173.

### 4. Worker de certificados (só quem mexe em PDF)

WeasyPrint precisa de bibliotecas de sistema, então o worker roda em Docker:

```bash
docker compose up worker
```

Com o banco na nuvem, defina `DATABASE_URL_DOCKER` com a mesma `DATABASE_URL` do `.env`.

### Usuários de teste

O projeto dev tem um usuário de cada perfil (administrador, coordenador, participante), criados com:

```bash
cd backend
python -m scripts.criar_usuarios_teste
```

Os e-mails estão em `backend/scripts/criar_usuarios_teste.py`. A senha é compartilhada pelo Anderson.

## Banco de dados (Supabase)

- **Schema:** `supabase/migrations` é a fonte da verdade (ADR-01). Toda conta criada no Auth ganha uma `pessoa` com perfil participante por trigger (`20261019000000_auth_cria_pessoa.sql`).
- **Mudança no banco:** `npx supabase migration new <nome>`, escreva o SQL e atualize o model SQLAlchemy correspondente. **Não altere migrations já aplicadas**, crie uma nova.
- **Aplicar no projeto dev** (quem tiver acesso ao projeto):
  ```bash
  npx supabase login
  npx supabase link --project-ref <ref-do-projeto>
  npx supabase db push
  ```
- **Configuração do Auth no painel** (Authentication → URL Configuration): Site URL `http://localhost:5173` e, em Redirect URLs, `http://localhost:5173/**` e a URL do deploy. Sem isso os links de confirmação e de recuperação de senha não voltam para o app.
- **Promover alguém a coordenador ou admin** (no MVP não tem tela, é pelo SQL Editor):
  ```sql
  update pessoa set perfil = 'administrador' where email = 'fulano@exemplo.com';
  ```

## Fluxo de trabalho da equipe

- Pegue um card do Trello (ver [backlog](docs/BACKLOG.md)) e crie a branch `feat/<nome-curto-do-card>`.
- Novo módulo do backend: copie a estrutura de `backend/app/modules/instituicoes` (model → schema → repository → service → router + testes do service).
- Abra PR para `main`; o CI (lint + testes + build) precisa passar e um colega revisa.
