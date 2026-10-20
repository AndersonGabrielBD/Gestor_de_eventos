import { useState, type FormEvent } from "react";
import { Link } from "react-router";
import { Alert, Stack, Text } from "@mantine/core";

import { supabase } from "../lib/supabase";
import { Botao } from "../components/Botao";
import { CampoFormulario } from "../components/CampoFormulario";
import { notificar } from "../components/notificar";
import { PageLayout } from "../components/PageLayout";

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
    notificar.sucesso("Se houver uma conta, enviamos o link de recuperação.");
  }

  if (enviado) {
    return (
      <PageLayout titulo="Verifique seu e-mail" estreito>
        <Text component="p" role="status">
          Se houver uma conta para <strong>{email}</strong>, você vai receber um link para criar uma nova
          senha.
        </Text>
        <Text component="p">
          <Link to="/login">Voltar para o login</Link>
        </Text>
      </PageLayout>
    );
  }

  return (
    <PageLayout titulo="Recuperar senha" estreito>
      <form onSubmit={enviar} noValidate>
        <Stack gap="md">
          <CampoFormulario
            id="email"
            label="E-mail da conta"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          {erro && (
            <Alert color="erro" role="alert">
              {erro}
            </Alert>
          )}
          <Botao type="submit" carregando={enviando} disabled={!email}>
            Enviar link
          </Botao>
        </Stack>
      </form>
      <Text component="p" mt="lg">
        <Link to="/login">Voltar para o login</Link>
      </Text>
    </PageLayout>
  );
}
