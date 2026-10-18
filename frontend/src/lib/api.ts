import { supabase } from "./supabase";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

/** Erro padronizado da API: `codigo` traz a RN violada (ex.: "RN-1.1"). */
export class ErroApi extends Error {
  constructor(
    public status: number,
    public codigo: string,
    mensagem: string,
  ) {
    super(mensagem);
  }
}

export async function api<T>(caminho: string, opcoes: RequestInit = {}): Promise<T> {
  const { data } = await supabase.auth.getSession();
  const token = data.session?.access_token;

  const resposta = await fetch(`${BASE_URL}${caminho}`, {
    ...opcoes,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...opcoes.headers,
    },
  });

  if (!resposta.ok) {
    const corpo = await resposta.json().catch(() => ({}));
    throw new ErroApi(
      resposta.status,
      corpo.codigo ?? String(resposta.status),
      corpo.mensagem ?? corpo.detail ?? "Erro inesperado. Tente novamente.",
    );
  }
  return resposta.status === 204 ? (undefined as T) : resposta.json();
}

export const http = {
  get: <T>(caminho: string) => api<T>(caminho),
  post: <T>(caminho: string, corpo?: unknown) =>
    api<T>(caminho, { method: "POST", body: JSON.stringify(corpo ?? {}) }),
  put: <T>(caminho: string, corpo: unknown) =>
    api<T>(caminho, { method: "PUT", body: JSON.stringify(corpo) }),
  delete: <T>(caminho: string) => api<T>(caminho, { method: "DELETE" }),
};
