-- =============================================================================
-- Card "Login, cadastro de conta e recuperação de senha" (UC00, ADR-02)
-- Toda conta criada no Supabase Auth ganha uma `pessoa` com perfil participante.
-- O restante do cadastro (CPF, matrícula, categoria, aceite LGPD) é completado
-- em "Meu perfil" (card "Cadastro de pessoa").
-- =============================================================================

create or replace function public.criar_pessoa_do_usuario() returns trigger
language plpgsql security definer set search_path = public as $$
begin
    insert into public.pessoa (user_id, nome, email)
    values (
        new.id,
        coalesce(nullif(trim(new.raw_user_meta_data ->> 'nome'), ''), split_part(new.email, '@', 1)),
        new.email
    )
    -- Já existe pessoa com esse e-mail sem conta (ex.: palestrante externo cadastrado
    -- pelo coordenador): vincula a conta a ela em vez de duplicar.
    on conflict (email) do update
        set user_id = excluded.user_id
        where public.pessoa.user_id is null;
    return new;
end;
$$;

create trigger trg_auth_cria_pessoa
    after insert on auth.users
    for each row execute function public.criar_pessoa_do_usuario();

-- Mantém o e-mail da pessoa igual ao da conta quando o usuário troca de e-mail.
create or replace function public.sincronizar_email_pessoa() returns trigger
language plpgsql security definer set search_path = public as $$
begin
    update public.pessoa set email = new.email where user_id = new.id;
    return new;
end;
$$;

create trigger trg_auth_sincroniza_email
    after update of email on auth.users
    for each row
    when (old.email is distinct from new.email)
    execute function public.sincronizar_email_pessoa();

-- As funções rodam só pelo trigger; ninguém chama via API/SDK.
revoke execute on function public.criar_pessoa_do_usuario() from public, anon, authenticated;
revoke execute on function public.sincronizar_email_pessoa() from public, anon, authenticated;
