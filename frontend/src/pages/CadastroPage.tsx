import { useState, type FormEvent } from "react";
import { Link, Navigate } from "react-router";

import { useAuth } from "../auth/AuthProvider";
import { supabase } from "../lib/supabase";
import { SENHA_MINIMA, validarNovaSenha } from "./senha";

/** T01 — Cadastro de conta (UC00). A `pessoa` é criada por trigger no banco;
 * os demais dados (CPF, matrícula, aceite LGPD) são completados em "Meu perfil". */
export function CadastroPage() {
  const { session } = useAuth();
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [confirmacao, setConfirmacao] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [aguardandoConfirmacao, setAguardandoConfirmacao] = useState(false);

  if (session) return <Navigate to="/perfil" replace />;

  async function cadastrar(evento: FormEvent) {
    evento.preventDefault();
    setErro(null);
    if (nome.trim().length < 3) return setErro("Informe seu nome completo.");
    const erroSenha = validarNovaSenha(senha, confirmacao);
    if (erroSenha) return setErro(erroSenha);

    setEnviando(true);
    const { data, error } = await supabase.auth.signUp({
      email,
      password: senha,
      options: {
        data: { nome: nome.trim() },
        emailRedirectTo: `${window.location.origin}/perfil`,
      },
    });
    setEnviando(false);

    if (error) {
      setErro(
        error.code === "user_already_exists"
          ? "Já existe uma conta com este e-mail. Tente entrar ou recuperar a senha."
          : "Não foi possível criar a conta. Confira os dados e tente novamente.",
      );
      return;
    }
    // Com confirmação de e-mail ligada (padrão no Supabase), não vem sessão.
    if (!data.session) setAguardandoConfirmacao(true);
  }

  if (aguardandoConfirmacao) {
    return (
      <section className="cartao estreito">
        <h1>Confirme seu e-mail</h1>
        <p role="status">
          Enviamos um link de confirmação para <strong>{email}</strong>. Abra o e-mail e clique no
          link para ativar sua conta.
        </p>
        <p>
          <Link to="/login">Voltar para o login</Link>
        </p>
      </section>
    );
  }

  return (
    <section className="cartao estreito">
      <h1>Criar conta</h1>
      <form onSubmit={cadastrar} noValidate>
        <label htmlFor="nome">Nome completo</label>
        <input
          id="nome"
          autoComplete="name"
          required
          value={nome}
          onChange={(e) => setNome(e.target.value)}
        />

        <label htmlFor="email">E-mail</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <label htmlFor="senha">Senha</label>
        <input
          id="senha"
          type="password"
          autoComplete="new-password"
          required
          minLength={SENHA_MINIMA}
          aria-describedby="dica-senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
        <small id="dica-senha">Mínimo de {SENHA_MINIMA} caracteres, com letras e números.</small>

        <label htmlFor="confirmacao">Confirme a senha</label>
        <input
          id="confirmacao"
          type="password"
          autoComplete="new-password"
          required
          value={confirmacao}
          onChange={(e) => setConfirmacao(e.target.value)}
        />

        {erro && (
          <p role="alert" className="erro">
            {erro}
          </p>
        )}

        <button type="submit" disabled={enviando}>
          {enviando ? "Criando conta…" : "Criar conta"}
        </button>
      </form>
      <p>
        Já tem conta? <Link to="/login">Entrar</Link>
      </p>
    </section>
  );
}
