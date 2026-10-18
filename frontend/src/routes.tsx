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
  card: string; // card do Trello responsável pela tela
  perfil?: Perfil; // ausente = rota pública
}

const TELAS: Tela[] = [
  { path: "/cadastro", tela: "T01", titulo: "Cadastro", card: "Login, cadastro e recuperação de senha (Anderson)" },
  { path: "/recuperar-senha", tela: "T01", titulo: "Recuperar senha", card: "Login, cadastro e recuperação de senha (Anderson)" },
  { path: "/eventos", tela: "T13", titulo: "Catálogo de eventos", card: "Catálogo de eventos (José)" },
  { path: "/eventos/:id", tela: "T13", titulo: "Detalhe do evento", card: "Catálogo de eventos (José)" },
  { path: "/validar", tela: "T17", titulo: "Validação pública", card: "Meus certificados e validação pública (Thayná)" },
  { path: "/validar/:codigo", tela: "T17", titulo: "Validação pública", card: "Meus certificados e validação pública (Thayná)" },

  { path: "/painel", tela: "T02", titulo: "Painel", card: "Dashboard por perfil (Anderson)", perfil: "participante" },
  { path: "/perfil", tela: "—", titulo: "Meu perfil", card: "Cadastro de pessoa e Meu perfil (Anderson)", perfil: "participante" },
  { path: "/eventos/:id/inscricao", tela: "T14", titulo: "Inscrição", card: "Tela de inscrição (Thayná)", perfil: "participante" },
  { path: "/minhas-inscricoes", tela: "T15", titulo: "Minhas inscrições", card: "Minhas inscrições (Pedro)", perfil: "participante" },
  { path: "/meus-certificados", tela: "T16", titulo: "Meus certificados", card: "Meus certificados e validação pública (Thayná)", perfil: "participante" },

  { path: "/coordenacao/eventos", tela: "T07", titulo: "Meus eventos", card: "Criar e gerenciar evento (Anderson)", perfil: "coordenador" },
  { path: "/coordenacao/eventos/novo", tela: "T07", titulo: "Novo evento", card: "Criar e gerenciar evento (Anderson)", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id", tela: "T07", titulo: "Editar evento", card: "Criar e gerenciar evento (Anderson)", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id/coordenadores", tela: "T08", titulo: "Coordenadores", card: "Coordenadores do evento (Thayná)", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id/atividades", tela: "T09", titulo: "Programação", card: "Programação / Atividades (Pedro)", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id/inscritos", tela: "T10", titulo: "Inscritos", card: "Gestão de inscritos (Pedro)", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id/presenca", tela: "T11", titulo: "Check-in / Presença", card: "Check-in e presença (Thayná)", perfil: "coordenador" },
  { path: "/coordenacao/eventos/:id/certificados", tela: "T12", titulo: "Emissão de certificados", card: "Apuração final e Emissão em lote (José)", perfil: "coordenador" },
  { path: "/relatorios", tela: "T06", titulo: "Relatórios", card: "Relatórios oficiais (Pedro)", perfil: "coordenador" },

  { path: "/admin/instituicoes", tela: "T03", titulo: "Instituições e unidades", card: "Tela de Instituições e Unidades (Thayná)", perfil: "administrador" },
  { path: "/admin/tipos-certificado", tela: "T04", titulo: "Tipos de certificado", card: "Tela de Tipos de certificado (Pedro)", perfil: "administrador" },
  { path: "/admin/auditoria", tela: "T05", titulo: "Auditoria", card: "Auditoria (Pedro)", perfil: "administrador" },
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
