# products/products_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, RoundedRectangle

import colors
from products.products_data import LISTA_PRODUCTOS

class ProductsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout Estructural Vertical Base
        self.main_layout = BoxLayout(orientation='vertical')
        self.add_widget(self.main_layout)

        # --- NAVBAR SUPERIOR UNIFICADA ---
        navbar = BoxLayout(orientation='horizontal', size_hint_y=None, height=56, padding=10, spacing=10)
        with navbar.canvas.before:
            Color(rgba=colors.COLOR_ROSADO_BOTON)
            self.nav_rect = RoundedRectangle(size=navbar.size, pos=navbar.pos)
        navbar.bind(size=self._update_nav, pos=self._update_nav)

        navbar.add_widget(Label(text="🍰 Tesoe Pop", bold=True, color=colors.COLOR_CAFE, font_size='18sp', size_hint_x=0.4))
        
        btn_carrito = Button(text="Carrito 🛒", background_color=(0,0,0,0), color=colors.COLOR_CAFE, bold=True)
        btn_carrito.bind(on_press=lambda x: setattr(self.manager, 'current', 'cart'))
        navbar.add_widget(btn_carrito)
        
        btn_perfil = Button(text="Perfil 👤", background_color=(0,0,0,0), color=colors.COLOR_CAFE, bold=True)
        btn_perfil.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        navbar.add_widget(btn_perfil)
        
        self.main_layout.add_widget(navbar)

        # Fondo general de la sección del catálogo
        self.catalogo_box = BoxLayout(orientation='vertical', padding=12, spacing=10)
        with self.catalogo_box.canvas.before:
            Color(rgba=colors.COLOR_ROSADO_FONDO)
            self.bg_rect = RoundedRectangle(size=self.catalogo_box.size, pos=self.catalogo_box.pos)
        self.catalogo_box.bind(size=self._update_bg, pos=self._update_bg)
        
        self.catalogo_box.add_widget(Label(text="Nuestro Catálogo Artesanal", font_size='20sp', bold=True, color=colors.COLOR_CAFE, size_hint_y=None, height=30))

        # --- LISTA DESPLOZABLE DE TARJETAS (UI/UX) ---
        scroll = ScrollView()
        self.container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=12, padding=[2, 5, 2, 5])
        self.container.bind(minimum_height=self.container.setter('height'))

        self.cargar_productos_en_interfaz()
        
        scroll.add_widget(self.container)
        self.catalogo_box.add_widget(scroll)
        self.main_layout.add_widget(self.catalogo_box)

    def cargar_productos_en_interfaz(self):
        self.container.clear_widgets()
        
        for prod in LISTA_PRODUCTOS:
            # Tarjeta Beige Estilizada
            tarjeta = BoxLayout(orientation='horizontal', size_hint_y=None, height=105, padding=10, spacing=12)
            with tarjeta.canvas.before:
                Color(rgba=colors.COLOR_BEIGE)
                rect_t = RoundedRectangle(size=tarjeta.size, pos=tarjeta.pos, radius=[10])
            tarjeta.bind(size=lambda inst, val, r=rect_t: setattr(r, 'size', val), pos=lambda inst, val, r=rect_t: setattr(r, 'pos', val))

            # Imagen del postre con recortes limpios
            img = AsyncImage(source=prod["imagen"], size_hint_x=0.25, allow_stretch=True, keep_ratio=False)
            tarjeta.add_widget(img)

            # Información del Producto
            info = BoxLayout(orientation='vertical', spacing=2, size_hint_x=0.45)
            info.add_widget(Label(text=prod["nombre"], bold=True, color=colors.COLOR_CAFE, font_size='15sp', halign='left'))
            info.add_widget(Label(text=f"Precio: ${prod['precio']:.2f}", bold=True, color=colors.COLOR_CAFE, font_size='13sp'))
            tarjeta.add_widget(info)

            # Botón de Acción Directa
            btn_ver = Button(
                text="VER MAS 🍰", font_size='11sp', bold=True, background_normal='',
                background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE,
                size_hint_x=0.3, size_hint_y=None, height=38, pos_hint={'center_y': 0.5}
            )
            # Vinculación dinámica al gestor para mandar los datos a la pantalla detalle
            btn_ver.bind(on_press=lambda instance, p=prod: self.ir_al_detalle(p))
            tarjeta.add_widget(btn_ver)

            self.container.add_widget(tarjeta)

    def ir_al_detalle(self, producto):
        pantalla_detalle = self.manager.get_screen('product_detail')
        pantalla_detalle.set_producto(producto)
        self.manager.current = 'product_detail'

    def _update_nav(self, instance, value): self.nav_rect.pos = instance.pos; self.nav_rect.size = instance.size
    def _update_bg(self, instance, value): self.bg_rect.pos = instance.pos; self.bg_rect.size = instance.size