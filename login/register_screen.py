# login/register_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

import colors
from login.session_data import USUARIOS_REGISTRADOS

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(rgba=colors.COLOR_ROSADO_FONDO)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=[35, 40, 35, 25], spacing=10)
        
        # --- ENCABEZADO CON ÍCONO ---
        layout.add_widget(Label(text="✨ Crear Cuenta ✨", font_size='26sp', bold=True, color=colors.COLOR_CAFE, size_hint_y=None, height=40))
        layout.add_widget(Label(text="Únete a la experiencia Tesoe Pop", font_size='14sp', color=colors.COLOR_CAFE, size_hint_y=None, height=20))
        
        self.lbl_mensaje = Label(text="", font_size='13sp', color=(0.2, 0.6, 0.2, 1), bold=True, size_hint_y=None, height=20)
        layout.add_widget(self.lbl_mensaje)

        # --- CAMPOS FORMULARIOS ---
        layout.add_widget(Label(text="👤 Nombre Completo", font_size='13sp', bold=True, color=colors.COLOR_CAFE, size_hint_y=None, height=18, halign='left'))
        self.txt_nombre = TextInput(hint_text="Tu nombre", multiline=False, size_hint_y=None, height=40, background_normal='', background_color=colors.COLOR_BLANCO, foreground_color=colors.COLOR_CAFE, padding=[10, 10, 10, 10])
        layout.add_widget(self.txt_nombre)

        layout.add_widget(Label(text="📧 Correo Electrónico", font_size='13sp', bold=True, color=colors.COLOR_CAFE, size_hint_y=None, height=18, halign='left'))
        self.txt_email = TextInput(hint_text="correo@ejemplo.com", multiline=False, size_hint_y=None, height=40, background_normal='', background_color=colors.COLOR_BLANCO, foreground_color=colors.COLOR_CAFE, padding=[10, 10, 10, 10])
        layout.add_widget(self.txt_email)

        layout.add_widget(Label(text="🔒 Contraseña Segura", font_size='13sp', bold=True, color=colors.COLOR_CAFE, size_hint_y=None, height=18, halign='left'))
        self.txt_pass = TextInput(hint_text="Crea tu contraseña", password=True, multiline=False, size_hint_y=None, height=40, background_normal='', background_color=colors.COLOR_BLANCO, foreground_color=colors.COLOR_CAFE, padding=[10, 10, 10, 10])
        layout.add_widget(self.txt_pass)

        layout.add_widget(Label(size_hint_y=None, height=10))

        # --- BOTÓN DE REGISTRO ---
        btn_registrar = Button(text="REGISTRARME 🚀", background_normal='', background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE, bold=True, size_hint_y=None, height=46)
        btn_registrar.bind(on_press=self.registrar_usuario_logica)
        layout.add_widget(btn_registrar)

        # Volver
        btn_volver = Button(text="◀ Volver al Inicio de Sesión", background_color=(0,0,0,0), color=colors.COLOR_CAFE, font_size='13sp', size_hint_y=None, height=35)
        btn_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        layout.add_widget(btn_volver)

        layout.add_widget(Label(size_hint_y=1))
        self.add_widget(layout)

    def registrar_usuario_logica(self, instance):
        nombre = self.txt_nombre.text.strip()
        email = self.txt_email.text.strip().lower()
        clave = self.txt_pass.text.strip()

        if not nombre or not email or not clave:
            self.lbl_mensaje.color = (0.9, 0.2, 0.2, 1)
            self.lbl_mensaje.text = "⚠️ Por favor, rellena todos los campos."
            return

        if email in USUARIOS_REGISTRADOS:
            self.lbl_mensaje.color = (0.9, 0.2, 0.2, 1)
            self.lbl_mensaje.text = "⚠️ Este correo ya está en uso."
            return

        # Guardar en la base de datos simulada
        USUARIOS_REGISTRADOS[email] = {
            "nombre": nombre,
            "pass": clave,
            "rol": "cliente"
        }
        
        self.lbl_mensaje.color = (0.2, 0.6, 0.2, 1)
        self.lbl_mensaje.text = "🎉 ¡Registro exitoso! Ya puedes iniciar sesión."
        self.txt_nombre.text = ""; self.txt_email.text = ""; self.txt_pass.text = ""

    def _update_rect(self, instance, value): self.rect.pos = instance.pos; self.rect.size = instance.size