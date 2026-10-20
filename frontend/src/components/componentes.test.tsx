import { MantineProvider } from "@mantine/core";
import { ModalsProvider } from "@mantine/modals";
import { fireEvent, render, screen } from "@testing-library/react";
import type { ReactNode } from "react";

import { Botao } from "./Botao";
import { CampoFormulario } from "./CampoFormulario";
import { Modal } from "./Modal";
import { Tabela } from "./Tabela";
import { theme } from "./theme";

function renderComProviders(ui: ReactNode) {
  return render(
    <MantineProvider theme={theme} defaultColorScheme="light">
      <ModalsProvider>{ui}</ModalsProvider>
    </MantineProvider>,
  );
}

describe("Botao", () => {
  it("fica desabilitado enquanto carrega", () => {
    renderComProviders(<Botao carregando>Salvar</Botao>);

    expect(screen.getByRole("button", { name: "Salvar" })).toBeDisabled();
  });
});

describe("CampoFormulario", () => {
  it("associa label, dica e erro ao campo", () => {
    renderComProviders(
      <CampoFormulario label="E-mail" dica="Use seu e-mail institucional" error="E-mail inválido" />,
    );

    const campo = screen.getByLabelText("E-mail");
    expect(campo).toHaveAccessibleDescription("E-mail inválido Use seu e-mail institucional");
  });
});

describe("Tabela", () => {
  it("mantém cabeçalhos e exibe o estado vazio", () => {
    renderComProviders(<Tabela legenda="Pessoas inscritas" cabecalhos={["Nome", "E-mail"]} linhas={[]} />);

    expect(screen.getByRole("table", { name: "Pessoas inscritas" })).toBeInTheDocument();
    expect(screen.getAllByRole("columnheader")).toHaveLength(2);
    expect(screen.getByText("Nenhum registro encontrado.")).toBeInTheDocument();
  });
});

describe("Modal", () => {
  it("abre e fecha pelo controle acessível", () => {
    const onClose = vi.fn();
    renderComProviders(
      <Modal opened onClose={onClose} titulo="Confirmar exclusão">
        Conteúdo
      </Modal>,
    );

    expect(screen.getByRole("dialog", { name: "Confirmar exclusão" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Fechar modal" }));
    expect(onClose).toHaveBeenCalledOnce();
  });
});
