from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field


class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=1)
    email: EmailStr
    tipo: Literal["cliente", "administrador"]
    direccion: Optional[str] = None


class UsuarioRead(BaseModel):
    id: str
    nombre: str
    email: EmailStr
    es_admin: bool


class ProductoCreate(BaseModel):
    tipo: Literal["generico", "electronico", "ropa"]
    nombre: str = Field(min_length=1)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    meses_garantia: Optional[int] = Field(default=None, ge=0)
    talla: Optional[str] = None
    color: Optional[str] = None


class ProductoRead(BaseModel):
    id: str
    tipo: str
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None


class PedidoItemCreate(BaseModel):
    producto_id: str
    cantidad: int = Field(gt=0)


class PedidoCreate(BaseModel):
    cliente_id: str
    items: list[PedidoItemCreate] = Field(min_length=1)


class PedidoItemRead(BaseModel):
    producto_id: str
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float


class PedidoRead(BaseModel):
    id: str
    fecha: str
    cliente_id: str
    cliente_nombre: str
    total: float
    items: list[PedidoItemRead]
