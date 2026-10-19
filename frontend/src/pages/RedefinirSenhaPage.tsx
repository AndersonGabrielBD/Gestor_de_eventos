import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router";

import { useAuth } from "../auth/AuthProvider";
import { supabase } from "../lib/supabase";
import { SENHA_MINIMA, validarNovaSenha } from "./senha";

/** T01 — Nova senha. O link do e-mail de recuperação abre esta página já com uma
 * sessão temporária (o supabase-js lê o token da URL). */
export function RedefinirSenhaPage() {
  const { session, carregando } = useAuth();
  const navigate = useNavigate();
  const [senha, setSenha] = useState("");
  const [confirmacao, setConfirmacao] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  if (carregando) return <p role="status">Carregando…</p>;

  if (!session) {
    return (
      <section className="cartao estreito">
        <h1>Link inválido ou expirado</h1>
        <p>Peça um novo link de recuperação de senha.</p>
        <p>
          <Link to="/recuperar-senha">Recuperar senha</Link>
        </p>
      </section>
    );
  }

  async function salvar(evento: FormEvent) {
    evento.preventDefault();
    setErro(null);
    const erroSenha = validarNovaSenha(senha, confirmacao);
    if (erroSenha) return setErro(erroSenha);

    setEnviando(true);
    const { error } = await supabase.auth.updateUser({ password: senha });
    setEnviando(false);
    if (error) {
      setErro(
        error.code === "same_password"
          ? "A nova senha precisa ser diferente da anterior."
          : "Não foi possível salvar a nova senha. Tente novamente.",
      );
      return;
    }
    navigate("/painel", { replace: true });
  }

  return (
    <section className="cartao estreito">
      <h1>Criar nova senha</h1>
      <form onSubmit={salvar} noValidate>
        <label htmlFor="senha">Nova senha</label>
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

        <label htmlFor="confirmacao">Confirme a nova senha</label>
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
          {enviando ? "Salvando…" : "Salvar nova senha"}
        </button>
      </form>
    </section>
  );
}
