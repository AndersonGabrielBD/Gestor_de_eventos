# 06 — Frontend: rotas e telas

> Fonte: seção 8 do documento. Rotas declaradas em `frontend/src/routes.tsx`.

## Áreas
| Área | Prefixo | Perfis |
|---|---|---|
| Pública | `/`, `/login`, `/eventos`, `/validar` | todos, inclusive sem login |
| Participante | `/minhas-inscricoes`, `/meus-certificados`, `/perfil` | participante+ |
| Coordenador | `/coordenacao/...` | coordenador, administrador |
| Administrador | `/admin/...` | administrador |

## Mapa de telas
| Tela | Rota | Perfil | UC |
|---|---|---|---|
| T01 Login / Recuperação | `/login`, `/recuperar-senha`, `/cadastro` | Público | UC00 |
| T02 Dashboard | `/painel` | Todos (varia por perfil) | — |
| T03 Instituições e Unidades | `/admin/instituicoes` | Admin | UC02 |
| T04 Tipos de Certificado | `/admin/tipos-certificado` | Admin | UC09 |
| T05 Auditoria | `/admin/auditoria` | Admin | UC11 |
| T06 Relatórios | `/relatorios` | Admin, Coord. | UC12 |
| T07 Meus Eventos / Novo Evento | `/coordenacao/eventos`, `/coordenacao/eventos/novo`, `/coordenacao/eventos/:id` | Coord. | UC01 |
| T08 Coordenadores do Evento | `/coordenacao/eventos/:id/coordenadores` | Coord. | UC03 |
| T09 Programação / Atividades | `/coordenacao/eventos/:id/atividades` | Coord. | UC04 |
| T10 Inscritos do Evento | `/coordenacao/eventos/:id/inscritos` | Coord. | UC07, UC13, UC14 |
| T11 Check-in / Presença | `/coordenacao/eventos/:id/presenca` | Coord. | UC08 |
| T12 Emissão de Certificados | `/coordenacao/eventos/:id/certificados` | Coord. | UC10, UC15 |
| T13 Catálogo de Eventos | `/eventos`, `/eventos/:id` | Público | — |
| T14 Formulário de Inscrição | `/eventos/:id/inscricao` | Participante | UC05, UC06 |
| T15 Minhas Inscrições | `/minhas-inscricoes` | Participante | UC14 |
| T16 Meus Certificados | `/meus-certificados` | Participante | UC10 |
| T17 Validação Pública | `/validar`, `/validar/:codigo` | Público | UC10 |

## Fluxos principais
1. **Inscrição** — T13 → detalhe → T14 (1. dados/categoria → 2. atividades → 3. confirmação) → T15.
2. **Gestão do evento** — T07 (dados gerais) → T08 (coordenadores) → T09 (atividades) → Publicar.
3. **Check-in e certificado** — T10 → T11 → Encerrar evento → T12 → T16 do participante.
4. **Validação** — QR Code/PDF → T17.

## Diretrizes de UI
- **Acessibilidade (RNF-012):** contraste AA, foco visível, navegação 100% por teclado, `label` em todo campo, mensagens de erro associadas via `aria-describedby`, anúncios de sucesso/erro com `aria-live` (essencial no modo leitor do T11).
- **Responsividade (RNF-013):** mobile-first; o check-in (T11) será muito usado em celular/tablet.
- **Usabilidade (RNF-011):** inscrição em no máximo 3 etapas; mostrar vagas restantes e lista de espera.
- **Leitura de QR Code (T11):** biblioteca de câmera no navegador (ex.: `@zxing/browser` ou `html5-qrcode`) + suporte a leitor USB (que "digita" o código em um input com foco contínuo).
