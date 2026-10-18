# 07 — Lacunas do documento e perguntas para a equipe

Pontos encontrados na leitura do PDF que precisam de decisão antes (ou durante) a implementação. Cada item tem uma **sugestão** para não travar o desenvolvimento.

> ⚠️ **Pendente de aprovação do professor: escopo do MVP para 14/11/2026.** Com 4 semanas até a entrega, o plano cobre só o fluxo principal (criar evento → inscrever → check-in → emitir → validar). A lista do que ficou de fora está em [BACKLOG.md](BACKLOG.md) (seção "Fora do MVP"). Responsável por levar a pergunta: José (card "Validar regras de negócio", até qua 21/10).

| # | Lacuna | Impacto | Sugestão adotada até decisão |
|---|---|---|---|
| 1 | As **Regras de Negócio (RN x.y)** são citadas, mas não definidas no PDF. | Alto — validações dependem delas | Reconstruídas em `04-regras-de-negocio.md`; validar as marcadas 🟡. |
| 2 | **Pagamento/estorno** aparece em UC07 A1, UC10 E3, UC14 e T12/T15, mas não existe RF de pagamento. | Médio | Fora do MVP: evento tem flag `pago` e o coordenador marca a `situacao_financeira` manualmente. Sem gateway. |
| 3 | `POST /auth/login` sugerido no doc × Supabase Auth na stack. | Baixo | Login pelo Supabase no frontend; backend só valida JWT (ADR-02). |
| 4 | **SSO institucional** "se disponível" (RNF-006). | Baixo | Começar com e-mail/senha; Supabase suporta SAML/OAuth depois. |
| 5 | Status do evento: o doc lista planejado/em andamento/em apuração/encerrado **e** ações "Salvar rascunho"/"Publicar". | Baixo | `status` + flag `publicado` separada. |
| 6 | Frequência mínima para certificado não tem valor definido. | Médio | 75% padrão, configurável por evento. |
| 7 | "Totem/leitor automatizado" de check-in (UC08). | Baixo | Tela T11 em modo leitor (input com foco contínuo); totem físico fora do escopo. |
| 8 | "Participação por submissão de avaliação" (UC08 A1). | Baixo | Registrar como presença com `origem = avaliacao` lançada pelo coordenador; formulário de avaliação fora do MVP. |
| 9 | Emissão automática "pelo Sistema" (UC10 A2) — quando dispara? | Médio | Ao mudar o evento para `em_apuracao`, se o evento tiver `emissao_automatica = true`. Senão, botão manual. |
| 10 | Cancelamento de inscrição com certificado já emitido "salvo exceção configurada" (RN 3.4). | Baixo | Não revogar; coordenador pode cancelar o certificado manualmente (auditado). |
| 11 | Mobile citado em 7.1 ("Web/Mobile"). | Baixo | Apenas web responsiva (RNF-013). |
| 12 | RNF-004/005 (99% e backup com RTO 4h) dependem do plano do Supabase. | Médio | Documentar procedimento; plano gratuito tem limitações de backup — usar `pg_dump` agendado como alternativa. |
| 13 | Retenção de logs de 5 anos × direito de exclusão da LGPD. | Médio | Logs guardam apenas `pessoa_id`; exclusão LGPD = **anonimização** da pessoa (dados pessoais apagados, id preservado). |
| 14 | Quem promove um usuário a coordenador? | Médio | Administrador, via tela de pessoas (item extra no backlog). |
