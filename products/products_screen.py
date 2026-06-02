from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle

from utils.data import productos
from utils.cart import carrito


BG = (1, 0.94, 0.97, 1)
PINK = (1, 0.42, 0.72, 1)
TEXT = (0, 0, 0, 1)


class CartIcon(ButtonBehavior, AsyncImage):
    pass


class ProductScreen(BoxLayout):

    def __init__(self, change_screen, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.change_screen = change_screen
        self.filtro = "Todos"

        # fondo
        with self.canvas.before:
            Color(*BG)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_bg, pos=self._update_bg)

        # HEADER
        header = BoxLayout(size_hint_y=None, height=60, padding=10)

        title = Label(
            text="🍰 Tesoe Pop",
            color=TEXT,
            font_size=20
        )

        cart_icon = CartIcon(
            source="assets/cart.png",
            size_hint=(None, None),
            size=(45, 45)
        )

        cart_icon.bind(on_press=lambda x: self.change_screen("cart"))

        header.add_widget(title)
        header.add_widget(cart_icon)

        self.add_widget(header)

        # FILTRO
        self.spinner = Spinner(
            text="Categorías",
            values=("Todos", "Tortas", "Donas", "Brownies", "Cupcakes", "Galletas"),
            size_hint_y=None,
            height=45,
            background_color=PINK
        )

        self.spinner.bind(text=self.set_filter)
        self.add_widget(self.spinner)

        # SCROLL
        scroll = ScrollView()

        self.cont = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=15,
            padding=15
        )

        self.cont.bind(minimum_height=self.cont.setter("height"))

        scroll.add_widget(self.cont)
        self.add_widget(scroll)

        self.render()

    def _update_bg(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def set_filter(self, spinner, value):
        self.filtro = value
        self.render()

    def render(self):

        self.cont.clear_widgets()

        for p in productos:

            if self.filtro != "Todos" and p["categoria"] != self.filtro:
                continue

            card = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=140,
                spacing=10,
                padding=10
            )

            img = AsyncImage(
                source=p["imagen"],
                size_hint_x=0.3
            )

            info = BoxLayout(orientation="vertical", spacing=5)

            name = Label(text=p["nombre"], color=TEXT, font_size=18)
            price = Label(text=f"${p['precio']:.2f}", color=TEXT)

            btn = Button(
                text="Agregar 🛒",
                size_hint_y=None,
                height=40,
                background_color=PINK
            )

            btn.bind(on_press=lambda x, prod=p: self.add(prod))

            info.add_widget(name)
            info.add_widget(price)
            info.add_widget(btn)

            card.add_widget(img)
            card.add_widget(info)

            self.cont.add_widget(card)

    def add(self, producto):

        for item in carrito:
            if item["nombre"] == producto["nombre"]:
                item["cantidad"] += 1
                return

        carrito.append({
            "nombre": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": 1
        })