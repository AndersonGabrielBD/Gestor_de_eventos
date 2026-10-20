import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router";
import { Alert, Stack, Text } from "@mantine/core";

import { useAuth } from "../auth/AuthProvider";
import { supabase } from "../lib/supabase";
import { Botao } from "../components/Botao";
import { CampoFormulario } from "../components/CampoFormulario";
import { notificar } from "../components/notificar";
import { PageLayout } from "../components/PageLayout";
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

  if (carregando)
    return (
      <Text role="status" p="xl">
        Carregando…
      </Text>
    );

  if (!session) {
    return (
      <PageLayout titulo="Link inválido ou expirado" estreito>
        <Text component="p">Peça um novo link de recuperação de senha.</Text>
        <Text component="p">
          <Link to="/recuperar-senha">Recuperar senha</Link>
        </Text>
      </PageLayout>
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
    notificar.sucesso("Sua nova senha foi salva.");
    navigate("/painel", { replace: true });
  }

  return (
    <PageLayout titulo="Criar nova senha" estreito>
      <form onSubmit={salvar} noValidate>
        <Stack gap="md">
          <CampoFormulario
            id="senha"
            label="Nova senha"
            type="password"
            autoComplete="new-password"
            required
            minLength={SENHA_MINIMA}
            dica={`Mínimo de ${SENHA_MINIMA} caracteres, com letras e números.`}
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />

          <CampoFormulario
            id="confirmacao"
            label="Confirme a nova senha"
            type="password"
            autoComplete="new-password"
            required
            value={confirmacao}
            onChange={(e) => setConfirmacao(e.target.value)}
          />

          {erro && (
            <Alert color="erro" role="alert">
              {erro}
            </Alert>
          )}

          <Botao type="submit" carregando={enviando}>
            Salvar nova senha
          </Botao>
        </Stack>
      </form>
    </PageLayout>
  );
}
