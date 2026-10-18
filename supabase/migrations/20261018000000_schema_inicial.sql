-- =============================================================================
-- Sistema de Gestão de Eventos Institucionais — schema inicial
-- Referências: docs/03-modelo-de-dados.md e docs/04-regras-de-negocio.md
-- =============================================================================

create extension if not exists citext with schema extensions;

-- -----------------------------------------------------------------------------
-- Enums
-- -----------------------------------------------------------------------------
create type perfil_usuario       as enum ('participante', 'coordenador', 'administrador');
create type categoria_pessoa     as enum ('discente', 'docente', 'tecnico', 'externo', 'outro');
create type tipo_unidade         as enum ('campus', 'centro', 'curso', 'outro');
create type modalidade_evento    as enum ('presencial', 'hibrido', 'remoto');
create type status_evento        as enum ('planejado', 'em_andamento', 'em_apuracao', 'encerrado');
create type tipo_atividade       as enum ('palestra', 'oficina', 'minicurso', 'mesa_redonda', 'apresentacao_trabalho', 'outro');
create type papel_responsavel    as enum ('palestrante', 'ministrante', 'mediador', 'apresentador');
create type status_inscricao     as enum ('pre_inscrita', 'confirmada', 'em_espera', 'cancelada', 'indeferida');
create type situacao_financeira  as enum ('nao_aplicavel', 'pendente', 'pago', 'estornado');
create type origem_presenca      as enum ('manual', 'leitor', 'avaliacao');
create type status_certificado   as enum ('emitido', 'reemitido', 'substituido', 'cancelado');
create type tipo_job_certificado as enum ('lote', 'individual', 'reemissao');
create type status_job           as enum ('pendente', 'processando', 'concluido', 'erro');
create type acao_auditoria       as enum (
    'inscricao_status_alterado', 'inscricao_indeferida', 'inscricao_cancelada',
    'presenca_ajuste_manual', 'presenca_removida',
    'certificado_emitido', 'certificado_reemitido', 'certificado_cancelado',
    'evento_status_alterado', 'coordenador_vinculado', 'coordenador_removido',
    'perfil_alterado', 'pessoa_anonimizada'
);
create type tipo_solicitacao_lgpd   as enum ('acesso', 'correcao', 'exclusao', 'anonimizacao');
create type status_solicitacao_lgpd as enum ('aberta', 'atendida', 'recusada');

-- -----------------------------------------------------------------------------
-- Função utilitária para atualizado_em
-- -----------------------------------------------------------------------------
create or replace function public.tocar_atualizado_em() returns trigger
language plpgsql as $$
begin
    new.atualizado_em := now();
    return new;
end $$;

-- -----------------------------------------------------------------------------
-- Pessoa (RF-005) — ADR-05 / ADR-06
-- -----------------------------------------------------------------------------
create table public.pessoa (
    id                     uuid primary key default gen_random_uuid(),
    user_id                uuid unique references auth.users (id) on delete set null,
    perfil                 perfil_usuario   not null default 'participante',
    nome                   text             not null,
    email                  extensions.citext not null unique,
    cpf_cifrado            bytea,
    cpf_hash               text unique,
    matricula              text unique,
    categoria              categoria_pessoa not null default 'externo',
    vinculo_institucional  text,
    consentimento_lgpd_em  timestamptz,
    anonimizado_em         timestamptz,
    criado_em              timestamptz      not null default now(),
    atualizado_em          timestamptz      not null default now()
);
create trigger trg_pessoa_atualizado before update on public.pessoa
    for each row execute function public.tocar_atualizado_em();

-- -----------------------------------------------------------------------------
-- Instituição / Unidade (RF-002)
-- -----------------------------------------------------------------------------
create table public.instituicao (
    id            uuid primary key default gen_random_uuid(),
    nome          text        not null,
    sigla         text,
    dados         jsonb       not null default '{}'::jsonb,
    ativo         boolean     not null default true,
    criado_em     timestamptz not null default now(),
    atualizado_em timestamptz not null default now()
);
create unique index uq_instituicao_nome on public.instituicao (lower(nome));
create trigger trg_instituicao_atualizado before update on public.instituicao
    for each row execute function public.tocar_atualizado_em();

