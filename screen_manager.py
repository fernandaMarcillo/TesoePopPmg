# screen_manager.py
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

# Importaciones de los módulos de todo el equipo
from login.login_screen import LoginScreen
from login.register_screen import RegisterScreen
from login.pofile_screen import ProfileScreen
from products.products_screen import ProductsScreen
from products.products_detail_screen import ProductDetailScreen
from cart.cart_screen import CartScreen
from admin.admin_screen import AdminScreen

# Forzar tamaño de pantalla tipo smartphone para cuidar el diseño UI/UX
Window.size = (360, 640)

class AppScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # El orden aquí dicta qué pantalla aparece primero al abrir la app
        self.add_widget(LoginScreen(name='login'))
        self.add_widget(RegisterScreen(name='register'))
        self.add_widget(ProfileScreen(name='profile'))
        self.add_widget(ProductsScreen(name='products'))
        self.add_widget(ProductDetailScreen(name='product_detail')) 
        self.add_widget(CartScreen(name='cart'))
        self.add_widget(AdminScreen(name='admin'))