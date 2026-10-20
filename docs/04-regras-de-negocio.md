# 04 — Regras de Negócio (RN)

> ⚠️ **Lacuna no documento de requisitos:** os casos de uso citam regras "RN 1.1 … RN 10.3", mas o PDF **não contém a seção que as define**. A tabela abaixo foi **reconstruída a partir do contexto de cada caso de uso**. Regras marcadas com 🔵 foram inferidas pela equipe; as marcadas com 🟢 estão descritas explicitamente em algum fluxo do PDF.

> ✅ **Validadas com o professor em 20/10/2026** (card "Validar regras de negócio"): todas as regras desta tabela foram aceitas como estão, inclusive as inferidas (🔵). Frequência mínima confirmada em **75%**, configurável por evento (RN 4.2). Respostas completas em [07-lacunas-e-perguntas.md](07-lacunas-e-perguntas.md#respostas-do-professor-20102026).

| RN | Regra | Origem | Onde é aplicada |
|---|---|---|---|
| 1.1 | 🟢 Instituição/unidade vinculada a evento ativo (≠ encerrado) não pode ser inativada nem excluída. | UC02 E1, T03 | `InstituicaoService.inativar` |
| 1.2 | 🟢 Todo evento deve ter **ao menos um** coordenador; o último não pode ser removido. | UC01 E1, UC03 E1 | `CoordenadorService` + trigger |
| 1.3 | 🔵 Atividades devem estar contidas no período do evento. | UC01/UC04 | `AtividadeService` |
| 1.4 | 🟢 Carga horária de atividade deve ser > 0. | UC04 E1 | schema + CHECK |
| 1.5 | 🔵 Evento segue o ciclo planejado → em andamento → em apuração → encerrado; não volta de estado. | UC01 pós-condição | `EventoService` |
| 2.1 | 🔵 Só pessoa cadastrada (UC05) pode se inscrever; o cadastro é criado no fluxo se não existir. | UC06 passo 2 | `InscricaoService` |
| 2.2 | 🟢 A categoria da pessoa deve atender os critérios de participação do evento. | UC06 E2 | `InscricaoService` |
| 2.3 | 🟢 Uma pessoa só pode ter **uma inscrição ativa** por evento. | UC06 E3 | índice único parcial |
| 2.4 | 🟢 Evento lotado: com lista de espera → `em_espera`; sem lista → rejeita. | UC06 A2/E4 | `InscricaoService` (com lock) |
| 2.5 | 🔵 Atividades com capacidade própria seguem a mesma regra de vagas; não é permitido escolher duas atividades paralelas. | UC06 A1, UC04 | `InscricaoService` |
| 3.1 | 🔵 Transições de status seguem a máquina de estados; `cancelada` e `indeferida` são finais. | UC07 E1, UC13 | `StatusInscricaoService` |
| 3.2 | 🟢 Participante cancela sozinho apenas até `cancelamento_ate`; depois disso vira pedido pendente de decisão da organização. | UC14 E1, T15 | `InscricaoService.cancelar` |
| 3.3 | 🔵 Cancelamento de inscrição confirmada libera a vaga e promove o primeiro da lista de espera. | UC14 | `InscricaoService.cancelar` |
| 3.4 | 🟢 Inscrição cancelada não gera certificado; cancelar não revoga certificado já emitido (salvo configuração). | UC10 E2, UC14 E2 | `CertificadoService` |
| 4.1 | 🟢 Presença só pode ser registrada para inscrição **confirmada**. | UC08 pré-condição | `PresencaService` |
| 4.2 | 🟢 Certificado exige frequência mínima (padrão 75%, configurável por evento). | UC10 E1 | `CertificadoService` |
| 4.3 | 🟢 Percentual de presença é calculado sobre a carga horária certificável. | UC08 passo 4 | `PresencaService.consolidar` |
| 4.4 | 🟢 A elegibilidade é avaliada por certificado (por atividade e/ou geral do evento). | UC10 E1 | `CertificadoService` |
| 4.5 | 🟢 Registro fora do período oficial sem justificativa é descartado. | UC08 E1 | `PresencaService` |
| 5.1 | 🟢 O tipo de certificado depende do papel da pessoa no evento (participante, palestrante…). | UC09, UC10 passo 5 | `CertificadoService` |
| 5.2 | 🟢 Tipo já usado em certificado não pode ser excluído, apenas inativado. | UC09 E1 | `TipoCertificadoService` + FK RESTRICT |
| 5.3 | 🔵 Pares de tipos marcados como exclusivos não podem ser emitidos para a mesma pessoa no mesmo evento. | UC09 passo 3 | `CertificadoService` |
| 5.4 | 🟢 Carga horária de atividades paralelas não é somada em duplicidade. | UC04 A2, UC10 passo 3 | `CertificadoService` |
| 5.5 | 🔵 Certificados de palestrante/ministrante/mediador derivam de `atividade_responsavel`, não exigem inscrição/presença. | UC10 | `CertificadoService` |
| 6.1 | 🟢 Todo certificado tem identificador único e mecanismo de validação pública. | UC10, RNF-010 | `certificado.codigo` |
| 6.2 | 🟢 Certificado é gerado em PDF/A com QR Code. | RNF-010 | worker |
| 6.3 | 🟢 Reemissão gera nova versão ligada ao identificador original e preserva a anterior. | UC15 | `CertificadoService.reemitir` |
| 6.4 | 🟢 Certificado cancelado não é reemitido e continua validável como "cancelado". | UC15 E2 | `CertificadoService.reemitir` |
| 6.5 | 🟢 Emissão (inclusive em lote) só com evento em apuração/encerrado. | UC10 pré-condição, A1 | `CertificadoService` |
| 7.1 | 🟢 Evento pago com pendência financeira bloqueia a emissão. | UC10 E3 | `CertificadoService` |
| 7.3 | 🔵 Cancelamento em evento pago aciona estorno conforme política do evento. | UC07 A1, UC14 passo 4 | fora do MVP (sem gateway; registro manual da situação financeira) |
| 8.3 | 🟢 Não pode haver pessoa duplicada (e-mail institucional, matrícula ou CPF). | UC05 passo 3 | `PessoaService` + índices únicos |
| 9.1 | 🟢 Inscrição só dentro da janela de inscrição do evento. | UC06 E1 | `InscricaoService` |
| 9.3 | 🟢 Correção/reemissão só dentro do prazo do evento (ex.: 30 dias); fora, exige aprovação especial. | UC15 E1 | `CertificadoService.reemitir` |
| 10.1 | 🟢 Toda ação de impacto é vinculada a um responsável autenticado e, quando administrativa, a uma justificativa obrigatória. | UC00, UC13 E1 | `AuditoriaService` |
| 10.2 | 🟢 Ajustes manuais de presença são auditados. | UC08 A2 | `PresencaService` |
| 10.3 | 🟢 Relatórios são reproduzíveis e sinalizam "dados parciais" se o evento não estiver apurado. | UC12 E1 | `RelatorioService` |

Regras não citadas no PDF (RN 7.2, 8.1, 8.2, 9.2…) provavelmente existem no material original — vale perguntar ao professor/equipe.
