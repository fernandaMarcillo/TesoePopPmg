from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from login.login_screen import LoginScreen
from login.register_screen import RegisterScreen
from products.products_screen import ProductScreen
from cart.cart_screen import CartScreen


class MainApp(App):

    def build(self):

        self.sm = ScreenManager()

        # LOGIN
        self.sm.add_widget(LoginScreen(name="login"))

        # REGISTER (YA EXISTE EN TU PROYECTO)
        self.sm.add_widget(RegisterScreen(name="register"))

        # PRODUCTS
        products = Screen(name="products")
        self.products_widget = ProductScreen(self.change)
        products.add_widget(self.products_widget)
        self.sm.add_widget(products)

        # CART
        cart = Screen(name="cart")
        self.cart_widget = CartScreen(self.change)
        cart.add_widget(self.cart_widget)
        self.sm.add_widget(cart)

        # INICIO
        self.sm.current = "login"

        return self.sm

    def change(self, name):
        self.sm.current = name

        if name == "cart":
            self.cart_widget.update()


MainApp().run()