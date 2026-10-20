import { useState, type FormEvent } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router";
import { Alert, Stack, Text } from "@mantine/core";

import { useAuth } from "../auth/AuthProvider";
import { supabase } from "../lib/supabase";
import { Botao } from "../components/Botao";
import { CampoFormulario } from "../components/CampoFormulario";
import { PageLayout } from "../components/PageLayout";

/** T01 — Login (UC00). Cadastro: CadastroPage · recuperação: RecuperarSenhaPage. */
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
      setErro(
        error.code === "email_not_confirmed"
          ? "Confirme seu e-mail antes de entrar (veja o link que enviamos)."
          : "E-mail ou senha inválidos.", // UC00 E1
      );
      return;
    }
    navigate(destino, { replace: true });
  }

  return (
    <PageLayout titulo="Entrar" estreito>
      <form onSubmit={entrar} noValidate>
        <Stack gap="md">
          <CampoFormulario
            id="email"
            label="E-mail"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <CampoFormulario
            id="senha"
            label="Senha"
            type="password"
            autoComplete="current-password"
            required
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />

          {erro && (
            <Alert color="erro" role="alert">
              {erro}
            </Alert>
          )}

          <Botao type="submit" carregando={enviando}>
            Entrar
          </Botao>
        </Stack>
      </form>
      <Text component="p" mt="lg">
        <Link to="/recuperar-senha">Esqueci minha senha</Link> · <Link to="/cadastro">Cadastre-se</Link>
      </Text>
    </PageLayout>
  );
}
