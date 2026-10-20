/** Placeholder das telas ainda não implementadas. Substitua pelo componente real
 * da tela ao pegar o item do backlog correspondente. */
export function EmConstrucao({ tela, titulo, card }: { tela: string; titulo: string; card: string }) {
  return (
    <PageLayout titulo={`${tela} — ${titulo}`}>
      <Text>Tela em construção. Card no Trello: {card}.</Text>
    </PageLayout>
  );
}

export function NaoEncontrado() {
  return (
    <PageLayout titulo="Página não encontrada">
      <Text>Verifique o endereço e tente novamente.</Text>
    </PageLayout>
  );
}
import { Text } from "@mantine/core";

import { PageLayout } from "../components/PageLayout";
