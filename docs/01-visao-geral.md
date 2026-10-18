# 01 — Visão Geral do Sistema

> Fonte: `Documento_Requisitos_Gestao_Eventos.pdf` (seções 2, 3, 5 e 8). Este arquivo é um resumo de trabalho para a equipe; o PDF continua sendo o documento oficial.

## Objetivo

Centralizar **planejamento, execução e certificação** de eventos acadêmicos (congressos, seminários, semanas científicas, oficinas, minicursos…) promovidos por instituições de ensino e suas unidades organizadoras.

Ciclo de vida resumido de um evento:

```
Cadastro institucional ─► Evento criado ─► Atividades + coordenadores ─► Publicação
      (Admin)              (Coordenador)        (Coordenador)              │
                                                                          ▼
Validação pública ◄─ Certificados ◄─ Apuração final ◄─ Presença ◄─ Inscrições
   (Público)          (Sistema)       (Coordenador)    (Coord.)   (Participante)
```

## Atores e perfis

| Ator | Perfil no sistema | O que faz |
|---|---|---|
| **Administrador** | `administrador` | Cadastro institucional, tipos de certificado, auditoria, relatórios. **Herda tudo do Coordenador.** |
| **Coordenador do Evento** | `coordenador` | Eventos, atividades, coordenadores, inscrições, presença, emissão/reemissão de certificados. |
| **Participante** | `participante` | Cadastro, inscrição, acompanhamento de status, download de certificados, cancelamento da própria inscrição. |
| **Público (sem login)** | — | Validação pública de certificado (T17) e catálogo de eventos. |
| **Sistema** | (worker/middleware) | Emissão automática de certificados e registro automático de auditoria. |

> Atenção: "coordenador" é ao mesmo tempo um **perfil global** (pode criar eventos) e um **vínculo por evento** (`coordenador_evento`). Um coordenador só gerencia os eventos aos quais está vinculado; o administrador gerencia todos.

## Requisitos funcionais

| RF | Requisito | Prioridade | Status | Casos de uso | Telas | Módulo backend |
|---|---|---|---|---|---|---|
| RF-001 | Evento | Essencial | Validado | UC01 | T07 | `eventos` |
| RF-002 | Instituição / Unidade | Essencial | Validado | UC02 | T03 | `instituicoes` |
| RF-003 | Coordenador do Evento | Essencial | Validado | UC03 | T08 | `coordenadores` |
| RF-004 | Atividade | Essencial | Validado | UC04 | T09 | `atividades` |
| RF-005 | Pessoa (Participante) | Essencial | Validado | UC05 | T14 | `pessoas` |
| RF-006 | Inscrição | Essencial | Validado | UC06 | T13, T14, T15 | `inscricoes` |
| RF-007 | Status da Inscrição | Essencial | Validado | UC07, UC13, UC14 | T10, T15 | `inscricoes` |
| RF-008 | Presença / Participação | Essencial | Validado | UC08 | T11 | `presencas` |
| RF-009 | Tipo de Certificado | Importante | Validado | UC09 | T04 | `certificados` |
| RF-010 | Certificado | Essencial | Validado | UC10, UC15 | T12, T16, T17 | `certificados` + `worker` |
| RF-011 | Auditoria | Importante | Validado | UC11 | T05 | `auditoria` |
| RF-012 | Relatórios | Desejável | Em negociação | UC12 | T06 | `relatorios` |

## Requisitos não funcionais (resumo acionável)

| RNF | Tema | Meta verificável | Como atendemos |
|---|---|---|---|
| RNF-001 | Tempo de resposta | Consulta ≤ 2 s; escrita ≤ 4 s | Índices, paginação, PDF fora da requisição (fila) |
| RNF-002 | Concorrência | 500 usuários simultâneos se inscrevendo | Controle de vagas com lock/transação; teste de carga (k6/Locust) |
| RNF-003 | Escalabilidade | Escala sem redesenho | API stateless, worker separado, Supabase gerenciado |
| RNF-004 | Disponibilidade | ≥ 99%/mês | Hospedagem gerenciada + health check |
| RNF-005 | Backup | Diário; RTO 4 h; RPO 24 h | Backups do Supabase + procedimento de restauração documentado |
| RNF-006 | AuthN/AuthZ | Perfis admin/coord/participante | Supabase Auth (JWT) + dependências FastAPI + RLS |
| RNF-007 | Proteção de dados | Dados sensíveis cifrados; só HTTPS | CPF cifrado na aplicação + hash para busca; TLS |
| RNF-008 | LGPD | Consentimento, finalidade, exclusão/anonimização | Consentimento no cadastro, rotina de anonimização |
| RNF-009 | Auditabilidade | Log imutável, retenção ≥ 5 anos | Tabela append-only com trigger que bloqueia UPDATE/DELETE |
| RNF-010 | Certificados | Código único/QR; PDF/A | WeasyPrint + pikepdf + qrcode; rota pública de validação |
| RNF-011 | Usabilidade | Inscrição em ≤ 3 passos; erro < 5% | Formulário em 3 etapas (T14) |
| RNF-012 | Acessibilidade | WCAG 2.1 AA | Componentes acessíveis, axe/Lighthouse no CI |
| RNF-013 | Compatibilidade | Chrome/Firefox/Edge/Safari (2 últimas); responsivo | SPA responsiva, browserslist |
| RNF-014 | Manutenibilidade | Camadas; cobertura ≥ 70% | Monólito modular; pytest-cov / vitest coverage no CI |

## Mapa de casos de uso

| UC | Nome | Ator(es) | Relações |
|---|---|---|---|
| UC00 | Autenticar-se | Todos | pré-requisito transversal |
| UC01 | Gerenciar Evento | Coordenador, Admin | |
| UC02 | Gerenciar Instituição/Unidade | Admin | |
| UC03 | Gerenciar Coordenador do Evento | Coordenador, Admin | |
| UC04 | Gerenciar Atividade | Coordenador, Admin | |
| UC05 | Cadastrar Pessoa | Participante | incluído por UC06 |
| UC06 | Realizar Inscrição | Participante | inclui UC05, UC07 |
| UC07 | Gerenciar Status da Inscrição | Coordenador | estendido por UC13, UC14 |
| UC08 | Registrar Presença | Coordenador | incluído por UC10 |
| UC09 | Gerenciar Tipo de Certificado | Admin | incluído por UC10 |
| UC10 | Emitir/Gerenciar Certificado | Coordenador, Participante, Sistema | inclui UC08, UC09; estendido por UC15 |
| UC11 | Consultar Auditoria | Admin, Sistema | |
| UC12 | Gerar Relatórios | Admin, Coordenador | |
| UC13 | Indeferir Inscrição | Coordenador | estende UC07 |
| UC14 | Cancelar Inscrição | Participante, Coordenador | estende UC07 |
| UC15 | Reemitir Certificado | Coordenador | estende UC10 |

## Glossário

- **Unidade organizadora** — campus, centro ou curso pertencente a uma instituição.
- **Atividade** — item da programação (palestra, oficina, minicurso, mesa-redonda…), com carga horária própria.
- **Atividades paralelas** — atividades que se sobrepõem no tempo; a carga horária não pode ser somada em duplicidade.
- **Apuração final** — estado do evento em que a presença é consolidada e os certificados podem ser emitidos.
- **Carga horária certificável** — soma das cargas horárias em que a pessoa atingiu a frequência mínima, sem duplicar paralelas.
- **Ação de impacto** — indeferimento, validação/ajuste manual de presença, emissão, cancelamento, reemissão. Sempre auditada.
