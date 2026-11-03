"""Cliente independiente de la API: solo se comunica mediante HTTP con requests."""
import os
import requests

BASE_URL = os.getenv("TIENDA_API_URL", "http://127.0.0.1:8000")


def mostrar_respuesta(titulo, respuesta):
    print(f"\n--- {titulo} | HTTP {respuesta.status_code} ---")
    try:
        print(respuesta.json())
    except ValueError:
        print(respuesta.text)
    respuesta.raise_for_status()
    try:
        return respuesta.json()
    except ValueError:
        return None


def main():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})

    # 1. Crear usuario cliente.
    usuario = mostrar_respuesta(
        "Crear usuario",
        session.post(
            f"{BASE_URL}/usuarios",
            json={
                "nombre": "Cliente de prueba",
                "email": "cliente.prueba@example.com",
                "tipo": "cliente",
                "direccion": "Calle de prueba 10",
            },
            timeout=10,
        ),
    )

    # 2. Consultar usuarios.
    mostrar_respuesta("Lista de usuarios", session.get(f"{BASE_URL}/usuarios", timeout=10))

    # 3. Crear producto electrónico.
    producto = mostrar_respuesta(
        "Crear producto",
        session.post(
            f"{BASE_URL}/productos",
            json={
                "tipo": "electronico",
                "nombre": "Auriculares de prueba",
                "precio": 29.99,
                "stock": 10,
                "meses_garantia": 24,
            },
            timeout=10,
        ),
    )

    # 4. Consultar productos.
    mostrar_respuesta("Lista de productos", session.get(f"{BASE_URL}/productos", timeout=10))

    # 5. Crear pedido con el usuario y producto recién creados.
    pedido = mostrar_respuesta(
        "Crear pedido",
        session.post(
            f"{BASE_URL}/pedidos",
            json={
                "cliente_id": usuario["id"],
                "items": [{"producto_id": producto["id"], "cantidad": 1}],
            },
            timeout=10,
        ),
    )

    # 6. Consultar historial de pedidos del usuario.
    mostrar_respuesta(
        "Historial de pedidos",
        session.get(f"{BASE_URL}/usuarios/{usuario['id']}/pedidos", timeout=10),
    )
    print("\nCliente finalizado correctamente.")


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as error:
        print(f"Error de comunicación con la API: {error}")
        print(f"Comprueba que el servidor está activo en {BASE_URL}.")