create table public.unidade_organizadora (
    id             uuid primary key default gen_random_uuid(),
    instituicao_id uuid         not null references public.instituicao (id) on delete restrict,
    nome           text         not null,
    tipo           tipo_unidade not null default 'curso',
    ativo          boolean      not null default true,
    criado_em      timestamptz  not null default now(),
    atualizado_em  timestamptz  not null default now(),
    unique (instituicao_id, nome)
);
create trigger trg_unidade_atualizado before update on public.unidade_organizadora
    for each row execute function public.tocar_atualizado_em();

-- -----------------------------------------------------------------------------
-- Evento (RF-001)
-- -----------------------------------------------------------------------------
create table public.evento (
    id                       uuid primary key default gen_random_uuid(),
    unidade_organizadora_id  uuid              not null references public.unidade_organizadora (id) on delete restrict,
    titulo                   text              not null,
    descricao                text,
    data_inicio              timestamptz       not null,
    data_fim                 timestamptz       not null,
    inscricao_inicio         timestamptz       not null,
    inscricao_fim            timestamptz       not null,
    cancelamento_ate         timestamptz,
    prazo_correcao_dias      int               not null default 30 check (prazo_correcao_dias >= 0),
    modalidade               modalidade_evento not null,
    local                    text,
    link                     text,
    publico_alvo             text,
    categorias_permitidas    categoria_pessoa[] not null default '{}',
    capacidade               int check (capacidade is null or capacidade > 0),
    lista_espera_habilitada  boolean           not null default false,
    frequencia_minima        numeric(5,2)      not null default 75 check (frequencia_minima between 0 and 100),
    pago                     boolean           not null default false,
    emissao_automatica       boolean           not null default false,
    publicado                boolean           not null default false,
    status                   status_evento     not null default 'planejado',
    criado_em                timestamptz       not null default now(),
    atualizado_em            timestamptz       not null default now(),
    check (data_fim >= data_inicio),
    check (inscricao_fim >= inscricao_inicio)
);
create index ix_evento_unidade on public.evento (unidade_organizadora_id);
create index ix_evento_catalogo on public.evento (publicado, data_inicio);
create trigger trg_evento_atualizado before update on public.evento
    for each row execute function public.tocar_atualizado_em();

-- -----------------------------------------------------------------------------
-- Coordenador do evento (RF-003) — RN 1.2
-- -----------------------------------------------------------------------------
create table public.coordenador_evento (
    evento_id  uuid        not null references public.evento (id) on delete cascade,
    pessoa_id  uuid        not null references public.pessoa (id) on delete restrict,
    criado_em  timestamptz not null default now(),
    primary key (evento_id, pessoa_id)
);
create index ix_coordenador_pessoa on public.coordenador_evento (pessoa_id);

-- Garante, no banco, que o último coordenador não seja removido (RN 1.2).
-- Exclusões em cascata do próprio evento são permitidas.
create or replace function public.impedir_remover_ultimo_coordenador() returns trigger
language plpgsql as $$
begin
    if exists (select 1 from public.evento where id = old.evento_id)
       and not exists (
           select 1 from public.coordenador_evento
           where evento_id = old.evento_id and pessoa_id <> old.pessoa_id
       ) then
        raise exception 'RN-1.2: o evento precisa de ao menos um coordenador';
    end if;
    return old;
end $$;
create trigger trg_ultimo_coordenador before delete on public.coordenador_evento
    for each row execute function public.impedir_remover_ultimo_coordenador();

