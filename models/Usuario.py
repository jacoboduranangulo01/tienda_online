"""Modelo de usuarios de la tienda online."""

import uuid


class Usuario:
    """Clase base que representa a cualquier usuario de la tienda."""

    def __init__(self, nombre: str, email: str) -> None:
        """Inicializa un usuario con identificador único autogenerado.

        Args:
            nombre: Nombre del usuario.
            email: Correo electrónico del usuario.
        """
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.email: str = email

    def is_admin(self) -> bool:
        """Indica si el usuario tiene privilegios de administrador.

        Returns:
            False por defecto para cualquier usuario base.
        """
        return False

    def __str__(self) -> str:
        """Devuelve una descripción textual básica del usuario."""
        return f"[{self.id}] {self.nombre} ({self.email})"


class Cliente(Usuario):
    """Usuario de tipo cliente, con dirección postal adicional."""

    def __init__(self, nombre: str, email: str, direccion: str) -> None:
        """Inicializa un cliente.

        Args:
            nombre: Nombre del cliente.
            email: Correo electrónico del cliente.
            direccion: Dirección postal del cliente.
        """
        super().__init__(nombre, email)
        self.direccion: str = direccion

    def __str__(self) -> str:
        """Devuelve la descripción del cliente incluyendo su dirección."""
        return f"{super().__str__()} - Cliente - Dirección: {self.direccion}"


class Administrador(Usuario):
    """Usuario de tipo administrador, gestor de la tienda."""

    def is_admin(self) -> bool:
        """Indica que un administrador siempre tiene privilegios de admin.

        Returns:
            True.
        """
        return True

    def __str__(self) -> str:
        """Devuelve la descripción del administrador."""
        return f"{super().__str__()} - Administrador"
