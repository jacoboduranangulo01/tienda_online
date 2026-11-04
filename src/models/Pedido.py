"""Modelo de pedidos de la tienda online."""

import uuid
from datetime import datetime
from typing import List, Tuple

from models.Producto import Producto
from models.Usuario import Cliente


class Pedido:
    """Representa un pedido realizado por un cliente."""

    def __init__(
        self, cliente: Cliente, lineas: List[Tuple[Producto, int]]
    ) -> None:
        """Inicializa un pedido.

        Args:
            cliente: Cliente que realiza el pedido.
            lineas: Lista de tuplas (producto, cantidad) que componen
                el pedido.
        """
        self.id: str = str(uuid.uuid4())
        self.cliente: Cliente = cliente
        self.lineas: List[Tuple[Producto, int]] = lineas
        self.fecha: datetime = datetime.now()

    def calcular_total(self) -> float:
        """Calcula el importe total del pedido.

        Returns:
            Suma de precio x cantidad de todas las líneas del pedido.
        """
        return sum(producto.precio * cantidad for producto, cantidad in self.lineas)

    def __str__(self) -> str:
        """Devuelve un resumen legible del pedido."""
        detalle = ", ".join(
            f"{cantidad}x {producto.nombre}" for producto, cantidad in self.lineas
        )
        return (
            f"Pedido [{self.id}] de {self.cliente.nombre} "
            f"({self.fecha:%Y-%m-%d %H:%M}) - {detalle} "
            f"- Total: {self.calcular_total():.2f}€"
        )