-- -----------------------------------------------------------------------------
-- Atividade (RF-004)
-- -----------------------------------------------------------------------------
create table public.atividade (
    id             uuid primary key default gen_random_uuid(),
    evento_id      uuid           not null references public.evento (id) on delete cascade,
    titulo         text           not null,
    tipo           tipo_atividade not null,
    area_tematica  text,
    carga_horaria  numeric(6,2)   not null check (carga_horaria > 0),  -- RN 1.4
    inicio         timestamptz    not null,
    fim            timestamptz    not null,
    capacidade     int check (capacidade is null or capacidade > 0),
    paralela       boolean        not null default false,
    criado_em      timestamptz    not null default now(),
    atualizado_em  timestamptz    not null default now(),
    check (fim > inicio)
);
create index ix_atividade_evento on public.atividade (evento_id, inicio);
create trigger trg_atividade_atualizado before update on public.atividade
    for each row execute function public.tocar_atualizado_em();

create table public.atividade_responsavel (
    atividade_id uuid              not null references public.atividade (id) on delete cascade,
    pessoa_id    uuid              not null references public.pessoa (id) on delete restrict,
    papel        papel_responsavel not null,
    primary key (atividade_id, pessoa_id, papel)
);

-- -----------------------------------------------------------------------------
-- Inscrição (RF-006, RF-007)
-- -----------------------------------------------------------------------------
create table public.inscricao (
    id                  uuid primary key default gen_random_uuid(),
    evento_id           uuid                not null references public.evento (id) on delete restrict,
    pessoa_id           uuid                not null references public.pessoa (id) on delete restrict,
    status              status_inscricao    not null default 'pre_inscrita',
    situacao_financeira situacao_financeira not null default 'nao_aplicavel',
    codigo_checkin      text                not null unique default substr(replace(gen_random_uuid()::text, '-', ''), 1, 16),
    motivo_status       text,
    criada_em           timestamptz         not null default now(),
    atualizado_em       timestamptz         not null default now()
);
-- RN 2.3: uma inscrição ativa por pessoa por evento
create unique index uq_inscricao_ativa on public.inscricao (evento_id, pessoa_id)
    where status not in ('cancelada', 'indeferida');
create index ix_inscricao_evento_status on public.inscricao (evento_id, status, criada_em);
create index ix_inscricao_pessoa on public.inscricao (pessoa_id);
create trigger trg_inscricao_atualizado before update on public.inscricao
    for each row execute function public.tocar_atualizado_em();

create table public.inscricao_atividade (
    inscricao_id uuid        not null references public.inscricao (id) on delete cascade,
    atividade_id uuid        not null references public.atividade (id) on delete restrict,
    em_espera    boolean     not null default false,
    criado_em    timestamptz not null default now(),
    primary key (inscricao_id, atividade_id)
);
create index ix_inscricao_atividade_atividade on public.inscricao_atividade (atividade_id);

-- -----------------------------------------------------------------------------
-- Presença (RF-008)
-- -----------------------------------------------------------------------------
create table public.registro_presenca (
    id              uuid primary key default gen_random_uuid(),
    inscricao_id    uuid            not null references public.inscricao (id) on delete restrict,
    atividade_id    uuid            references public.atividade (id) on delete restrict,  -- nulo = evento todo
    check_in        timestamptz     not null,
    check_out       timestamptz,
    origem          origem_presenca not null default 'manual',
    ajuste_manual   boolean         not null default false,
    justificativa   text,
    registrado_por  uuid            references public.pessoa (id),
    criado_em       timestamptz     not null default now(),
    check (check_out is null or check_out >= check_in),
    check (not ajuste_manual or length(coalesce(trim(justificativa), '')) > 0)  -- RN 10.2
);
create index ix_presenca_inscricao on public.registro_presenca (inscricao_id);
create index ix_presenca_atividade on public.registro_presenca (atividade_id);

-- -----------------------------------------------------------------------------
-- Tipo de certificado (RF-009)
-- -----------------------------------------------------------------------------
create table public.tipo_certificado (
    id            uuid primary key default gen_random_uuid(),
    codigo        text        not null unique,
    nome          text        not null,
    descricao     text,
    ativo         boolean     not null default true,
    criado_em     timestamptz not null default now(),
    atualizado_em timestamptz not null default now()
);
create trigger trg_tipo_certificado_atualizado before update on public.tipo_certificado
    for each row execute function public.tocar_atualizado_em();

