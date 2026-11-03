from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from models.Producto import Producto, ProductoElectronico, ProductoRopa
from models.Usuario import Cliente
from services.Tienda_service import TiendaService
from schemas import (
    UsuarioCreate, UsuarioRead, ProductoCreate, ProductoRead,
    PedidoCreate, PedidoRead, PedidoItemRead,
)

app = FastAPI(
    title="Tienda online - Práctica 2",
    description="API REST para gestionar usuarios, productos y pedidos.",
    version="1.0.0",
)

# Permite que el frontend web realice peticiones a la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adecuado para esta práctica local; restringir en producción.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

tienda = TiendaService()


def usuario_a_schema(usuario) -> UsuarioRead:
    return UsuarioRead(
        id=usuario.id, nombre=usuario.nombre, email=usuario.email,
        es_admin=usuario.is_admin()
    )


def producto_a_schema(producto) -> ProductoRead:
    tipo = (
        "electronico" if isinstance(producto, ProductoElectronico)
        else "ropa" if isinstance(producto, ProductoRopa)
        else "generico"
    )
    return ProductoRead(
        id=producto.id, tipo=tipo, nombre=producto.nombre,
        precio=producto.precio, stock=producto.stock,
        meses_garantia=getattr(producto, "meses_garantia", None),
        talla=getattr(producto, "talla", None),
        color=getattr(producto, "color", None),
    )


def pedido_a_schema(pedido) -> PedidoRead:
    items = [
        PedidoItemRead(
            producto_id=producto.id,
            nombre=producto.nombre,
            cantidad=cantidad,
            precio_unitario=producto.precio,
            subtotal=round(producto.precio * cantidad, 2),
        )
        for producto, cantidad in pedido.lineas
    ]
    return PedidoRead(
        id=pedido.id,
        fecha=pedido.fecha.isoformat(),
        cliente_id=pedido.cliente.id,
        cliente_nombre=pedido.cliente.nombre,
        total=round(pedido.calcular_total(), 2),
        items=items,
    )


@app.get("/")
def inicio():
    return {"mensaje": "API de la tienda online", "documentacion": "/docs"}


# USUARIOS
@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: UsuarioCreate):
    if datos.tipo == "cliente":
        if not datos.direccion:
            raise HTTPException(status_code=422, detail="La dirección es obligatoria para un cliente.")
        usuario = tienda.registrar_usuario(
            "cliente", nombre=datos.nombre, email=str(datos.email),
            direccion=datos.direccion
        )
    else:
        usuario = tienda.registrar_usuario(
            "administrador", nombre=datos.nombre, email=str(datos.email)
        )
    return usuario_a_schema(usuario)


@app.get("/usuarios", response_model=list[UsuarioRead])
def listar_usuarios():
    return [usuario_a_schema(usuario) for usuario in tienda.usuarios.values()]


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: str):
    usuario = tienda.usuarios.get(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return usuario_a_schema(usuario)


# PRODUCTOS
@app.post("/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCreate):
    if datos.tipo == "electronico":
        if datos.meses_garantia is None:
            raise HTTPException(status_code=422, detail="meses_garantia es obligatorio para productos electrónicos.")
        producto = ProductoElectronico(
            datos.nombre, datos.precio, datos.stock, datos.meses_garantia
        )
    elif datos.tipo == "ropa":
        if not datos.talla or not datos.color:
            raise HTTPException(status_code=422, detail="talla y color son obligatorios para ropa.")
        producto = ProductoRopa(
            datos.nombre, datos.precio, datos.stock, datos.talla, datos.color
        )
    else:
        producto = Producto(datos.nombre, datos.precio, datos.stock)
    tienda.anadir_producto(producto)
    return producto_a_schema(producto)


@app.get("/productos", response_model=list[ProductoRead])
def listar_productos():
    return [producto_a_schema(producto) for producto in tienda.listar_productos()]


@app.get("/productos/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: str):
    producto = tienda.productos.get(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return producto_a_schema(producto)


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: str):
    if not tienda.eliminar_producto(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return None


# PEDIDOS
@app.post("/pedidos", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def crear_pedido(datos: PedidoCreate):
    cliente = tienda.usuarios.get(datos.cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    if not isinstance(cliente, Cliente):
        raise HTTPException(status_code=400, detail="El usuario indicado no es un cliente.")
    lineas = [(item.producto_id, item.cantidad) for item in datos.items]
    try:
        pedido = tienda.realizar_pedido(datos.cliente_id, lineas)
    except ValueError as error:
        mensaje = str(error)
        codigo = 404 if "no existe" in mensaje else 400
        raise HTTPException(status_code=codigo, detail=mensaje)
    return pedido_a_schema(pedido)


@app.get("/usuarios/{cliente_id}/pedidos", response_model=list[PedidoRead])
def listar_pedidos_cliente(cliente_id: str):
    cliente = tienda.usuarios.get(cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if not isinstance(cliente, Cliente):
        raise HTTPException(status_code=400, detail="El usuario indicado no es un cliente.")
    return [pedido_a_schema(pedido) for pedido in tienda.listar_pedidos_usuario(cliente_id)]
