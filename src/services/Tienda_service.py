"""Capa de servicios que centraliza las operaciones de la tienda."""

from typing import Dict, List, Tuple

from models.Pedido import Pedido
from models.Producto import Producto
from models.Usuario import Administrador, Cliente, Usuario


class TiendaService:
    """Intermediario entre los usuarios, el inventario y los pedidos."""

    def __init__(self) -> None:
        """Inicializa los almacenes en memoria de usuarios, productos y pedidos."""
        self.usuarios: Dict[str, Usuario] = {}
        self.productos: Dict[str, Producto] = {}
        self.pedidos: List[Pedido] = []

    def registrar_usuario(self, tipo: str, **kwargs) -> Usuario:
        """Registra un nuevo usuario en la tienda.

        Args:
            tipo: Tipo de usuario a crear: "cliente" o "administrador".
            **kwargs: Atributos del usuario. Para "cliente" se esperan
                nombre, email y direccion. Para "administrador" se
                esperan nombre y email.

        Returns:
            El usuario creado y registrado.

        Raises:
            ValueError: Si el tipo de usuario no es reconocido.
        """
        if tipo.lower() == "cliente":
            usuario: Usuario = Cliente(
                nombre=kwargs["nombre"],
                email=kwargs["email"],
                direccion=kwargs["direccion"],
            )
        elif tipo.lower() == "administrador":
            usuario = Administrador(nombre=kwargs["nombre"], email=kwargs["email"])
        else:
            raise ValueError(f"Tipo de usuario no reconocido: {tipo}")

        self.usuarios[usuario.id] = usuario
        return usuario

    def anadir_producto(self, producto: Producto) -> None:
        """Añade un producto al inventario de la tienda.

        Args:
            producto: Instancia de Producto (o subclase) a añadir.
        """
        self.productos[producto.id] = producto

    def eliminar_producto(self, producto_id: str) -> bool:
        """Elimina un producto del inventario a partir de su identificador.

        Args:
            producto_id: Identificador del producto a eliminar.

        Returns:
            True si el producto existía y se eliminó, False en caso contrario.
        """
        if producto_id in self.productos:
            del self.productos[producto_id]
            return True
        return False

    def listar_productos(self) -> List[Producto]:
        """Lista todos los productos disponibles en la tienda.

        Returns:
            Lista de productos actualmente en inventario.
        """
        return list(self.productos.values())

    def realizar_pedido(
        self, usuario_id: str, lineas: List[Tuple[str, int]]
    ) -> Pedido:
        """Realiza un pedido para un usuario, si existe y hay stock suficiente.

        Args:
            usuario_id: Identificador del usuario (debe ser un Cliente).
            lineas: Lista de tuplas (producto_id, cantidad) solicitadas.

        Returns:
            El pedido generado, ya registrado en el histórico.

        Raises:
            ValueError: Si el usuario no existe, no es un cliente, algún
                producto no existe o no hay stock suficiente.
        """
        usuario = self.usuarios.get(usuario_id)
        if usuario is None:
            raise ValueError(f"El usuario '{usuario_id}' no existe.")
        if not isinstance(usuario, Cliente):
            raise ValueError("Solo los clientes pueden realizar pedidos.")

        lineas_pedido: List[Tuple[Producto, int]] = []
        for producto_id, cantidad in lineas:
            producto = self.productos.get(producto_id)
            if producto is None:
                raise ValueError(f"El producto '{producto_id}' no existe.")
            if not producto.hay_stock(cantidad):
                raise ValueError(
                    f"Stock insuficiente para '{producto.nombre}': "
                    f"disponible {producto.stock}, solicitado {cantidad}."
                )
            lineas_pedido.append((producto, cantidad))

        # Todo verificado: se descuenta el stock y se genera el pedido.
        for producto, cantidad in lineas_pedido:
            producto.actualizar_stock(-cantidad)

        pedido = Pedido(cliente=usuario, lineas=lineas_pedido)
        self.pedidos.append(pedido)
        return pedido

    def listar_pedidos_usuario(self, usuario_id: str) -> List[Pedido]:
        """Lista los pedidos de un usuario ordenados por fecha.

        Args:
            usuario_id: Identificador del usuario (cliente).

        Returns:
            Lista de pedidos del usuario, ordenados de más antiguo a más
            reciente.
        """
        pedidos_usuario = [
            pedido for pedido in self.pedidos if pedido.cliente.id == usuario_id
        ]
        return sorted(pedidos_usuario, key=lambda pedido: pedido.fecha)
