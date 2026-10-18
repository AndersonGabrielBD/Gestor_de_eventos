import { createClient } from "@supabase/supabase-js";

// O SDK é usado só para sessão (login) e realtime (ADR-02/ADR-03). Dados vêm da API.
const url = import.meta.env.VITE_SUPABASE_URL ?? "http://127.0.0.1:54321";
const chaveAnon = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!chaveAnon) {
  console.warn("VITE_SUPABASE_ANON_KEY não configurada — veja frontend/.env.example");
}

export const supabase = createClient(url, chaveAnon || "chave-nao-configurada");