-- RN 5.3: pares de tipos exclusivos para a mesma pessoa no mesmo evento
create table public.tipo_certificado_exclusividade (
    tipo_a_id uuid not null references public.tipo_certificado (id) on delete cascade,
    tipo_b_id uuid not null references public.tipo_certificado (id) on delete cascade,
    primary key (tipo_a_id, tipo_b_id),
    check (tipo_a_id < tipo_b_id)
);

-- -----------------------------------------------------------------------------
-- Certificado (RF-010) — RN 6.x
-- -----------------------------------------------------------------------------
create table public.certificado (
    id                      uuid primary key default gen_random_uuid(),
    codigo                  text               not null,  -- identificador público, igual entre versões
    versao                  int                not null default 1 check (versao >= 1),
    certificado_anterior_id uuid               references public.certificado (id),
    pessoa_id               uuid               not null references public.pessoa (id) on delete restrict,
    evento_id               uuid               not null references public.evento (id) on delete restrict,
    atividade_id            uuid               references public.atividade (id) on delete restrict,
    tipo_certificado_id     uuid               not null references public.tipo_certificado (id) on delete restrict,  -- RN 5.2
    nome_impresso           text               not null,
    carga_horaria           numeric(6,2)       not null check (carga_horaria >= 0),
    status                  status_certificado not null default 'emitido',
    arquivo_path            text,
    hash_arquivo            text,
    motivo                  text,
    emitido_em              timestamptz        not null default now(),
    emitido_por             uuid               references public.pessoa (id),
    unique (codigo, versao)
);
create index ix_certificado_pessoa on public.certificado (pessoa_id);
create index ix_certificado_evento on public.certificado (evento_id, status);

-- -----------------------------------------------------------------------------
-- Fila de emissão (ADR-04)
-- -----------------------------------------------------------------------------
create table public.job_certificado (
    id            uuid primary key default gen_random_uuid(),
    evento_id     uuid                 not null references public.evento (id) on delete cascade,
    tipo          tipo_job_certificado not null,
    payload       jsonb                not null default '{}'::jsonb,
    status        status_job           not null default 'pendente',
    tentativas    int                  not null default 0,
    total         int,
    processados   int                  not null default 0,
    erro          text,
    criado_por    uuid                 references public.pessoa (id),
    criado_em     timestamptz          not null default now(),
    iniciado_em   timestamptz,
    finalizado_em timestamptz
);
create index ix_job_pendente on public.job_certificado (criado_em) where status = 'pendente';

-- -----------------------------------------------------------------------------
-- Auditoria (RF-011) — append-only (RNF-009)
-- -----------------------------------------------------------------------------
create table public.log_auditoria (
    id             bigint generated always as identity primary key,
    acao           acao_auditoria not null,
    responsavel_id uuid           references public.pessoa (id),  -- nulo = Sistema
    evento_id      uuid           references public.evento (id),
    entidade       text           not null,
    entidade_id    text           not null,
    justificativa  text,
    dados          jsonb          not null default '{}'::jsonb,
    criado_em      timestamptz    not null default now()
);
create index ix_auditoria_filtros on public.log_auditoria (evento_id, acao, criado_em desc);
create index ix_auditoria_responsavel on public.log_auditoria (responsavel_id, criado_em desc);

create or replace function public.bloquear_alteracao_auditoria() returns trigger
language plpgsql as $$
begin
    raise exception 'RNF-009: log_auditoria é imutável (operação % bloqueada)', tg_op;
end $$;
create trigger trg_auditoria_imutavel before update or delete on public.log_auditoria
    for each row execute function public.bloquear_alteracao_auditoria();
create trigger trg_auditoria_sem_truncate before truncate on public.log_auditoria
    for each statement execute function public.bloquear_alteracao_auditoria();

-- -----------------------------------------------------------------------------
-- LGPD (RNF-008)
-- -----------------------------------------------------------------------------
create table public.solicitacao_lgpd (
    id           uuid primary key default gen_random_uuid(),
    pessoa_id    uuid                    not null references public.pessoa (id),
    tipo         tipo_solicitacao_lgpd   not null,
    status       status_solicitacao_lgpd not null default 'aberta',
    detalhes     text,
    criado_em    timestamptz             not null default now(),
    atendido_em  timestamptz,
    atendido_por uuid                    references public.pessoa (id)
);

