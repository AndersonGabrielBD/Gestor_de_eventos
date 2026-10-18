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
| [04 — Regras de negócio](docs/04-regras-de-negocio.md) | RN 1.1–10.3 reconstruídas (⚠️ validar) |
| [05 — API](docs/05-api.md) | Endpoints planejados |
| [06 — Frontend](docs/06-frontend.md) | Rotas e telas T01–T17 |
| [07 — Lacunas e perguntas](docs/07-lacunas-e-perguntas.md) | O que o PDF não define |
| [**Backlog**](docs/BACKLOG.md) | Épicos, itens GE-xxx, sprints |

## Stack

React + Vite + TypeScript · FastAPI + Pydantic · SQLAlchemy async · Supabase (PostgreSQL, Auth, Storage, RLS) · WeasyPrint + pikepdf + qrcode.

```
backend/    API FastAPI (app/) + worker de certificados (worker/)
frontend/   SPA React
supabase/   migrations (fonte da verdade do schema), seed e config local
docs/       documentação e backlog
```

## Como rodar localmente

Pré-requisitos: Python 3.12, Node 22, Docker Desktop.

### 1. Banco (Supabase local)

```bash
npx supabase start
```

Aplica `supabase/migrations` e `supabase/seed.sql`. Ao final, o comando mostra a `API URL`, a chave `anon`/publishable e o segredo JWT — use-os nos `.env` abaixo. Para recriar o banco do zero: `npx supabase db reset`. Painel: http://127.0.0.1:54323.

> Alternativa: usar um projeto Supabase na nuvem compartilhado pela equipe (GE-006) e aplicar as migrations com `npx supabase link` + `npx supabase db push`.

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

### 3. Worker de certificados

WeasyPrint precisa de bibliotecas de sistema, então o worker roda em Docker:

```bash
docker compose up worker
```

### 4. Frontend

```bash
cd frontend
npm install
copy .env.example .env.local    # preencha VITE_SUPABASE_ANON_KEY
npm run dev
```

App em http://localhost:5173.

### Criar o primeiro administrador

1. Crie um usuário pelo painel do Supabase (Authentication → Add user).
2. No SQL Editor, crie a pessoa vinculada:
   ```sql
   insert into pessoa (user_id, nome, email, perfil, categoria, consentimento_lgpd_em)
   select id, 'Admin', email, 'administrador', 'tecnico', now() from auth.users where email = 'seu@email.com';
   ```

## Fluxo de trabalho da equipe

- Pegue um item do [backlog](docs/BACKLOG.md) e crie a branch `feat/GE-xxx-descricao`.
- Novo módulo do backend: copie a estrutura de `backend/app/modules/instituicoes` (model → schema → repository → service → router + testes do service).
- Mudança no banco: `npx supabase migration new <nome>` e escreva o SQL; atualize o model SQLAlchemy correspondente.
- Abra PR para `main`; o CI (lint + testes + build) precisa passar e um colega revisa.
