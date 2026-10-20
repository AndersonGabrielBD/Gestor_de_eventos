import { Box, Table as MantineTable, Text } from "@mantine/core";
import type { ReactNode } from "react";

interface TabelaProps {
  legenda: string;
  cabecalhos: ReactNode[];
  linhas: ReactNode[][];
  mensagemVazia?: string;
}

export function Tabela({
  legenda,
  cabecalhos,
  linhas,
  mensagemVazia = "Nenhum registro encontrado.",
}: TabelaProps) {
  return (
    <Box style={{ overflowX: "auto" }}>
      <MantineTable striped highlightOnHover withTableBorder withColumnBorders>
        <caption>{legenda}</caption>
        <MantineTable.Thead>
          <MantineTable.Tr>
            {cabecalhos.map((cabecalho, indice) => (
              <MantineTable.Th key={indice}>{cabecalho}</MantineTable.Th>
            ))}
          </MantineTable.Tr>
        </MantineTable.Thead>
        <MantineTable.Tbody>
          {linhas.length > 0 ? (
            linhas.map((linha, indice) => (
              <MantineTable.Tr key={indice}>
                {linha.map((celula, coluna) => (
                  <MantineTable.Td key={coluna}>{celula}</MantineTable.Td>
                ))}
              </MantineTable.Tr>
            ))
          ) : (
            <MantineTable.Tr>
              <MantineTable.Td colSpan={cabecalhos.length}>
                <Text c="dimmed">{mensagemVazia}</Text>
              </MantineTable.Td>
            </MantineTable.Tr>
          )}
        </MantineTable.Tbody>
      </MantineTable>
    </Box>
  );
}
