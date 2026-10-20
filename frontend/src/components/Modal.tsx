import { Modal as MantineModal, type ModalProps as MantineModalProps } from "@mantine/core";

interface ModalProps extends Omit<MantineModalProps, "title"> {
  titulo: string;
}

export function Modal({ titulo, children, ...props }: ModalProps) {
  return (
    <MantineModal {...props} title={titulo} centered closeButtonProps={{ "aria-label": "Fechar modal" }}>
      {children}
    </MantineModal>
  );
}
