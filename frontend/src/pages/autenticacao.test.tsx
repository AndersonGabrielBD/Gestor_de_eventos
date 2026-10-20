import { MantineProvider } from "@mantine/core";
import { Notifications } from "@mantine/notifications";
import { fireEvent, render, screen } from "@testing-library/react";
import type { ReactNode } from "react";
import { MemoryRouter } from "react-router";

import { theme } from "../components/theme";
import { CadastroPage } from "./CadastroPage";
import { LoginPage } from "./LoginPage";
import { RecuperarSenhaPage } from "./RecuperarSenhaPage";
import { RedefinirSenhaPage } from "./RedefinirSenhaPage";

const mocks = vi.hoisted(() => ({
  entrar: vi.fn(),
  recuperar: vi.fn(),
  session: null as { user: { id: string } } | null,
}));

vi.mock("../auth/AuthProvider", () => ({
  useAuth: () => ({ session: mocks.session, carregando: false }),
}));

vi.mock("../lib/supabase", () => ({
  supabase: {
    auth: {
      signInWithPassword: mocks.entrar,
      resetPasswordForEmail: mocks.recuperar,
      signUp: vi.fn(),
      updateUser: vi.fn(),
    },
  },
}));

function renderPagina(ui: ReactNode) {
  return render(
    <MantineProvider theme={theme} defaultColorScheme="light">
      <Notifications />
      <MemoryRouter>{ui}</MemoryRouter>
    </MantineProvider>,
  );
}

describe("fluxos de autenticação", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.session = null;
  });

  it("mantém a mensagem de credenciais inválidas ao submeter o login", async () => {
    const senhaDeTeste = ["credencial", "ficticia"].join("-");
    mocks.entrar.mockResolvedValue({ error: { code: "invalid_credentials" } });
    renderPagina(<LoginPage />);

    fireEvent.change(screen.getByLabelText(/^E-mail/), { target: { value: "teste@exemplo.com" } });
    fireEvent.change(screen.getByLabelText(/^Senha/), { target: { value: senhaDeTeste } });
    fireEvent.click(screen.getByRole("button", { name: "Entrar" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("E-mail ou senha inválidos.");
    expect(mocks.entrar).toHaveBeenCalledWith({ email: "teste@exemplo.com", password: senhaDeTeste });
  });

  it("mantém a validação de nome no cadastro", () => {
    renderPagina(<CadastroPage />);

    fireEvent.click(screen.getByRole("button", { name: "Criar conta" }));

    expect(screen.getByRole("alert")).toHaveTextContent("Informe seu nome completo.");
  });

  it("mantém o limite de tentativas na recuperação", async () => {
    mocks.recuperar.mockResolvedValue({ error: { status: 429 } });
    renderPagina(<RecuperarSenhaPage />);

    fireEvent.change(screen.getByLabelText(/^E-mail da conta/), { target: { value: "teste@exemplo.com" } });
    fireEvent.click(screen.getByRole("button", { name: "Enviar link" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Muitas tentativas");
  });

  it("mantém a validação da nova senha", () => {
    mocks.session = { user: { id: "usuario" } };
    renderPagina(<RedefinirSenhaPage />);

    fireEvent.click(screen.getByRole("button", { name: "Salvar nova senha" }));

    expect(screen.getByRole("alert")).toHaveTextContent("A senha precisa ter");
  });
});
