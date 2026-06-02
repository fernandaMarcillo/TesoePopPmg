# login/profile_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, RoundedRectangle

import colors
from login.session_data import USUARIO_ACTUAL

class ProfileScreen(Screen):
    def on_enter(self, *args):
        """Carga dinámicamente los íconos y datos del usuario activo al entrar"""
        self.lbl_user_name.text = f"👤 {USUARIO_ACTUAL['nombre'] or 'Usuario Cliente'}"
        self.lbl_user_email.text = f"📧 {USUARIO_ACTUAL['email'] or 'sin_correo@email.com'}"
        self.lbl_user_role.text = f"🛡️ Rango Cuenta: {USUARIO_ACTUAL['rol'].upper()}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical')
        self.add_widget(main_layout)

        # --- NAVBAR SUPERIOR ---
        navbar = BoxLayout(orientation='horizontal', size_hint_y=None, height=54, padding=10)
        with navbar.canvas.before:
            Color(rgba=colors.COLOR_ROSADO_BOTON)
            self.nav_rect = RoundedRectangle(size=navbar.size, pos=navbar.pos)
        navbar.bind(size=self._update_nav, pos=self._update_nav)

        navbar.add_widget(Label(text="Mi Perfil Digital 👤", bold=True, color=colors.COLOR_CAFE, font_size='16sp'))
        
        btn_volver = Button(text="Volver 🍰", background_color=(0,0,0,0), color=colors.COLOR_CAFE, bold=True, size_hint_x=0.25)
        btn_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'products'))
        navbar.add_widget(btn_volver)
        main_layout.add_widget(navbar)

        # --- CONTENIDO DE CONFIGURACIÓN ---
        content = BoxLayout(orientation='vertical', padding=30, spacing=15)
        with content.canvas.before:
            Color(rgba=colors.COLOR_ROSADO_FONDO)
            self.bg_rect = RoundedRectangle(size=content.size, pos=content.pos)
        content.bind(size=self._update_bg, pos=self._update_bg)

        # Avatar Ilustrativo
        content.add_widget(AsyncImage(source='https://cdn-icons-png.flaticon.com/512/6997/6997662.png', size_hint_y=None, height=120))
        content.add_widget(Label(size_hint_y=None, height=10))

        # Tarjeta de Datos Estilizada (Beige)
        tarjeta_datos = BoxLayout(orientation='vertical', padding=15, spacing=8, size_hint_y=None, height=130)
        with tarjeta_datos.canvas.before:
            Color(rgba=colors.COLOR_BEIGE)
            rect = RoundedRectangle(size=tarjeta_datos.size, pos=tarjeta_datos.pos, radius=[8])
        tarjeta_datos.bind(size=lambda inst, val, r=rect: setattr(r, 'size', val), pos=lambda inst, val, r=rect: setattr(r, 'pos', val))

        self.lbl_user_name = Label(text="", bold=True, color=colors.COLOR_CAFE, font_size='16sp', halign='left')
        self.lbl_user_email = Label(text="", color=colors.COLOR_CAFE, font_size='14sp', halign='left')
        self.lbl_user_role = Label(text="", font_size='12sp', bold=True, color=(0.5, 0.4, 0.4, 1), halign='left')
        
        tarjeta_datos.add_widget(self.lbl_user_name)
        tarjeta_datos.add_widget(self.lbl_user_email)
        tarjeta_datos.add_widget(self.lbl_user_role)
        content.add_widget(tarjeta_datos)

        content.add_widget(Label(size_hint_y=1))

        # Botón de Cerrar Sesión Seguro
        btn_logout = Button(text="CERRAR SESIÓN 🚪", background_normal='', background_color=(0.9, 0.4, 0.4, 0.2), color=(0.8, 0.2, 0.2, 1), bold=True, size_hint_y=None, height=46)
        btn_logout.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        content.add_widget(btn_logout)

        main_layout.add_widget(content)

    def _update_nav(self, instance, value): self.nav_rect.pos = instance.pos; self.nav_rect.size = instance.size
    def _update_bg(self, instance, value): self.bg_rect.pos = instance.pos; self.bg_rect.size = instance.size