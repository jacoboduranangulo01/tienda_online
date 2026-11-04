"""Modelo de productos de la tienda online."""

import uuid


class Producto:
    """Clase base que representa un producto genérico de la tienda."""

    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        """Inicializa un producto con identificador único autogenerado.

        Args:
            nombre: Nombre del producto.
            precio: Precio unitario del producto.
            stock: Cantidad disponible en inventario.
        """
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock

    def hay_stock(self, cantidad: int) -> bool:
        """Comprueba si hay stock suficiente para la cantidad solicitada.

        Args:
            cantidad: Cantidad que se desea comprobar.

        Returns:
            True si el stock disponible es suficiente, False en caso contrario.
        """
        return self.stock >= cantidad

    def actualizar_stock(self, cantidad: int) -> None:
        """Actualiza el stock del producto.

        Args:
            cantidad: Variación de stock. Negativa para una compra,
                positiva para una reposición.

        Raises:
            ValueError: Si la operación dejaría el stock por debajo de 0.
        """
        nuevo_stock = self.stock + cantidad
        if nuevo_stock < 0:
            raise ValueError(
                f"Stock insuficiente para '{self.nombre}': "
                f"stock actual {self.stock}, solicitado {abs(cantidad)}."
            )
        self.stock = nuevo_stock

    def __str__(self) -> str:
        """Devuelve una descripción textual básica del producto."""
        return (
            f"[{self.id}] {self.nombre} - {self.precio:.2f}€ "
            f"(stock: {self.stock})"
        )


class ProductoElectronico(Producto):
    """Producto electrónico, con meses de garantía adicionales."""

    def __init__(
        self, nombre: str, precio: float, stock: int, meses_garantia: int
    ) -> None:
        """Inicializa un producto electrónico.

        Args:
            nombre: Nombre del producto.
            precio: Precio unitario del producto.
            stock: Cantidad disponible en inventario.
            meses_garantia: Meses de garantía del producto.
        """
        super().__init__(nombre, precio, stock)
        self.meses_garantia: int = meses_garantia

    def __str__(self) -> str:
        """Devuelve la descripción del producto incluyendo la garantía."""
        return f"{super().__str__()} - Garantía: {self.meses_garantia} meses"


class ProductoRopa(Producto):
    """Producto de ropa, con talla y color adicionales."""

    def __init__(
        self, nombre: str, precio: float, stock: int, talla: str, color: str
    ) -> None:
        """Inicializa un producto de ropa.

        Args:
            nombre: Nombre del producto.
            precio: Precio unitario del producto.
            stock: Cantidad disponible en inventario.
            talla: Talla del producto (p. ej. "M", "42").
            color: Color del producto.
        """
        super().__init__(nombre, precio, stock)
        self.talla: str = talla
        self.color: str = color

    def __str__(self) -> str:
        """Devuelve la descripción del producto incluyendo talla y color."""
        return f"{super().__str__()} - Talla: {self.talla}, Color: {self.color}"
