# 05 — Contrato da API (planejado)

> Prefixo: `/api/v1`. A documentação viva fica em `http://localhost:8000/docs` (OpenAPI gerado pelo FastAPI).
> Legenda de acesso: **P** = público, **A** = autenticado, **Pa** = participante (dono do recurso), **C** = coordenador vinculado ao evento, **Ad** = administrador.
> ✅ = implementado na estrutura inicial.

## Auth / Pessoa
| Método | Rota | Acesso | UC |
|---|---|---|---|
| GET | `/auth/me` ✅ | A | UC00 |
| POST | `/pessoas` (completar cadastro + consentimento LGPD) | A | UC05 |
| GET/PUT | `/pessoas/me` | A | UC05 |
| GET | `/pessoas?busca=` (para vincular coordenador/palestrante) | C, Ad | UC03 |
| POST | `/pessoas/externas` (palestrante sem login) | C, Ad | UC04 |
| PUT | `/pessoas/{id}/perfil` | Ad | — |
| POST | `/pessoas/me/solicitacoes-lgpd` | A | RNF-008 |

> Login, logout e recuperação de senha são feitos pelo Supabase Auth no frontend (ver ADR-02).

## Instituições (UC02)
| Método | Rota | Acesso |
|---|---|---|
| GET | `/instituicoes` ✅ | A |
| POST | `/instituicoes` ✅ | Ad |
| GET | `/instituicoes/{id}` ✅ | A |
| PUT | `/instituicoes/{id}` ✅ | Ad |
| POST | `/instituicoes/{id}/inativar` ✅ | Ad |
| GET | `/instituicoes/{id}/unidades` ✅ | A |
| POST | `/instituicoes/{id}/unidades` ✅ | Ad |
| PUT | `/instituicoes/{id}/unidades/{unidade_id}` ✅ | Ad |
| POST | `/instituicoes/{id}/unidades/{unidade_id}/inativar` ✅ | Ad |

## Eventos (UC01) e Coordenadores (UC03)
| Método | Rota | Acesso |
|---|---|---|
| GET | `/eventos` (catálogo: publicados; filtros) | P |
| GET | `/eventos/meus` | C |
| GET | `/eventos/{id}` | P (se publicado) / C |
| POST | `/eventos` (cria e já vincula o criador como coordenador) | C, Ad |
| PUT | `/eventos/{id}` | C |
| POST | `/eventos/{id}/publicar` | C |
| POST | `/eventos/{id}/iniciar` | C |
| POST | `/eventos/{id}/encerrar` (→ em_apuracao) | C |
| GET | `/eventos/{id}/coordenadores` | C |
| POST | `/eventos/{id}/coordenadores` | C |
| DELETE | `/eventos/{id}/coordenadores/{pessoa_id}` | C |

## Atividades (UC04)
| Método | Rota | Acesso |
|---|---|---|
| GET | `/eventos/{id}/atividades` | P |
| POST | `/eventos/{id}/atividades` | C |
| PUT | `/atividades/{id}` | C |
| DELETE | `/atividades/{id}` (se sem inscrições/presenças) | C |
| PUT | `/atividades/{id}/responsaveis` | C |

## Inscrições (UC06, UC07, UC13, UC14)
| Método | Rota | Acesso |
|---|---|---|
| POST | `/eventos/{id}/inscricoes` | A |
| GET | `/inscricoes/minhas` | A |
| POST | `/inscricoes/{id}/cancelar` | Pa / C (com justificativa) |
| GET | `/eventos/{id}/inscricoes?status=&categoria=&atividade=` | C |
| POST | `/inscricoes/{id}/status` (`{status, justificativa}`) | C |
| POST | `/inscricoes/{id}/indeferir` (`{justificativa}`) | C |
| POST | `/inscricoes/{id}/situacao-financeira` | C |

## Presença (UC08)
| Método | Rota | Acesso |
|---|---|---|
| POST | `/eventos/{id}/presencas/check-in` (`{codigo | inscricao_id, atividade_id?}`) | C |
| POST | `/eventos/{id}/presencas/check-out` | C |
| POST | `/eventos/{id}/presencas/ajuste-manual` (`{…, justificativa}`) | C |
| GET | `/eventos/{id}/presencas?pessoa=&atividade=` | C |
| GET | `/eventos/{id}/presencas/consolidado` | C |
| DELETE | `/presencas/{id}` (com justificativa) | C |

## Certificados (UC09, UC10, UC15)
| Método | Rota | Acesso |
|---|---|---|
| GET/POST | `/tipos-certificado` | A / Ad |
| PUT | `/tipos-certificado/{id}` | Ad |
| POST | `/tipos-certificado/{id}/inativar` | Ad |
| PUT | `/tipos-certificado/{id}/exclusividades` | Ad |
| GET | `/eventos/{id}/certificados/elegiveis` | C |
| POST | `/eventos/{id}/certificados/lote` → `202 {job_id}` | C |
| POST | `/eventos/{id}/certificados/individual` | C |
| GET | `/jobs-certificado/{job_id}` | C |
| POST | `/certificados/{id}/reemitir` (`{dados_corrigidos, motivo}`) | C |
| POST | `/certificados/{id}/cancelar` (`{motivo}`) | C |
| GET | `/certificados/meus` | A |
| GET | `/certificados/{id}/download` (URL assinada do Storage) | Pa / C |
| GET | `/validar/{codigo}` | **P** |

## Auditoria (UC11) e Relatórios (UC12)
| Método | Rota | Acesso |
|---|---|---|
| GET | `/auditoria?evento=&acao=&responsavel=&de=&ate=` | Ad |
| GET | `/auditoria/exportar?…&formato=csv` | Ad |
| GET | `/relatorios/eventos/{id}/certificados-emitidos?formato=json|csv|pdf` | C, Ad |
| GET | `/relatorios/eventos/{id}/carga-horaria?formato=` | C, Ad |
| GET | `/relatorios/eventos/{id}/indeferimentos?formato=` | C, Ad |
| GET | `/dashboard` (indicadores por perfil — T02) | A |

## Convenções
- Erros de regra de negócio: `422` com corpo `{"codigo": "RN-1.1", "mensagem": "..."}`.
- Recurso não encontrado: `404`; sem permissão: `403`; sem token/expirado: `401`.
- Paginação: `?pagina=1&tamanho=20` → `{"itens": [...], "total": n}`.
- Datas em ISO-8601 com fuso (`timestamptz`).
