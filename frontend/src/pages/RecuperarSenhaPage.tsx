import { useState, type FormEvent } from "react";
import { Link } from "react-router";

import { supabase } from "../lib/supabase";

/** T01 — Esqueci minha senha (UC00). O Supabase Auth envia o e-mail com o link
 * para /redefinir-senha. */
export function RecuperarSenhaPage() {
  const [email, setEmail] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [enviado, setEnviado] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  async function enviar(evento: FormEvent) {
    evento.preventDefault();
    setEnviando(true);
    setErro(null);
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/redefinir-senha`,
    });
    setEnviando(false);
    // Limite de envios estourado é o único erro que vale mostrar; nos demais casos a
    // mensagem é sempre a mesma, para não revelar quais e-mails têm conta.
    if (error?.status === 429) {
      setErro("Muitas tentativas. Aguarde alguns minutos e tente de novo.");
      return;
    }
    setEnviado(true);
  }

  if (enviado) {
    return (
      <section className="cartao estreito">
        <h1>Verifique seu e-mail</h1>
        <p role="status">
          Se houver uma conta para <strong>{email}</strong>, você vai receber um link para criar uma
          nova senha.
        </p>
        <p>
          <Link to="/login">Voltar para o login</Link>
        </p>
      </section>
    );
  }

  return (
    <section className="cartao estreito">
      <h1>Recuperar senha</h1>
      <form onSubmit={enviar} noValidate>
        <label htmlFor="email">E-mail da conta</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {erro && (
          <p role="alert" className="erro">
            {erro}
          </p>
        )}
        <button type="submit" disabled={enviando || !email}>
          {enviando ? "Enviando…" : "Enviar link"}
        </button>
      </form>
      <p>
        <Link to="/login">Voltar para o login</Link>
      </p>
    </section>
  );
}
