import { useState, type FormEvent } from "react";
import { Link, Navigate } from "react-router";
import { Alert, Stack, Text } from "@mantine/core";

import { useAuth } from "../auth/AuthProvider";
import { supabase } from "../lib/supabase";
import { Botao } from "../components/Botao";
import { CampoFormulario } from "../components/CampoFormulario";
import { PageLayout } from "../components/PageLayout";
import { notificar } from "../components/notificar";
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
    if (!data.session) {
      setAguardandoConfirmacao(true);
      notificar.sucesso("Enviamos um link de confirmação para seu e-mail.");
    }
  }

  if (aguardandoConfirmacao) {
    return (
      <PageLayout titulo="Confirme seu e-mail" estreito>
        <Text component="p" role="status">
          Enviamos um link de confirmação para <strong>{email}</strong>. Abra o e-mail e clique no link para
          ativar sua conta.
        </Text>
        <Text component="p">
          <Link to="/login">Voltar para o login</Link>
        </Text>
      </PageLayout>
    );
  }

  return (
    <PageLayout titulo="Criar conta" estreito>
      <form onSubmit={cadastrar} noValidate>
        <Stack gap="md">
          <CampoFormulario
            id="nome"
            label="Nome completo"
            autoComplete="name"
            required
            value={nome}
            onChange={(e) => setNome(e.target.value)}
          />

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
            autoComplete="new-password"
            required
            minLength={SENHA_MINIMA}
            dica={`Mínimo de ${SENHA_MINIMA} caracteres, com letras e números.`}
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />

          <CampoFormulario
            id="confirmacao"
            label="Confirme a senha"
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
            Criar conta
          </Botao>
        </Stack>
      </form>
      <Text component="p" mt="lg">
        Já tem conta? <Link to="/login">Entrar</Link>
      </Text>
    </PageLayout>
  );
}
