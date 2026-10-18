/** Placeholder das telas ainda não implementadas. Substitua pelo componente real
 * da tela ao pegar o item do backlog correspondente. */
export function EmConstrucao({ tela, titulo, backlog }: { tela: string; titulo: string; backlog: string }) {
  return (
    <section>
      <h1>
        {tela} — {titulo}
      </h1>
      <p>Tela em construção. Itens do backlog: {backlog}.</p>
    </section>
  );
}

export function NaoEncontrado() {
  return (
    <section>
      <h1>Página não encontrada</h1>
    </section>
  );
}
