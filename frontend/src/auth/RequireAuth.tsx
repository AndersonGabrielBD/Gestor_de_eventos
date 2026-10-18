import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router";

import { perfilAtende, useAuth, type Perfil } from "./AuthProvider";

/** Protege uma rota: exige sessão e, opcionalmente, um perfil mínimo. */
export function RequireAuth({
  perfilMinimo = "participante",
  children,
}: {
  perfilMinimo?: Perfil;
  children: ReactNode;
}) {
  const { session, eu, carregando } = useAuth();
  const location = useLocation();

  if (carregando) return <p role="status">Carregando…</p>;
  if (!session) return <Navigate to="/login" replace state={{ de: location.pathname }} />;
  if (!perfilAtende(eu?.perfil, perfilMinimo)) {
    return (
      <section>
        <h1>Acesso negado</h1>
        <p>Seu perfil não tem permissão para acessar esta página.</p>
      </section>
    );
  }
  return <>{children}</>;
}
