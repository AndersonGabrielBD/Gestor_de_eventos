import { notifications } from "@mantine/notifications";

type TipoNotificacao = "sucesso" | "erro" | "informacao";

const cores: Record<TipoNotificacao, string> = {
  sucesso: "sucesso",
  erro: "erro",
  informacao: "institucional",
};

export function notificar(tipo: TipoNotificacao, mensagem: string, titulo?: string) {
  notifications.show({
    color: cores[tipo],
    title: titulo,
    message: mensagem,
    autoClose: tipo === "erro" ? false : 5000,
  });
}

notificar.sucesso = (mensagem: string, titulo?: string) => notificar("sucesso", mensagem, titulo);
notificar.erro = (mensagem: string, titulo?: string) => notificar("erro", mensagem, titulo);
notificar.informacao = (mensagem: string, titulo?: string) => notificar("informacao", mensagem, titulo);
