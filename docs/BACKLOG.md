# Backlog — Sistema de Gestão de Eventos Institucionais

> Espelho do quadro do Trello **[Gestão de eventos APP](https://trello.com/b/FplztFY4/gest%C3%A3o-de-eventos-app)**.
> Cada card é uma **funcionalidade completa** (backend + tela + testes). As tarefas técnicas ficam no checklist **"Tarefas"** dentro do card no Trello; aqui fica a visão geral.
> Fonte de verdade do andamento: **o Trello**. Quem depende de quem: [08-dependencias.md](08-dependencias.md).

## Como ler

- **Tipo:** `[Feature]` funcionalidade · `[Infra]` ambiente/deploy · `[Qualidade]` testes/segurança · `[Doc]` documentação
- **Prioridade** (herdada do PDF): **E** = Essencial · **I** = Importante · **D** = Desejável
- **Pts** — estimativa relativa (1 pt ≈ meio dia de uma pessoa). Entre parênteses, o que ainda falta quando parte já está pronta.
- ⚠️ — depende de outro card **da mesma sprint** (ver [08-dependencias.md](08-dependencias.md))
- **Branch:** `feat/<nome-curto-do-card>` (ex.: `feat/criar-evento`). Cite o nome do card no PR.

### Definição de Pronto (DoD)
1. Todos os itens do checklist "Tarefas" e os critérios de aceite do card concluídos.
2. Código revisado por pelo menos 1 colega (PR) e CI verde (lint + testes + build).
3. Testes automatizados das regras de negócio do card.
4. Ações de impacto gravam `log_auditoria` com responsável e justificativa.
5. Tela navegável por teclado, com `label` em todos os campos e responsiva.
6. Endpoints aparecem corretamente no `/docs` (OpenAPI).

---

## Equipe e divisão

4 pessoas fullstack, por fatia vertical (cada um faz backend + tela do próprio card). **Todo mundo tem trabalho em todas as sprints.**

| Pessoa | Perfil no projeto | Pts restantes |
|---|---|---|
| **Anderson** | Supabase/infra + base do sistema (conta → pessoa → evento) + LGPD + testes de carga/E2E | ~80 |
| **Thayná** | Frontend: componentes, telas de admin e do participante, inscrição, check-in, acessibilidade | ~72 |
| **Pedro** | Tipos de certificado, auditoria, atividades, gestão de inscritos, relatórios | ~66 |
| **José** | Infra de deploy/segurança/testes + certificados (motor PDF/A, apuração, emissão, reemissão) + catálogo | ~61 |

### Quem faz o quê em cada sprint (pts restantes)

| Sprint | Anderson | Thayná | Pedro | José |
|---|---|---|---|---|
| **S0** | Fundação + Ambiente + Login (19) | Componentes (5) | Tipos de certificado (6) | Validar RNs + Deploy (6) |
| **S1** | Cadastro de pessoa (15) | Instituições (5) | Auditoria (9) | Segurança + Testes de integração (8) |
| **S2** | Criar evento (23) | Coordenadores (6) | Atividades (16) | Motor de PDF/A (8) |
| **S3** | Privacidade LGPD (6) | Inscrição (22) | Minhas inscrições + Admin define perfil (9) | Catálogo (8) |
| **S4** | Teste de carga (4) | Check-in (23) | Gestão de inscritos (12) | Apuração final (15) |
| **S5** | Dashboard (8) | Meus certificados + Validação (6) | Relatórios (11) | Emissão em lote (8) |
| **S6** | E2E + cobertura 70% (5) | Acessibilidade (5) | Manual e apresentação (3) | Reemissão (8) |

> No Trello, o responsável aparece no fim do título do card (`· 👤 Nome`). Cada um deve clicar em **"Participar"** nos seus cards para aparecer o avatar.

---

## Plano de sprints (7 sprints de 2 semanas)

**Marco do MVP (fim da S5):** criar evento → inscrever → check-in → emitir certificado → validar publicamente.

| Sprint | Objetivo | Pts (estimativa total) |
|---|---|---|
| **S0** | Fundação, ambiente, login, componentes e deploy | ~61 |
| **S1** | Cadastros base, auditoria, segurança e testes de integração | ~49 |
| **S2** | Coordenador monta um evento completo + motor de PDF/A | ~53 |
| **S3** | Participante encontra o evento e se inscreve | ~45 |
| **S4** | Gestão de inscritos, check-in e apuração | ~54 |
| **S5** | Certificados emitidos, validação pública, relatórios e dashboard (**MVP**) | ~33 |
| **S6** | Reemissão, acessibilidade, E2E e entrega | ~21 |
| | **Total** (33 cards) | **~316** |

---

## Cards

### S0 — Fundação

| Card | Tipo | Pri | Pts | Responsável | Depende de |
|---|---|---|---|---|---|
| Fundação do projeto (estrutura, CI, schema do banco) — **Em review** | Infra | E | 18 (~1) | Anderson | — |
| Ambiente da equipe: Supabase compartilhado, local e worker em Docker | Infra | E | 7 | Anderson | Fundação |
| Login, cadastro de conta e recuperação de senha (T01) | Feature | E | 19 (~11) | Anderson | Fundação |
| Biblioteca de componentes acessível + ESLint/Prettier | Infra | I | 5 | Thayná | Fundação |
| Tela de Tipos de certificado (T04) | Feature | I | 6 | Pedro | Fundação · Componentes ⚠️ |
| Validar regras de negócio e lacunas com o professor | Doc | E | 1 | José | — |
| Deploy de homologação (API, frontend e worker) | Infra | I | 5 | José | Ambiente ⚠️ |

### S1 — Cadastros base

| Card | Tipo | Pri | Pts | Responsável | Depende de |
|---|---|---|---|---|---|
| Cadastro de pessoa e "Meu perfil" com consentimento LGPD | Feature | E | 15 | Anderson | Login |
| Tela de Instituições e Unidades (T03) — backend pronto | Feature | E | 13 (~5) | Thayná | Login · Componentes |
| Auditoria: consulta e exportação dos logs (T05) — registro pronto | Feature | I | 13 (~9) | Pedro | Login |
| Segurança: rate limit, headers e backup/restauração | Qualidade | E | 4 | José | Deploy |
| Testes de integração contra Postgres real | Qualidade | I | 4 | José | Ambiente |

### S2 — Evento

| Card | Tipo | Pri | Pts | Responsável | Depende de |
|---|---|---|---|---|---|
| Criar e gerenciar evento (T07) | Feature | E | 23 | Anderson | Login · Instituições (✅ endpoints) · Pessoa |
| Coordenadores do evento (T08) | Feature | E | 6 | Thayná | Criar evento ⚠️ · Pessoa |
| Programação / Atividades do evento (T09) | Feature | E | 16 | Pedro | Criar evento ⚠️ · Pessoa |
| Motor de PDF/A do certificado (template + QR Code + worker) | Feature | E | 8 | José | Ambiente |

### S3 — Inscrição

| Card | Tipo | Pri | Pts | Responsável | Depende de |
|---|---|---|---|---|---|
| Privacidade LGPD: solicitações do titular e anonimização | Feature | E | 6 | Anderson | Pessoa · Auditoria |
| Tela de inscrição do participante (T14) | Feature | E | 22 | Thayná | Pessoa · Criar evento · Atividades · Catálogo ⚠️ |
| Minhas inscrições e cancelamento (T15) | Feature | E | 6 | Pedro | Inscrição ⚠️ |
| Admin define o perfil do usuário | Feature | I | 3 | Pedro | Pessoa · Auditoria |
| Catálogo de eventos e página de detalhe (T13) | Feature | E | 8 | José | Criar evento · Atividades |

### S4 — Gestão, presença e apuração

| Card | Tipo | Pri | Pts | Responsável | Depende de |
|---|---|---|---|---|---|
| Teste de carga da inscrição (500 usuários) | Qualidade | I | 4 | Anderson | Inscrição · Deploy |
| Check-in e presença: modo lista e leitor de QR Code (T11) | Feature | E | 23 | Thayná | Inscrição · Gestão de inscritos ⚠️ |
| Gestão de inscritos: confirmar, indeferir e cancelar (T10) | Feature | E | 12 | Pedro | Inscrição · Auditoria |
| Apuração final: quem tem direito a certificado (T12) | Feature | E | 15 | José | Check-in ⚠️ · Tipos · Atividades · Criar evento |

### S5 — Certificados (MVP)

| Card | Tipo | Pri | Pts | Responsável | Depende de |
|---|---|---|---|---|---|
| Dashboard por perfil (T02) | Feature | I | 8 | Anderson | Criar evento · Inscrição · Emissão em lote ⚠️ |
| Meus certificados e validação pública por QR Code (T16, T17) | Feature | E | 6 | Thayná | Emissão em lote ⚠️ · Motor de PDF/A |
| Relatórios oficiais do evento (T06) | Feature | D | 11 | Pedro | Gestão de inscritos · Emissão em lote ⚠️ · Motor de PDF/A |
| Emissão de certificados em lote: fila, Storage e progresso | Feature | E | 8 | José | Apuração · Motor de PDF/A · Ambiente |

### S6 — Fechamento

| Card | Tipo | Pri | Pts | Responsável | Depende de |
|---|---|---|---|---|---|
| Teste E2E do fluxo completo + cobertura mínima de 70% | Qualidade | I | 5 | Anderson | MVP completo · Testes de integração |
| Acessibilidade (WCAG AA) e teste de usabilidade | Qualidade | I | 5 | Thayná | Telas principais |
| Manual do usuário e roteiro de apresentação | Doc | I | 3 | Pedro | MVP completo |
| Reemissão e cancelamento de certificado | Feature | E | 8 | José | Emissão em lote · Motor de PDF/A |

---

## ⚠️ Capacidade

Já estão prontos ~37 pts (estrutura inicial), restando **~279 pts**. Com 4 pessoas em 7 sprints, isso dá **~10 pts por pessoa por sprint** (≈ 5 dias de trabalho a cada 2 semanas) — o plano ocupa as sprints inteiras, sem folga.

Sprints mais pesadas: **Anderson na S2** (23), **Thayná na S3 e S4** (22 e 23), **José na S4** (15). Quem estiver leve na mesma sprint (ex.: Anderson na S3/S4) deve ajudar com revisão de PR e testes desses cards.

Se o ritmo real ficar abaixo disso, cortar nesta ordem:

1. **Relatórios (T06)** — RF-012 está "em negociação" e é Desejável no PDF
2. Itens "(Desejável)" dentro dos checklists (emissão automática, situação financeira)
3. Dashboard simplificado (só atalhos, sem indicadores)
4. Teste de carga reduzido (100 usuários em vez de 500)
