# 02 — Arquitetura

> Fonte: seção 7 do documento de requisitos. Decisões marcadas com **[ADR]** foram tomadas na criação da estrutura inicial e podem ser revistas pela equipe.

## Visão em camadas (Monólito Modular)

```
┌──────────────────────────────────────────────────────────────────┐
│ Apresentação — React + Vite + TypeScript (SPA responsiva)        │
│   • REST/HTTPS → FastAPI                                          │
│   • Supabase SDK → somente sessão (login) e realtime              │
└──────────────┬───────────────────────────────────────────────────┘
               │ Authorization: Bearer <JWT do Supabase>
┌──────────────▼───────────────────────────────────────────────────┐
│ API / Aplicação — FastAPI + Pydantic (OpenAPI automático)         │
│   router.py  → valida entrada/saída, verifica perfil              │
│   service.py → regras de negócio (sem import de FastAPI)          │
│   repository.py → SQLAlchemy async                                │
│   ── transversais: auth (deps), auditoria (AuditoriaService)      │
└──────────────┬───────────────────────────────────────────────────┘
               │ asyncpg
┌──────────────▼───────────────────────────────────────────────────┐
│ Supabase — PostgreSQL + RLS + Storage + Auth                      │
│   • log_auditoria append-only (trigger)                           │
│   • job_certificado (fila)                                        │
└──────────────▲───────────────────────────────────────────────────┘
               │
┌──────────────┴───────────────────────────────────────────────────┐
│ Worker de certificados (Python) — WeasyPrint + pikepdf + qrcode   │
│   consome job_certificado, gera PDF/A, envia ao Supabase Storage   │
└──────────────────────────────────────────────────────────────────┘
```

## Estrutura do repositório

```
.
├── backend/                 # FastAPI + worker (Python 3.12)
│   ├── app/
│   │   ├── main.py          # cria a app, registra routers e handlers
│   │   ├── core/            # config, banco, segurança (JWT), deps, exceções
│   │   └── modules/         # um pacote por módulo do documento (7.2)
│   │       └── <modulo>/    # models.py · schemas.py · repository.py · service.py · router.py
│   ├── worker/              # fila de emissão de certificados
│   └── tests/
├── frontend/                # React + Vite + TS
│   └── src/
│       ├── auth/            # sessão Supabase + perfil vindo de /auth/me
│       ├── layouts/         # layout por área (admin/coord/participante)
│       ├── pages/           # telas T01–T17
│       └── lib/             # cliente da API e do Supabase
├── supabase/
│   ├── migrations/          # FONTE DA VERDADE do schema (tabelas, RLS, triggers)
│   └── seed.sql
└── docs/
```

O módulo `backend/app/modules/instituicoes` é a **implementação de referência** (CRUD completo, RN 1.1, testes). Os demais módulos devem copiar esse padrão.

## Stack

| Camada | Tecnologia |
|---|---|
| Frontend | React 18/19, Vite, TypeScript, React Router, TanStack Query, `@supabase/supabase-js`, Vitest |
| API | FastAPI, Pydantic v2, pydantic-settings, Uvicorn |
| Domínio/Persistência | Python puro (services) + SQLAlchemy 2 async + asyncpg |
| Banco/Arquivos/Auth | Supabase (PostgreSQL, RLS, Storage, Auth) |
| Certificados | WeasyPrint (HTML→PDF), pikepdf (PDF/A), qrcode |
| Qualidade | pytest, pytest-cov, ruff, Vitest, GitHub Actions |

## Decisões

**[ADR-01] Schema versionado em `supabase/migrations` (SQL), não em Alembic.**
RLS, triggers de imutabilidade e policies são SQL nativo do Postgres/Supabase; manter tudo num único lugar evita duas fontes de verdade. Os models SQLAlchemy apenas *mapeiam* as tabelas existentes. Novas mudanças: `npx supabase migration new <nome>`.

