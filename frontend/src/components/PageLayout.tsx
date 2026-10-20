import { Box, Container, Group, Paper, Stack, Text, Title } from "@mantine/core";
import type { ReactNode } from "react";

interface PageLayoutProps {
  titulo: string;
  descricao?: string;
  acoes?: ReactNode;
  children: ReactNode;
  estreito?: boolean;
}

export function PageLayout({ titulo, descricao, acoes, children, estreito = false }: PageLayoutProps) {
  return (
    <Container size={estreito ? 500 : "lg"} py="xl">
      <Paper withBorder shadow="sm" p="xl">
        <Stack gap="lg">
          <Box>
            <Group justify="space-between" align="flex-start">
              <div>
                <Title order={1}>{titulo}</Title>
                {descricao && (
                  <Text c="dimmed" mt={4}>
                    {descricao}
                  </Text>
                )}
              </div>
              {acoes}
            </Group>
          </Box>
          {children}
        </Stack>
      </Paper>
    </Container>
  );
}
