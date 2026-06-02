# login/login_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle

import colors
from login.session_data import USUARIOS_REGISTRADOS, USUARIO_ACTUAL

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fondo Rosado Pastel Oficial
        with self.canvas.before:
            Color(rgba=colors.COLOR_ROSADO_FONDO)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Contenedor principal con márgenes generosos para evitar esquinas saturadas
        layout = BoxLayout(orientation='vertical', padding=[40, 50, 40, 30], spacing=10)
        
        # --- ENCABEZADO UI/UX ---
        layout.add_widget(Label(text="Tesoe Pop", font_size='38sp', bold=True, color=colors.COLOR_CAFE, size_hint_y=None, height=55)) 
        layout.add_widget(Label(text="¡Bienvenido de vuelta!", font_size='16sp', color=colors.COLOR_CAFE, size_hint_y=None, height=25))
        layout.add_widget(Label(size_hint_y=None, height=20)) # Espacio en blanco arquitectónico

        # Mensaje de Alerta / Error Dinámico
        self.lbl_error = Label(text="", font_size='13sp', color=(0.8, 0.2, 0.2, 1), bold=True, size_hint_y=None, height=25)
        layout.add_widget(self.lbl_error)

        # --- FORMULARIO ADMINISTRATIVO / CLIENTE ---
        layout.add_widget(Label(text="Correo Electrónico", font_size='14sp', bold=True, color=colors.COLOR_CAFE, size_hint_y=None, height=20, halign='left'))
        
        self.email = TextInput(
            hint_text="ejemplo@correo.com", multiline=False, size_hint_y=None, height=44,
            background_normal='', background_color=colors.COLOR_BLANCO,
            foreground_color=colors.COLOR_CAFE, padding=[12, 12, 12, 12]
        )
        layout.add_widget(self.email)

        layout.add_widget(Label(text="Contraseña", font_size='14sp', bold=True, color=colors.COLOR_CAFE, size_hint_y=None, height=20, halign='left'))
        
        self.password = TextInput(
            hint_text="Introduce tu clave", password=True, multiline=False, size_hint_y=None, height=44,
            background_normal='', background_color=colors.COLOR_BLANCO,
            foreground_color=colors.COLOR_CAFE, padding=[12, 12, 12, 12]
        )
        layout.add_widget(self.password)

        layout.add_widget(Label(size_hint_y=None, height=15))

        # --- BOTÓN DE ACCIÓN PRINCIPAL ---
        btn_login = Button(
            text="INICIAR SESIÓN", background_normal='',
            background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE,
            bold=True, font_size='15sp', size_hint_y=None, height=48
        )
        btn_login.bind(on_press=self.autenticar)
        layout.add_widget(btn_login)

        # Botón Secundario Sutil
        btn_ir_registro = Button(
            text="¿No tienes cuenta? Regístrate aquí", background_color=(0, 0, 0, 0),
            color=colors.COLOR_CAFE, font_size='13sp', size_hint_y=None, height=35
        )
        btn_ir_registro.bind(on_press=lambda x: setattr(self.manager, 'current', 'register'))
        layout.add_widget(btn_ir_registro)

        # Cierre estético inferior
        layout.add_widget(Label(size_hint_y=1))
        layout.add_widget(Label(text="© 2026 Tesoe Pop - Pastelería Artesanal", font_size='11sp', color=colors.COLOR_CAFE, size_hint_y=None, height=20))
        
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def autenticar(self, instance):
        email_ingresado = self.email.text.strip().lower()
        pass_ingresado = self.password.text.strip()

        if email_ingresado in USUARIOS_REGISTRADOS:
            if USUARIOS_REGISTRADOS[email_ingresado]["pass"] == pass_ingresado:
                USUARIO_ACTUAL["email"] = email_ingresado
                USUARIO_ACTUAL["nombre"] = USUARIOS_REGISTRADOS[email_ingresado]["nombre"]
                USUARIO_ACTUAL["rol"] = USUARIOS_REGISTRADOS[email_ingresado]["rol"]
                self.lbl_error.text = "" 
                
                if USUARIO_ACTUAL["rol"] == "admin":
                    self.manager.current = 'admin'
                else:
                    self.manager.current = 'products'
            else:
                self.lbl_error.text = "Contraseña incorrecta."
        else:
            self.lbl_error.text = "El correo no está registrado."