**[ADR-02] Login acontece no frontend via Supabase Auth; o backend apenas valida o JWT.**
O documento sugere `POST /auth/login`; na prática o Supabase já entrega login, recuperação de senha e refresh de token. O backend expõe `GET /auth/me` (dados + perfil) e valida o token em toda requisição (`core/security.py`). Suporta JWT HS256 (segredo do projeto) ou chaves assimétricas via JWKS.

**[ADR-03] Escritas sempre pela API; RLS como segunda barreira.**
A API conecta com um papel que ignora RLS e aplica as regras de negócio. O RLS existe para que o acesso direto pelo SDK (chave `anon`/`authenticated`) só consiga **ler** o que é do próprio usuário (necessário para realtime) e **nunca escrever**.

**[ADR-04] Fila de certificados usando o próprio Postgres (`job_certificado` + `FOR UPDATE SKIP LOCKED`).**
Atende "fila assíncrona sem bloquear a API" sem adicionar Redis/RabbitMQ. Se a carga crescer, troca-se por arq/Celery sem mudar a API (RNF-003).

**[ADR-05] Perfil global guardado em `pessoa.perfil`; vínculo com evento em `coordenador_evento`.**
`pessoa.user_id` aponta para `auth.users`. Pessoas sem login (palestrante externo cadastrado pelo coordenador) têm `user_id` nulo.

**[ADR-06] CPF cifrado na aplicação + hash para deduplicação.**
Supabase já cifra o disco (AES-256). Para RNF-007, o CPF é guardado cifrado (`cpf_cifrado`) e um HMAC (`cpf_hash`) permite verificar duplicidade (RN 8.3) sem decifrar.

**[ADR-07] Worker roda em Docker.**
WeasyPrint depende de Pango/GTK, que é difícil de instalar no Windows. A API roda nativamente; o worker roda via `docker compose up worker`.

**[ADR-08] Kit visual do frontend baseado em Mantine.**
O frontend adota Mantine em tema exclusivamente claro, com azul institucional `#0B5394`, tipografia de sistema e componentes acessíveis. O ponto de entrada fornece `MantineProvider`, `ModalsProvider` e um único contêiner de notificações. O kit em `frontend/src/components` contém `Botao`, `CampoFormulario`, `Tabela`, `Modal`, `notificar` e `PageLayout`. Novas telas devem consumir esse kit antes de usar primitivas Mantine diretamente; primitivas só são usadas na composição estrutural quando o kit ainda não oferece uma abstração adequada. Isso mantém os contratos visuais e de acessibilidade consistentes sem transformar componentes de domínio em componentes globais.

## Fluxos transversais

### Autenticação/Autorização
1. Frontend faz login com `supabase.auth.signInWithPassword`.
2. Toda chamada à API envia `Authorization: Bearer <access_token>`.
3. `core/security.py` valida assinatura/expiração e extrai `sub` (id do usuário).
4. `core/deps.py::get_current_user` busca a `pessoa` do usuário e o perfil.
5. Rotas usam `Depends(require_perfil(Perfil.ADMINISTRADOR))` ou checam vínculo com o evento no service.

### Auditoria
- `AuditoriaService.registrar(...)` é chamado **dentro da mesma transação** da ação de impacto (garante que não existe ação sem log).
- A tabela `log_auditoria` tem trigger `BEFORE UPDATE OR DELETE OR TRUNCATE` que lança exceção.
- Justificativa é obrigatória para indeferimento, cancelamento administrativo, ajuste manual de presença e reemissão (RN 10.1).

### Emissão de certificados
1. Coordenador clica "Iniciar apuração final" → evento vai para `em_apuracao`.
2. `POST /eventos/{id}/certificados/lote` calcula elegíveis e cria um `job_certificado`.
3. Worker pega o job (`SKIP LOCKED`), gera HTML → PDF (WeasyPrint) → PDF/A (pikepdf) com QR Code apontando para `/validar/{codigo}`.
4. Upload no bucket `certificados`, grava `certificado` (status `emitido`) e o log de auditoria.
5. Frontend acompanha o progresso via realtime em `job_certificado`.

## Ambientes e variáveis

Ver `backend/.env.example` e `frontend/.env.example`. Nunca commitar `.env`.
