import type { Session } from "@supabase/supabase-js";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

import { http } from "../lib/api";
import { supabase } from "../lib/supabase";

export type Perfil = "participante" | "coordenador" | "administrador";

export interface Eu {
  user_id: string;
  email: string | null;
  pessoa_id: string | null;
  perfil: Perfil;
  cadastro_completo: boolean;
}

interface AuthContexto {
  session: Session | null;
  eu: Eu | undefined;
  carregando: boolean;
  sair: () => Promise<void>;
}

const Contexto = createContext<AuthContexto | null>(null);

const NIVEL: Record<Perfil, number> = { participante: 0, coordenador: 1, administrador: 2 };

/** Administrador herda coordenador, que herda participante (seção 5.1). */
export function perfilAtende(perfil: Perfil | undefined, minimo: Perfil): boolean {
  return perfil !== undefined && NIVEL[perfil] >= NIVEL[minimo];
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);
  const [sessaoCarregada, setSessaoCarregada] = useState(false);
  const queryClient = useQueryClient();

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session);
      setSessaoCarregada(true);
    });
    const { data } = supabase.auth.onAuthStateChange((_evento, novaSessao) => {
      setSession(novaSessao);
      queryClient.invalidateQueries({ queryKey: ["auth", "me"] });
    });
    return () => data.subscription.unsubscribe();
  }, [queryClient]);

  const { data: eu, isLoading } = useQuery({
    queryKey: ["auth", "me", session?.user.id],
    queryFn: () => http.get<Eu>("/auth/me"),
    enabled: !!session,
  });

  const valor: AuthContexto = {
    session,
    eu,
    carregando: !sessaoCarregada || (!!session && isLoading),
    sair: async () => {
      await supabase.auth.signOut();
      queryClient.clear();
    },
  };

  return <Contexto.Provider value={valor}>{children}</Contexto.Provider>;
}

export function useAuth(): AuthContexto {
  const contexto = useContext(Contexto);
  if (!contexto) throw new Error("useAuth precisa estar dentro de <AuthProvider>");
  return contexto;
}
