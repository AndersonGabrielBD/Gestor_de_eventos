import { describe, expect, it } from "vitest";

import { validarNovaSenha } from "./senha";

describe("validarNovaSenha", () => {
  it("aceita senha com 8+ caracteres, letras e números, igual à confirmação", () => {
    expect(validarNovaSenha("abc12345", "abc12345")).toBeNull();
  });

  it("rejeita senha curta", () => {
    expect(validarNovaSenha("ab12", "ab12")).toMatch(/8 caracteres/);
  });

  it("rejeita senha sem números ou sem letras", () => {
    expect(validarNovaSenha("abcdefgh", "abcdefgh")).toMatch(/letras e números/);
    expect(validarNovaSenha("12345678", "12345678")).toMatch(/letras e números/);
  });

  it("rejeita confirmação diferente", () => {
    expect(validarNovaSenha("abc12345", "abc12346")).toMatch(/não conferem/);
  });
});
