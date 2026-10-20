import { NavLink, Outlet } from "react-router";
import {
  AppShell,
  Burger,
  Button,
  Group,
  NavLink as MantineNavLink,
  ScrollArea,
  Stack,
  Text,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";

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
  const [aberto, { toggle, close }] = useDisclosure();
  const itens = MENU.filter((i) => !i.perfil || (session && perfilAtende(eu?.perfil, i.perfil)));

  return (
    <>
      <a className="pular-conteudo" href="#conteudo">
        Pular para o conteúdo
      </a>
      <AppShell
        header={{ height: 64 }}
        navbar={{ width: 280, breakpoint: "sm", collapsed: { mobile: !aberto } }}
        padding={0}
      >
        <AppShell.Header>
          <Group h="100%" px="md" justify="space-between">
            <Group>
              <Burger opened={aberto} onClick={toggle} hiddenFrom="sm" size="sm" aria-label="Alternar menu" />
              <Text fw={700}>Gestão de Eventos</Text>
            </Group>
            {session ? (
              <Button variant="subtle" onClick={sair}>
                Sair
              </Button>
            ) : (
              <Button component={NavLink} to="/login" variant="subtle">
                Entrar
              </Button>
            )}
          </Group>
        </AppShell.Header>
        <AppShell.Navbar p="md">
          <AppShell.Section grow component={ScrollArea}>
            <nav aria-label="Principal">
              <Stack gap={4}>
                {itens.map((item) => (
                  <MantineNavLink
                    key={item.rota}
                    component={NavLink}
                    to={item.rota}
                    label={item.rotulo}
                    onClick={close}
                  />
                ))}
              </Stack>
            </nav>
          </AppShell.Section>
        </AppShell.Navbar>
        <AppShell.Main id="conteudo" tabIndex={-1}>
          <Outlet />
        </AppShell.Main>
      </AppShell>
    </>
  );
}
