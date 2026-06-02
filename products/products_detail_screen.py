# products/product_detail_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle

import colors
from cart.cart_screen import CARRITO_TEMPORAL

class ProductDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.producto = None

        with self.canvas.before:
            Color(rgba=colors.COLOR_ROSADO_FONDO)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=[25, 30, 25, 20], spacing=12)
        self.add_widget(self.layout)

    def set_producto(self, producto_data):
        self.producto = producto_data
        self.layout.clear_widgets()

        # Imagen superior impecable
        self.layout.add_widget(AsyncImage(source=self.producto["imagen"], size_hint_y=0.45, allow_stretch=True, keep_ratio=False))
        
        # Textos informativos ordenados con Emojis estructurados
        self.layout.add_widget(Label(text=f"🍰 {self.producto['nombre']}", font_size='24sp', bold=True, color=colors.COLOR_CAFE, size_hint_y=None, height=35))
        self.layout.add_widget(Label(text=f"Categoría: {self.producto['categoria']}", font_size='13sp', color=(0.5, 0.3, 0.3, 1), size_hint_y=None, height=18))
        
        lbl_desc = Label(text=self.producto["descripcion"], font_size='14sp', color=colors.COLOR_CAFE, halign='center')
        lbl_desc.bind(size=lambda idx, val: setattr(lbl_desc, 'text_size', (val[0], None)))
        self.layout.add_widget(lbl_desc)

        self.layout.add_widget(Label(text=f"Precio: ${self.producto['precio']:.2f}", font_size='22sp', bold=True, color=colors.COLOR_CAFE, size_hint_y=None, height=35))
        self.layout.add_widget(Label(size_hint_y=1))

        # --- BOTÓN DE ACCIÓN COMPRA ---
        btn_add = Button(text="AÑADIR AL CARRITO 🛒", background_normal='', background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE, bold=True, size_hint_y=None, height=48)
        btn_add.bind(on_press=self.agregar_al_carrito)
        self.layout.add_widget(btn_add)

        # Retornar de forma limpia
        btn_regresar = Button(text="◀ Volver al Catálogo", background_color=(0,0,0,0), color=colors.COLOR_CAFE, bold=True, size_hint_y=None, height=35)
        btn_regresar.bind(on_press=self.regresar)
        self.layout.add_widget(btn_regresar)

    def agregar_al_carrito(self, instance):
        if self.producto:
            prod_id = self.producto["id"]
            if prod_id in CARRITO_TEMPORAL:
                CARRITO_TEMPORAL[prod_id]["cantidad"] += 1
            else:
                CARRITO_TEMPORAL[prod_id] = {"datos": self.producto, "cantidad": 1}
            self.manager.current = 'cart'

    def regresar(self, instance):
        self.manager.current = 'products'

    def _update_rect(self, instance, value): self.rect.pos = instance.pos; self.rect.size = instance.size