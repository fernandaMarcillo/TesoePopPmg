# login/session_data.py

# Diccionario para controlar quién inició sesión en tiempo real
USUARIO_ACTUAL = {
    "nombre": "",
    "email": "",
    "rol": ""
}

# Base de datos simulada en formato Diccionario para acceso indexado rápido
USUARIOS_REGISTRADOS = {
    "user@gmail.com": {
        "nombre": "Fernanda Marcillo",
        "pass": "12345",
        "rol": "cliente"
    },
    "admin@gmail.com": {
        "nombre": "Administrador Principal",
        "pass": "admin123",
        "rol": "admin"
    }
}