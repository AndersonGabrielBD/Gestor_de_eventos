import { perfilAtende } from "./AuthProvider";

describe("perfilAtende", () => {
  it("administrador herda as permissões de coordenador", () => {
    expect(perfilAtende("administrador", "coordenador")).toBe(true);
  });

  it("participante não acessa área de coordenador", () => {
    expect(perfilAtende("participante", "coordenador")).toBe(false);
  });

  it("sem perfil carregado nega acesso", () => {
    expect(perfilAtende(undefined, "participante")).toBe(false);
  });
});
