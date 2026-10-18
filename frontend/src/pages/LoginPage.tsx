import { useState, type FormEvent } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router";

import { useAuth } from "../auth/AuthProvider";
import { supabase } from "../lib/supabase";

/** T01 — Login (UC00). Cadastro e recuperação de senha: card "Login, cadastro e recuperação de senha". */
export function LoginPage() {
  const { session } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const destino = (location.state as { de?: string } | null)?.de ?? "/painel";

  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  if (session) return <Navigate to={destino} replace />;

  async function entrar(evento: FormEvent) {
    evento.preventDefault();
    setEnviando(true);
    setErro(null);
    const { error } = await supabase.auth.signInWithPassword({ email, password: senha });
    setEnviando(false);
    if (error) {
      setErro("E-mail ou senha inválidos."); // UC00 E1
      return;
    }
    navigate(destino, { replace: true });
  }

  return (
    <section className="cartao estreito">
      <h1>Entrar</h1>
      <form onSubmit={entrar} noValidate>
        <label htmlFor="email">E-mail</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          aria-describedby={erro ? "erro-login" : undefined}
        />

        <label htmlFor="senha">Senha</label>
        <input
          id="senha"
          type="password"
          autoComplete="current-password"
          required
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          aria-describedby={erro ? "erro-login" : undefined}
        />

        {erro && (
          <p id="erro-login" role="alert" className="erro">
            {erro}
          </p>
        )}

        <button type="submit" disabled={enviando}>
          {enviando ? "Entrando…" : "Entrar"}
        </button>
      </form>
      <p>
        <Link to="/recuperar-senha">Esqueci minha senha</Link> ·{" "}
        <Link to="/cadastro">Cadastre-se</Link>
      </p>
    </section>
  );
}
