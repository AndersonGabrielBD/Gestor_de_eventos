import { Button, type ButtonProps } from "@mantine/core";
import type { ReactNode } from "react";

export type VarianteBotao = "primario" | "secundario" | "perigo";

interface BotaoProps extends Omit<ButtonProps, "variant" | "color" | "loading"> {
  children: ReactNode;
  carregando?: boolean;
  variante?: VarianteBotao;
  type?: "button" | "submit" | "reset";
}

const estilos: Record<VarianteBotao, Pick<ButtonProps, "variant" | "color">> = {
  primario: { variant: "filled", color: "institucional" },
  secundario: { variant: "outline", color: "institucional" },
  perigo: { variant: "filled", color: "erro" },
};

export function Botao({
  carregando = false,
  variante = "primario",
  children,
  disabled,
  ...props
}: BotaoProps) {
  return (
    <Button {...estilos[variante]} {...props} loading={carregando} disabled={disabled || carregando}>
      {children}
    </Button>
  );
}
