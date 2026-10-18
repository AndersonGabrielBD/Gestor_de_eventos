-- Dados iniciais para desenvolvimento (aplicado por `npx supabase db reset`).

insert into public.tipo_certificado (codigo, nome, descricao) values
    ('participante',           'Participante',             'Participação no evento ou atividade'),
    ('ouvinte',                'Ouvinte',                  'Participação como ouvinte'),
    ('palestrante',            'Palestrante',              'Proferiu palestra'),
    ('ministrante',            'Ministrante',              'Ministrou oficina/minicurso'),
    ('mediador',               'Mediador',                 'Mediou mesa-redonda ou sessão'),
    ('comissao_organizadora',  'Comissão Organizadora',    'Integrou a comissão organizadora'),
    ('apresentador_trabalho',  'Apresentador de Trabalho', 'Apresentou trabalho no evento')
on conflict (codigo) do nothing;

-- Exemplo de exclusividade (RN 5.3): a mesma pessoa não recebe "participante" e "ouvinte" no mesmo evento.
insert into public.tipo_certificado_exclusividade (tipo_a_id, tipo_b_id)
select least(a.id, b.id), greatest(a.id, b.id)
from public.tipo_certificado a, public.tipo_certificado b
where a.codigo = 'participante' and b.codigo = 'ouvinte'
on conflict do nothing;

insert into public.instituicao (id, nome, sigla)
values ('00000000-0000-0000-0000-000000000001', 'Centro Universitário Exemplo', 'CUE')
on conflict do nothing;

insert into public.unidade_organizadora (instituicao_id, nome, tipo) values
    ('00000000-0000-0000-0000-000000000001', 'Campus Maceió',          'campus'),
    ('00000000-0000-0000-0000-000000000001', 'Ciência da Computação',  'curso')
on conflict do nothing;