-- =============================================================================
-- Row Level Security (ADR-03)
-- A API conecta com um papel que ignora RLS. As policies abaixo valem para o
-- acesso direto via SDK (anon/authenticated): só LEITURA do que é do usuário.
-- Nenhuma policy de INSERT/UPDATE/DELETE => escrita via SDK é negada.
-- =============================================================================
create or replace function public.pessoa_atual_id() returns uuid
language sql stable security definer set search_path = public as $$
    select id from public.pessoa where user_id = auth.uid()
$$;

create or replace function public.eh_admin() returns boolean
language sql stable security definer set search_path = public as $$
    select exists (select 1 from public.pessoa where user_id = auth.uid() and perfil = 'administrador')
$$;

create or replace function public.eh_coordenador_do_evento(p_evento_id uuid) returns boolean
language sql stable security definer set search_path = public as $$
    select public.eh_admin() or exists (
        select 1 from public.coordenador_evento
        where evento_id = p_evento_id and pessoa_id = public.pessoa_atual_id()
    )
$$;

alter table public.pessoa                         enable row level security;
alter table public.instituicao                    enable row level security;
alter table public.unidade_organizadora           enable row level security;
alter table public.evento                         enable row level security;
alter table public.coordenador_evento             enable row level security;
alter table public.atividade                      enable row level security;
alter table public.atividade_responsavel          enable row level security;
alter table public.inscricao                      enable row level security;
alter table public.inscricao_atividade            enable row level security;
alter table public.registro_presenca              enable row level security;
alter table public.tipo_certificado               enable row level security;
alter table public.tipo_certificado_exclusividade enable row level security;
alter table public.certificado                    enable row level security;
alter table public.job_certificado                enable row level security;
alter table public.log_auditoria                  enable row level security;
alter table public.solicitacao_lgpd               enable row level security;

create policy pessoa_le_propria on public.pessoa
    for select to authenticated using (user_id = auth.uid() or public.eh_admin());

create policy instituicao_leitura on public.instituicao
    for select to anon, authenticated using (true);
create policy unidade_leitura on public.unidade_organizadora
    for select to anon, authenticated using (true);
create policy tipo_certificado_leitura on public.tipo_certificado
    for select to anon, authenticated using (true);

create policy evento_leitura on public.evento
    for select to anon, authenticated using (publicado or public.eh_coordenador_do_evento(id));
create policy atividade_leitura on public.atividade
    for select to anon, authenticated using (
        exists (select 1 from public.evento e where e.id = evento_id
                and (e.publicado or public.eh_coordenador_do_evento(e.id)))
    );

create policy coordenador_leitura on public.coordenador_evento
    for select to authenticated using (public.eh_coordenador_do_evento(evento_id));

create policy inscricao_leitura on public.inscricao
    for select to authenticated using (
        pessoa_id = public.pessoa_atual_id() or public.eh_coordenador_do_evento(evento_id)
    );

create policy certificado_leitura on public.certificado
    for select to authenticated using (
        pessoa_id = public.pessoa_atual_id() or public.eh_coordenador_do_evento(evento_id)
    );

-- realtime do progresso de emissão (T12)
create policy job_leitura on public.job_certificado
    for select to authenticated using (public.eh_coordenador_do_evento(evento_id));

create policy auditoria_leitura_admin on public.log_auditoria
    for select to authenticated using (public.eh_admin());

create policy lgpd_leitura on public.solicitacao_lgpd
    for select to authenticated using (pessoa_id = public.pessoa_atual_id() or public.eh_admin());

-- Defesa extra para a imutabilidade do log
revoke update, delete, truncate on public.log_auditoria from anon, authenticated;

-- =============================================================================
-- Storage: bucket privado de certificados (download via URL assinada pela API)
-- =============================================================================
insert into storage.buckets (id, name, public)
values ('certificados', 'certificados', false)
on conflict (id) do nothing;
