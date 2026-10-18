import { NavLink, Outlet } from "react-router";

import { perfilAtende, useAuth, type Perfil } from "../auth/AuthProvider";

interface ItemMenu {
  rota: string;
  rotulo: string;
  perfil?: Perfil; // ausente = público
}

// Arquitetura de informação — seção 8.1 do documento
const MENU: ItemMenu[] = [
  { rota: "/eventos", rotulo: "Eventos" },
  { rota: "/validar", rotulo: "Validar certificado" },
  { rota: "/painel", rotulo: "Painel", perfil: "participante" },
  { rota: "/minhas-inscricoes", rotulo: "Minhas inscrições", perfil: "participante" },
  { rota: "/meus-certificados", rotulo: "Meus certificados", perfil: "participante" },
  { rota: "/coordenacao/eventos", rotulo: "Meus eventos", perfil: "coordenador" },
  { rota: "/relatorios", rotulo: "Relatórios", perfil: "coordenador" },
  { rota: "/admin/instituicoes", rotulo: "Instituições", perfil: "administrador" },
  { rota: "/admin/tipos-certificado", rotulo: "Tipos de certificado", perfil: "administrador" },
  { rota: "/admin/auditoria", rotulo: "Auditoria", perfil: "administrador" },
];

export function AppLayout() {
  const { session, eu, sair } = useAuth();
  const itens = MENU.filter((i) => !i.perfil || (session && perfilAtende(eu?.perfil, i.perfil)));

  return (
    <>
      <a className="pular-conteudo" href="#conteudo">
        Pular para o conteúdo
      </a>
      <header className="topo">
        <strong>Gestão de Eventos</strong>
        <nav aria-label="Principal">
          <ul>
            {itens.map((item) => (
              <li key={item.rota}>
                <NavLink to={item.rota}>{item.rotulo}</NavLink>
              </li>
            ))}
          </ul>
        </nav>
        {session ? (
          <button type="button" onClick={sair}>
            Sair
          </button>
        ) : (
          <NavLink to="/login">Entrar</NavLink>
        )}
      </header>
      <main id="conteudo" tabIndex={-1}>
        <Outlet />
      </main>
    </>
  );
}
