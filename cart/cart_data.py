carrito = []

def agregar(producto):
    carrito.append(producto)

def total():

    suma = 0

    for producto in carrito:
        suma += producto["precio"]

    return suma