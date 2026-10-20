# Backlog — Sistema de Gestão de Eventos Institucionais

> Espelho do quadro do Trello **[Gestão de eventos APP](https://trello.com/b/FplztFY4/gest%C3%A3o-de-eventos-app)**.
> Cada card é uma **funcionalidade completa** (backend + tela + testes). As tarefas técnicas ficam no checklist **"Tarefas"** dentro do card no Trello; aqui fica a visão geral.
> Fonte de verdade do andamento: **o Trello**. Quem depende de quem: [08-dependencias.md](08-dependencias.md).

## 🎯 Entrega: sábado, 14/11/2026

O prazo é curto (4 semanas), então o plano é um **MVP do fluxo principal**:

> **criar evento → inscrever → confirmar → check-in → apurar → emitir certificado → validar publicamente**

Tudo que não é essencial para esse fluxo foi para a lista **"✂️ Fora do MVP (depois de 14/11)"** no Trello (ver a seção "Fora do MVP" abaixo). ✅ O escopo reduzido **foi aprovado pelo professor em 20/10/2026**, junto com as regras de negócio (ver [07-lacunas-e-perguntas.md](07-lacunas-e-perguntas.md#respostas-do-professor-20102026)). Nenhum card cortado voltou para o MVP.

## Como ler

- **Tipo:** `[Feature]` funcionalidade · `[Infra]` ambiente/deploy · `[Doc]` documentação
- **Prioridade** (herdada do PDF): **E** = Essencial · **I** = Importante
- **Pts** — estimativa relativa **já com o escopo cortado** (1 pt ≈ meio dia de uma pessoa)
- ⚠️ — depende de outro card **da mesma sprint**, com prazo combinado (ver [08-dependencias.md](08-dependencias.md))
- Itens de checklist marcados **(pós-MVP)** no Trello **não** precisam ser feitos para 14/11
- **Branch:** `feat/<nome-curto-do-card>` (ex.: `feat/criar-evento`). Cite o nome do card no PR.

### Definição de Pronto (DoD) — versão MVP
1. Critérios de aceite do card concluídos (itens "(pós-MVP)" ficam de fora).
2. PR revisado por pelo menos 1 colega e CI verde (lint + testes + build).
3. Testes automatizados das **regras de negócio** do card (não precisa testar tela).
4. Ações de impacto gravam `log_auditoria` com responsável e justificativa.
5. Tela usa os componentes base (labels nos campos, funciona no celular).

---

## Calendário

| Sprint | Datas | Objetivo |
|---|---|---|
| **S1** | 19–25/10 | Ambiente, login, componentes, cadastros base, deploy e motor de PDF |
| **S2** | 26/10–01/11 | Coordenador monta o evento; catálogo público; base da emissão |
| **S3** | 02–08/11 | Inscrição, gestão de inscritos, check-in e apuração |
| **S4** | 09–14/11 | Certificados na mão do participante, integração, demo e ensaio |

**Marcos da S4:**
- Seg 09 – Ter 10/11: integração ponta a ponta e correção de bugs (todos)
- **Qua 11/11: 🧊 code freeze** — depois disso só correção de bug
- Qui 12 – Sex 13/11: ensaio da apresentação e ajustes finais
- **Sáb 14/11: 🎯 entrega**

---

## Quem faz o quê em cada sprint (pts)

4 pessoas fullstack, por fatia vertical (cada um faz backend + tela do próprio card). **Todo mundo trabalha em todas as sprints.**

| Sprint | Anderson | Thayná | Pedro | José |
|---|---|---|---|---|
| **S1** | Fundação + Ambiente + Login (11) | Componentes + Instituições (7) | Pessoa (6) | Validar RNs + Deploy + Motor PDF/A (10) |
| **S2** | Criar evento (12) | Catálogo (5) | Atividades (8) | Auditoria + Emissão (base) (8) |
| **S3** | Check-in (7) | Inscrição (10) | Gestão de inscritos + Minhas inscrições (9) | Apuração (7) |
| **S4** | Demo + estabilização (4) | Meus certificados + Validação (5) | Manual + roteiro (3) | Emissão (integração) (3) |
| **Total** | **~34** | **~27** | **~26** | **~28** |

> No Trello, o responsável aparece no fim do título do card (`· 👤 Nome`). Cada um deve clicar em **"Participar"** nos seus cards para aparecer o avatar.

---

## Cards

### S1 — 19 a 25/10

| Card | Tipo | Pri | Pts | Responsável | Depende de |
|---|---|---|---|---|---|
| Fundação do projeto (estrutura, CI, schema do banco) — **Em review** | Infra | E | ~1 | Anderson | — |
| Ambiente da equipe: Supabase compartilhado, local e worker em Docker | Infra | E | 5 | Anderson | Fundação |
| Login, cadastro de conta e recuperação de senha (T01) | Feature | E | 5 | Anderson | Fundação |
| Biblioteca de componentes acessível + ESLint/Prettier | Infra | I | 3 | Thayná | Fundação |
| Tela de Instituições e Unidades (T03) — backend pronto ✅ | Feature | E | 4 | Thayná | Login ⚠️ · Componentes ⚠️ |
| Cadastro de pessoa e "Meu perfil" com consentimento LGPD | Feature | E | 6 | Pedro | Login ⚠️ |
| Validar regras de negócio, lacunas **e escopo do MVP** com o professor — **Concluído (20/10)** ✅ | Doc | E | 1 | José | — |
| Deploy de homologação (API, frontend e worker) + CORS/headers | Infra | I | 4 | José | Ambiente ⚠️ |
| Motor de PDF/A do certificado (template + QR Code + worker) | Feature | E | 5 | José | Ambiente ⚠️ |

### S2 — 26/10 a 01/11

| Card | Tipo | Pri | Pts | Responsável | Depende de |
|---|---|---|---|---|---|
| Criar e gerenciar evento (T07) | Feature | E | 12 | Anderson | Login · Instituições ✅ · Pessoa |
| Catálogo de eventos e página de detalhe (T13) | Feature | E | 5 | Thayná | Criar evento ⚠️ · Atividades ⚠️ |
| Programação / Atividades do evento (T09) | Feature | E | 8 | Pedro | Criar evento ⚠️ · Pessoa |
| Auditoria: consulta dos logs (T05) — registro pronto ✅ | Feature | I | 3 | José | Login · Componentes |
| Emissão de certificados em lote — **base** (fila, worker, Storage com elegíveis falsos) | Feature | E | 5 | José | Motor PDF/A · Ambiente |

### S3 — 02 a 08/11

| Card | Tipo | Pri | Pts | Responsável | Depende de |
|---|---|---|---|---|---|
| Check-in e presença — modo lista (T11) | Feature | E | 7 | Anderson | Inscrição ⚠️ · Gestão de inscritos ⚠️ |
| Tela de inscrição do participante (T14) | Feature | E | 10 | Thayná | Pessoa · Criar evento · Catálogo |
| Gestão de inscritos: confirmar, indeferir e cancelar (T10) | Feature | E | 6 | Pedro | Inscrição ⚠️ |
| Minhas inscrições e cancelamento (T15) | Feature | E | 3 | Pedro | Inscrição ⚠️ |
| Apuração final: quem tem direito a certificado (T12) | Feature | E | 7 | José | Check-in ⚠️ · Atividades · Criar evento |

### S4 — 09 a 14/11

| Card | Tipo | Pri | Pts | Responsável | Depende de |
|---|---|---|---|---|---|
| Dados de demonstração + estabilização para a entrega | Infra | E | 4 | Anderson | Tudo das S1–S3 |
| Meus certificados e validação pública por QR Code (T16, T17) | Feature | E | 5 | Thayná | Emissão ⚠️ · Motor PDF/A |
| Manual do usuário e roteiro de apresentação | Doc | E | 3 | Pedro | Telas prontas no code freeze · Demo ⚠️ |
| Emissão em lote — **integração** com a apuração real | Feature | E | 3 | José | Apuração · Emissão (base) |

---

## ✂️ Fora do MVP (depois de 14/11)

Cards movidos para a lista **"✂️ Fora do MVP (depois de 14/11)"** no Trello. Ficam documentados para o caso de o professor pedir ou de sobrar tempo.

| Card | Por que saiu | Como fica no MVP |
|---|---|---|
| Coordenadores do evento (T08) | Não é necessário para o fluxo principal | Quem cria o evento é o coordenador; admin acessa tudo |
| Tela de Tipos de certificado (T04) | Tipos podem vir do seed | Tipos padrão (participante, palestrante, ministrante, mediador) no `seed.sql` |
| Admin define o perfil do usuário | Tela administrativa secundária | Promover coordenador/admin direto no banco |
| Privacidade LGPD: solicitações e anonimização | Fluxo grande e fora do caminho principal | Fica o aceite do termo no cadastro de pessoa + CPF cifrado |
| Segurança: rate limit e backup | Infra de produção | CORS e headers foram para o card de Deploy |
| Testes de integração contra Postgres real | Tempo | Testes unitários das regras de negócio em cada card |
| Teste de carga (500 usuários) | Tempo | Trava de concorrência da última vaga testada na Inscrição |
| Teste E2E + cobertura 70% | Tempo | Fluxo ponta a ponta rodado à mão na S4 (card de Demo) |
| Acessibilidade WCAG AA completa | Tempo | Biblioteca de componentes acessível + labels nos campos |
| Relatórios oficiais (T06) | RF-012 "em negociação", Desejável | — |
| Dashboard por perfil (T02) | Não é essencial | `/painel` com atalhos simples (se der tempo) |
| Reemissão e cancelamento de certificado | Depois da emissão | — |

Também ficaram **(pós-MVP)** dentro dos cards: modo leitor de QR no check-in, QR na tela do participante, inscrição em atividades específicas, detecção automática de atividades paralelas, situação financeira, exportação CSV da auditoria, emissão automática e pre-commit no backend.

---

## ⚠️ Capacidade

O MVP soma **~115 pts** em 4 semanas — cerca de **7–8 pts por pessoa por semana** (≈ 3,5–4 dias de trabalho por semana para cada um). É apertado e **não tem folga**: qualquer atraso numa entrega "para os outros" (ver prazos em [08-dependencias.md](08-dependencias.md)) empurra a sprint seguinte.

Pontos de atenção:
- **Anderson na S2** (12 pts — Criar evento) e **Thayná na S3** (10 pts — Inscrição) são os cards mais pesados e os que mais destravam gente. Quem estiver mais leve na semana ajuda com revisão de PR e testes.
- A **S3 tem uma corrente de dependências** dentro da mesma semana (Inscrição → Gestão → Check-in → Apuração). Os prazos de terça/quarta/quinta são obrigatórios.

Se mesmo assim atrasar, cortar nesta ordem:
1. Promoção automática da lista de espera (coordenador confirma à mão)
2. Busca por texto no catálogo
3. Auditoria só no banco (sem tela) — mostrar via Supabase na apresentação
4. Ajuste manual de presença (fazer check-in pela lista)
