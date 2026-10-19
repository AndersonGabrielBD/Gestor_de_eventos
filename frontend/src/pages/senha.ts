export const SENHA_MINIMA = 8;

/** Regras da senha nova (cadastro e redefinição). Retorna a mensagem de erro ou null. */
export function validarNovaSenha(senha: string, confirmacao: string): string | null {
  if (senha.length < SENHA_MINIMA) return `A senha precisa ter pelo menos ${SENHA_MINIMA} caracteres.`;
  if (!/[a-zA-Z]/.test(senha) || !/\d/.test(senha)) return "A senha precisa ter letras e números.";
  if (senha !== confirmacao) return "As senhas não conferem.";
  return null;
}
