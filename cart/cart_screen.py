# cart/cart_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, RoundedRectangle

import colors

CARRITO_TEMPORAL = {}

class CartScreen(Screen):
    def on_enter(self, *args):
        self.actualizar_interfaz_carrito()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical')
        self.add_widget(self.main_layout)

    def actualizar_interfaz_carrito(self):
        self.main_layout.clear_widgets()

        navbar = BoxLayout(orientation='horizontal', size_hint_y=None, height=56, padding=10, spacing=5)
        with navbar.canvas.before:
            Color(rgba=colors.COLOR_ROSADO_BOTON)
            self.nav_rect = RoundedRectangle(size=navbar.size, pos=navbar.pos)
        navbar.bind(size=self._update_nav, pos=self._update_nav)

        navbar.add_widget(Label(text="Tu Orden 🛒", bold=True, color=colors.COLOR_CAFE, font_size='16sp', size_hint_x=0.4))
        
        btn_catalogo = Button(text="Catálogo 🍰", background_color=(0,0,0,0), color=colors.COLOR_CAFE, bold=True)
        btn_catalogo.bind(on_press=lambda x: setattr(self.manager, 'current', 'products'))
        navbar.add_widget(btn_catalogo)
        
        btn_perfil = Button(text="Perfil 👤", background_color=(0,0,0,0), color=colors.COLOR_CAFE, bold=True)
        btn_perfil.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        navbar.add_widget(btn_perfil)
        self.main_layout.add_widget(navbar)

        if not CARRITO_TEMPORAL:
            empty_box = BoxLayout(orientation='vertical', padding=40, spacing=20)
            with empty_box.canvas.before:
                Color(rgba=colors.COLOR_ROSADO_FONDO)
                self.bg_rect = RoundedRectangle(size=empty_box.size, pos=empty_box.pos)
            empty_box.bind(size=self._update_bg, pos=self._update_bg)

            empty_box.add_widget(AsyncImage(source='https://cdn-icons-png.flaticon.com/512/11329/11329060.png', size_hint_y=None, height=120))
            empty_box.add_widget(Label(text="Tu carrito está vacío", font_size='20sp', bold=True, color=colors.COLOR_CAFE, halign='center'))
            empty_box.add_widget(Label(size_hint_y=1))
            self.main_layout.add_widget(empty_box)
            return

        scroll = ScrollView()
        container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=12)
        container.bind(minimum_height=container.setter('height'))

        total_acumulado = 0.0

        for prod_id, item_info in list(CARRITO_TEMPORAL.items()):
            producto = item_info["datos"]
            cantidad = item_info["cantidad"]
            subtotal_item = producto["precio"] * cantidad
            total_acumulado += subtotal_item

            tarjeta_item = BoxLayout(orientation='horizontal', size_hint_y=None, height=95, padding=8, spacing=10)
            with tarjeta_item.canvas.before:
                Color(rgba=colors.COLOR_BEIGE)
                rect = RoundedRectangle(size=tarjeta_item.size, pos=tarjeta_item.pos, radius=[8])
            tarjeta_item.bind(size=lambda inst, val, r=rect: setattr(r, 'size', val), pos=lambda inst, val, r=rect: setattr(r, 'pos', val))

            tarjeta_item.add_widget(AsyncImage(source=producto["imagen"], size_hint_x=0.2, allow_stretch=True, keep_ratio=False))

            detalles = BoxLayout(orientation='vertical', spacing=2, size_hint_x=0.45)
            detalles.add_widget(Label(text=producto['nombre'], bold=True, color=colors.COLOR_CAFE, font_size='14sp', halign='left'))
            detalles.add_widget(Label(text=f"Subtotal: ${subtotal_item:.2f}", bold=True, color=colors.COLOR_CAFE, font_size='13sp'))
            tarjeta_item.add_widget(detalles)

            panel_edicion = BoxLayout(orientation='vertical', spacing=5, size_hint_x=0.35)
            controles_num = BoxLayout(orientation='horizontal', spacing=2)
            
            btn_menos = Button(text="-", font_size='16sp', bold=True, background_normal='', background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE)
            btn_menos.bind(on_press=lambda instance, pid=prod_id: self.modificar_cantidad_logica(pid, -1))
            
            lbl_cantidad = Label(text=str(cantidad), bold=True, color=colors.COLOR_CAFE, font_size='14sp')
            
            btn_mas = Button(text="+", font_size='16sp', bold=True, background_normal='', background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE)
            btn_mas.bind(on_press=lambda instance, pid=prod_id: self.modificar_cantidad_logica(pid, 1))
            
            controles_num.add_widget(btn_menos)
            controles_num.add_widget(lbl_cantidad)
            controles_num.add_widget(btn_mas)
            panel_edicion.add_widget(controles_num)

            btn_eliminar_todo = Button(text="Quitar 🗑️", font_size='10sp', background_normal='', background_color=(0.9, 0.4, 0.4, 0.15), color=(0.8, 0.2, 0.2, 1), size_hint_y=None, height=24)
            btn_eliminar_todo.bind(on_press=lambda instance, pid=prod_id: self.eliminar_item_logica(pid))
            panel_edicion.add_widget(btn_eliminar_todo)

            tarjeta_item.add_widget(panel_edicion)
            container.add_widget(tarjeta_item)

        scroll.add_widget(container)
        self.main_layout.add_widget(scroll)

        resumen_panel = BoxLayout(orientation='vertical', size_hint_y=None, height=130, padding=15, spacing=10)
        with resumen_panel.canvas.before:
            Color(rgba=colors.COLOR_ROSADO_FONDO)
            self.res_rect = RoundedRectangle(size=resumen_panel.size, pos=resumen_panel.pos)
        resumen_panel.bind(size=self._update_res, pos=self._update_res)

        fila_total = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        fila_total.add_widget(Label(text="TOTAL COMPRA:", font_size='16sp', bold=True, color=colors.COLOR_CAFE))
        fila_total.add_widget(Label(text=f"${total_acumulado:.2f}", font_size='20sp', bold=True, color=colors.COLOR_CAFE, halign='right'))
        resumen_panel.add_widget(fila_total)

        btn_checkout = Button(text="PROCESAR PEDIDO ✅", background_normal='', background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE, bold=True, size_hint_y=None, height=48)
        btn_checkout.bind(on_press=self.ejecutar_checkout_exitoso)
        resumen_panel.add_widget(btn_checkout)
        self.main_layout.add_widget(resumen_panel)

    def modificar_cantidad_logica(self, prod_id, cambio):
        if prod_id in CARRITO_TEMPORAL:
            CARRITO_TEMPORAL[prod_id]["cantidad"] += cambio
            if CARRITO_TEMPORAL[prod_id]["cantidad"] <= 0:
                CARRITO_TEMPORAL.pop(prod_id)
            self.actualizar_interfaz_carrito()

    def eliminar_item_logica(self, prod_id):
        if prod_id in CARRITO_TEMPORAL:
            CARRITO_TEMPORAL.pop(prod_id)
        self.actualizar_interfaz_carrito()

    def ejecutar_checkout_exitoso(self, instance):
        CARRITO_TEMPORAL.clear()
        self.main_layout.clear_widgets()
        layout_exito = BoxLayout(orientation='vertical', padding=40, spacing=25)
        with layout_exito.canvas.before:
            Color(rgba=colors.COLOR_ROSADO_FONDO)
            self.ex_rect = RoundedRectangle(size=layout_exito.size, pos=layout_exito.pos)
        layout_exito.bind(size=self._update_ex, pos=self._update_ex)

        layout_exito.add_widget(AsyncImage(source='https://cdn-icons-png.flaticon.com/512/4436/4436481.png', size_hint_y=None, height=140))
        layout_exito.add_widget(Label(text="¡Pedido Recibido! 🎉", font_size='26sp', bold=True, color=colors.COLOR_CAFE, halign='center'))
        layout_exito.add_widget(Label(size_hint_y=1))

        btn_volver = Button(text="Volver a la Tienda", background_normal='', background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE, bold=True, size_hint_y=None, height=50)
        btn_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'products'))
        layout_exito.add_widget(btn_volver)
        self.main_layout.add_widget(layout_exito)

    def _update_nav(self, instance, value): self.nav_rect.pos = instance.pos; self.nav_rect.size = instance.size
    def _update_bg(self, instance, value): self.bg_rect.pos = instance.pos; self.bg_rect.size = instance.size
    def _update_res(self, instance, value): self.res_rect.pos = instance.pos; self.res_rect.size = instance.size
    def _update_ex(self, instance, value): self.ex_rect.pos = instance.pos; self.ex_rect.size = instance.size