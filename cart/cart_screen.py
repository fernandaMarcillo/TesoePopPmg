from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

from utils.cart import carrito


BG = (1, 0.92, 0.95, 1)
PINK = (1, 0.45, 0.75, 1)
TEXT = (0, 0, 0, 1)


class CartScreen(BoxLayout):

    def __init__(self, change_screen, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.change_screen = change_screen

        # fondo
        with self.canvas.before:
            Color(*BG)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_bg, pos=self._update_bg)

        # título
        self.add_widget(Label(
            text="🛒 CARRITO",
            size_hint_y=None,
            height=60,
            font_size=26,
            color=TEXT
        ))

        # scroll
        self.scroll = ScrollView()
        self.cont = GridLayout(cols=1, size_hint_y=None, spacing=12, padding=12)
        self.cont.bind(minimum_height=self.cont.setter("height"))
        self.scroll.add_widget(self.cont)
        self.add_widget(self.scroll)

        # total
        self.total_label = Label(
            text="Total: 0.00",
            size_hint_y=None,
            height=60,
            font_size=20,
            color=TEXT
        )
        self.add_widget(self.total_label)

        # volver
        back = Button(
            text="VOLVER A TIENDA",
            size_hint_y=None,
            height=50,
            background_color=PINK
        )
        back.bind(on_press=lambda x: self.change_screen("product"))
        self.add_widget(back)

        self.update()

    def _update_bg(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update(self):

        self.cont.clear_widgets()

        if not carrito:
            self.cont.add_widget(Label(text="Carrito vacío", color=TEXT))
            self.total_label.text = "Total: 0.00"
            return

        total = 0

        for item in carrito:

            subtotal = item["precio"] * item["cantidad"]
            total += subtotal

            row = BoxLayout(
                size_hint_y=None,
                height=60,
                spacing=10,
                padding=5
            )

            name = Label(text=item["nombre"], color=TEXT, size_hint_x=0.35)

            minus = Button(text="-", size_hint_x=0.1, background_color=PINK)
            qty = Label(text=str(item["cantidad"]), size_hint_x=0.1, color=TEXT)
            plus = Button(text="+", size_hint_x=0.1, background_color=PINK)
            subtotal_lbl = Label(text=f"{subtotal:.2f}", size_hint_x=0.25, color=TEXT)
            delete = Button(text="X", size_hint_x=0.1, background_color=PINK)

            minus.bind(on_press=lambda x, i=item: self.decrease(i))
            plus.bind(on_press=lambda x, i=item: self.increase(i))
            delete.bind(on_press=lambda x, i=item: self.remove(i))

            row.add_widget(name)
            row.add_widget(minus)
            row.add_widget(qty)
            row.add_widget(plus)
            row.add_widget(subtotal_lbl)
            row.add_widget(delete)

            self.cont.add_widget(row)

        self.total_label.text = f"Total: {total:.2f}"

    def increase(self, item):
        item["cantidad"] += 1
        self.update()

    def decrease(self, item):
        item["cantidad"] -= 1
        if item["cantidad"] <= 0:
            carrito.remove(item)
        self.update()

    def remove(self, item):
        carrito.remove(item)
        self.update()