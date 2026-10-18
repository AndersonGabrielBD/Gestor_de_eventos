import { Navigate, type RouteObject } from "react-router";

import { type Perfil } from "./auth/AuthProvider";
import { RequireAuth } from "./auth/RequireAuth";
import { AppLayout } from "./layouts/AppLayout";
import { EmConstrucao, NaoEncontrado } from "./pages/EmConstrucao";
import { LoginPage } from "./pages/LoginPage";

/** Mapa de telas — docs/06-frontend.md. */
interface Tela {
  path: string;
  tela: string;
  titulo: string;
  backlog: string;
  perfil?: Perfil; // ausente = rota pública
}

const TELAS: Tela[] = [
  { path: "/cadastro", tela: "T01", titulo: "Cadastro", backlog: "GE-025" },
  { path: "/recuperar-senha", tela: "T01", titulo: "Recuperar senha", backlog: "GE-025" },
  { path: "/eventos", tela: "T13", titulo: "Catálogo de eventos", backlog: "GE-079" },
  { path: "/eventos/:id", tela: "T13", titulo: "Detalhe do evento", backlog: "GE-079" },
  { path: "/validar", tela: "T17", titulo: "Validação pública", backlog: "GE-10F" },
  { path: "/validar/:codigo", tela: "T17", titulo: "Validação pública", backlog: "GE-10F" },

  { path: "/painel", tela: "T02", titulo: "Painel", backlog: "GE-114", perfil: "participante" },
  { path: "/perfil", tela: "—", titulo: "Meu perfil", backlog: "GE-064", perfil: "participante" },
  { path: "/eventos/:id/inscricao", tela: "T14", titulo: "Inscrição", backlog: "GE-07A", perfil: "participante" },
  { path: "/minhas-inscricoes", tela: "T15", titulo: "Minhas inscrições", backlog: "GE-07B", perfil: "participante" },
  { path: "/meus-certificados", tela: "T16", titulo: "Meus certificados", backlog: "GE-10E", perfil: "participante" },

  { path: "/coordenacao/eventos", tela: "T07", titulo: "Meus eventos", backlog: "GE-037", perfil: "coordenador" },
  { path: "/coordenacao/eventos/novo", tela: "T07", titulo: "Novo evento", backlog: "GE-038", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id", tela: "T07", titulo: "Editar evento", backlog: "GE-038", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id/coordenadores", tela: "T08", titulo: "Coordenadores", backlog: "GE-039", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id/atividades", tela: "T09", titulo: "Programação", backlog: "GE-055", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id/inscritos", tela: "T10", titulo: "Inscritos", backlog: "GE-07C", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id/presenca", tela: "T11", titulo: "Check-in / Presença", backlog: "GE-095, GE-096", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id/certificados", tela: "T12", titulo: "Emissão de certificados", backlog: "GE-10D", perfil: "coordenador" },
  { path: "/relatorios", tela: "T06", titulo: "Relatórios", backlog: "GE-112", perfil: "coordenador" },

  { path: "/admin/instituicoes", tela: "T03", titulo: "Instituições e unidades", backlog: "GE-044", perfil: "administrador" },
  { path: "/admin/tipos-certificado", tela: "T04", titulo: "Tipos de certificado", backlog: "GE-101", perfil: "administrador" },
  { path: "/admin/auditoria", tela: "T05", titulo: "Auditoria", backlog: "GE-085", perfil: "administrador" },
];

export const routes: RouteObject[] = [
  {
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/eventos" replace /> },
      { path: "/login", element: <LoginPage /> },
      ...TELAS.map(({ path, perfil, ...tela }) => {
        const pagina = <EmConstrucao {...tela} />;
        return {
          path,
          element: perfil ? <RequireAuth perfilMinimo={perfil}>{pagina}</RequireAuth> : pagina,
        };
      }),
      { path: "*", element: <NaoEncontrado /> },
    ],
  },
];
