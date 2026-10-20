import { TextInput, type TextInputProps } from "@mantine/core";

interface CampoFormularioProps extends TextInputProps {
  dica?: string;
}

/** Campo textual com label, dica e mensagem de erro associados pelo Mantine. */
export function CampoFormulario({ dica, description, error, ...props }: CampoFormularioProps) {
  return <TextInput {...props} description={description ?? dica} error={error} />;
}
