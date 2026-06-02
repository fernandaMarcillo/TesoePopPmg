# main.py
import ssl

# DESACTIVAR VERIFICACIÓN SSL PARA CARGAR IMÁGENES POR URL SIN ERRORES
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# --- CONTINUACIÓN NORMAL DE TU APP ---
from kivy.app import App
from screen_manager import AppScreenManager

class TesoePopApp(App):
    def build(self):
        # Inicializa y retorna el ScreenManager personalizado
        return AppScreenManager()

if __name__ == '__main__':
    TesoePopApp().run()