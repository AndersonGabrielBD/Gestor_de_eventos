-- =============================================================================
-- Correções apontadas pelo Security Advisor do Supabase
-- =============================================================================

-- 1) Funções auxiliares do RLS saem do schema `public`, que é exposto pela API REST
--    (/rest/v1/rpc/...). As policies continuam funcionando: elas guardam a referência
--    à função, não o nome. anon/authenticated precisam de EXECUTE porque as policies
--    rodam com o papel de quem consulta.
create schema if not exists privado;
revoke all on schema privado from public;
grant usage on schema privado to anon, authenticated;

alter function public.pessoa_atual_id() set schema privado;
alter function public.eh_admin() set schema privado;
alter function public.eh_coordenador_do_evento(uuid) set schema privado;

-- O corpo desta função citava as outras duas por `public.`; recria apontando para `privado`.
create or replace function privado.eh_coordenador_do_evento(p_evento_id uuid) returns boolean
language sql stable security definer set search_path = '' as $$
    select privado.eh_admin() or exists (
        select 1 from public.coordenador_evento
        where evento_id = p_evento_id and pessoa_id = privado.pessoa_atual_id()
    )
$$;
alter function privado.pessoa_atual_id() set search_path = '';
alter function privado.eh_admin() set search_path = '';

revoke execute on all functions in schema privado from public;
grant execute on all functions in schema privado to anon, authenticated;

-- 2) search_path fixo nas funções de trigger (todas já usam nomes qualificados).
alter function public.tocar_atualizado_em() set search_path = '';
alter function public.impedir_remover_ultimo_coordenador() set search_path = '';
alter function public.bloquear_alteracao_auditoria() set search_path = '';

-- 3) Tabelas com RLS e sem policy (atividade_responsavel, inscricao_atividade,
--    registro_presenca, tipo_certificado_exclusividade) ficam assim de propósito:
--    só a API lê e escreve nelas (ADR-03).
