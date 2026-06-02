# admin/admin_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

import colors
from admin.admin_data import HISTORIAL_PEDIDOS
from products.products_data import LISTA_PRODUCTOS

class AdminScreen(Screen):
    def on_enter(self, *args):
        """Refresca la información al entrar al panel"""
        self.mostrar_vista_pedidos()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout estructural base
        self.main_layout = BoxLayout(orientation='vertical')
        self.add_widget(self.main_layout)
        
        # Variable intermedia para edición de productos
        self.producto_a_editar_id = None

    def generar_base_interfaz(self, titulo_seccion):
        """Limpia el contenedor y dibuja el Navbar y el Menú de Control"""
        self.main_layout.clear_widgets()

        # --- NAVBAR SUPERIOR ---
        navbar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
        with navbar.canvas.before:
            Color(rgba=colors.COLOR_CAFE)
            self.nav_rect = RoundedRectangle(size=navbar.size, pos=navbar.pos)
        navbar.bind(size=self._update_nav, pos=self._update_nav)

        navbar.add_widget(Label(text=f"Admin: {titulo_seccion} 👑", bold=True, color=colors.COLOR_BLANCO, font_size='15sp'))
        
        btn_logout = Button(text="Salir", background_color=(0,0,0,0), color=colors.COLOR_ROSADO_FONDO, bold=True, size_hint_x=0.2)
        btn_logout.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        navbar.add_widget(btn_logout)
        self.main_layout.add_widget(navbar)

        # --- MENÚ DE CONTROL (CAMBIO DE PANTALLAS DEL CRUD) ---
        menu_tabs = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=2)
        
        btn_tab_pedidos = Button(text="📋 Pedidos", background_normal='', background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE, font_size='12sp', bold=True)
        btn_tab_pedidos.bind(on_press=lambda x: self.mostrar_vista_pedidos())
        
        btn_tab_inventario = Button(text="📦 Inventario", background_normal='', background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE, font_size='12sp', bold=True)
        btn_tab_inventario.bind(on_press=lambda x: self.mostrar_vista_inventario())
        
        btn_tab_formulario = Button(text="➕ Nuevo Postre", background_normal='', background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE, font_size='12sp', bold=True)
        btn_tab_formulario.bind(on_press=lambda x: self.mostrar_vista_formulario_agregar())
        
        menu_tabs.add_widget(btn_tab_pedidos)
        menu_tabs.add_widget(btn_tab_inventario)
        menu_tabs.add_widget(btn_tab_formulario)
        self.main_layout.add_widget(menu_tabs)

        # Área de contenido dinámico desplazable
        self.contenido_scroll = ScrollView()
        self.contenido_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=12)
        self.contenido_box.bind(minimum_height=self.contenido_box.setter('height'))
        self.contenido_scroll.add_widget(self.contenido_box)
        self.main_layout.add_widget(self.contenido_scroll)


    # =========================================================================
    # VISTA 1: LISTA DE PEDIDOS Y METRICAS
    # =========================================================================
    def mostrar_vista_pedidos(self):
        self.generar_base_interfaz("Pedidos")

        # Tarjeta de Métricas rápidas (Dashboard Organizador de datos)
        total_ganancias = sum(p["total"] for p in HISTORIAL_PEDIDOS)
        pedidos_activos = sum(1 for p in HISTORIAL_PEDIDOS if p["estado"] != "Entregado")

        dashboard = BoxLayout(orientation='horizontal', size_hint_y=None, height=65, padding=8, spacing=10)
        with dashboard.canvas.before:
            Color(rgba=colors.COLOR_ROSADO_FONDO)
            rect = RoundedRectangle(size=dashboard.size, pos=dashboard.pos, radius=[6])
        dashboard.bind(size=lambda inst, val, r=rect: setattr(r, 'size', val), pos=lambda inst, val, r=rect: setattr(r, 'pos', val))

        dashboard.add_widget(Label(text=f"Ventas: ${total_ganancias:.2f}", bold=True, color=colors.COLOR_CAFE, font_size='13sp'))
        dashboard.add_widget(Label(text=f"Pendientes: {pedidos_activos}", bold=True, color=colors.COLOR_CAFE, font_size='13sp'))
        self.contenido_box.add_widget(dashboard)

        # Renderizar Órdenes realizadas
        for index, pedido in enumerate(HISTORIAL_PEDIDOS):
            tarjeta = BoxLayout(orientation='horizontal', size_hint_y=None, height=90, padding=8, spacing=5)
            fondo_tarjeta = colors.COLOR_BEIGE if pedido["estado"] != "Entregado" else (0.85, 0.95, 0.85, 1)
            
            with tarjeta.canvas.before:
                Color(rgba=fondo_tarjeta)
                r_tarjeta = RoundedRectangle(size=tarjeta.size, pos=tarjeta.pos, radius=[6])
            tarjeta.bind(size=lambda inst, val, r=r_tarjeta: setattr(r, 'size', val), pos=lambda inst, val, r=r_tarjeta: setattr(r, 'pos', val))

            # Información interna
            info = BoxLayout(orientation='vertical', spacing=2, size_hint_x=0.7)
            info.add_widget(Label(text=f"Orden #{pedido['id_pedido']} - {pedido['cliente']}", bold=True, color=colors.COLOR_CAFE, font_size='13sp', halign='left'))
            info.add_widget(Label(text=pedido["productos"], font_size='11sp', color=(0.4, 0.3, 0.3, 1)))
            info.add_widget(Label(text=f"Total: ${pedido['total']:.2f} [{pedido['estado']}]", bold=True, font_size='12sp', color=colors.COLOR_CAFE))
            tarjeta.add_widget(info)

            # Acción cambiar de estado
            acciones = BoxLayout(orientation='vertical', size_hint_x=0.3)
            if pedido["estado"] != "Entregado":
                btn_listo = Button(text="Listo ✅", font_size='11sp', background_normal='', background_color=colors.COLOR_ROSADO_BOTON, color=colors.COLOR_CAFE)
                btn_listo.bind(on_press=lambda inst, idx=index: self.marcar_pedido_entregado(idx))
                acciones.add_widget(btn_listo)
            else:
                acciones.add_widget(Label(text="Despachado ✨", color=(0.2, 0.5, 0.2, 1), font_size='11sp', bold=True))

            tarjeta.add_widget(acciones)
            self.contenido_box.add_widget(tarjeta)

    def marcar_pedido_entregado(self, index):
        HISTORIAL_PEDIDOS[index]["estado"] = "Entregado"
        self.mostrar_vista_pedidos()


    # =========================================================================
    # VISTA 2: GESTIÓN DE INVENTARIO (EDITAR / ELIMINAR PRODUCTOS)
    # =========================================================================
    def mostrar_vista_inventario(self):
        self.generar_base_interfaz("Inventario")

        if not LISTA_PRODUCTOS:
            self.contenido_box.add_widget(Label(text="No hay productos en catálogo.", color=colors.COLOR_CAFE, font_size='14sp'))
            return

        for prod in LISTA_PRODUCTOS:
            tarjeta = BoxLayout(orientation='horizontal', size_hint_y=None, height=75, padding=8, spacing=5)
            with tarjeta.canvas.before:
                Color(rgba=colors.COLOR_BEIGE)
                r = RoundedRectangle(size=tarjeta.size, pos=tarjeta.pos, radius=[6])
            tarjeta.bind(size=lambda inst, val, rect=r: setattr(rect, 'size', val), pos=lambda inst, val, rect=r: setattr(rect, 'pos', val))

            # Detalle simple del stock
            detalles = BoxLayout(orientation='vertical', spacing=2, size_hint_x=0.55)
            detalles.add_widget(Label(text=prod["nombre"], bold=True, color=colors.COLOR_CAFE, font_size='14sp', halign='left'))
            detalles.add_widget(Label(text=f"Precio / Administración: ${prod['precio']:.2f}", color=colors.COLOR_CAFE, font_size='12sp'))
            tarjeta.add_widget(detalles)

            # Botones de Control Operativo
            controles = BoxLayout(orientation='horizontal', size_hint_x=0.45, spacing=4)
            
            btn_edit = Button(text="✏️", background_normal='', background_color=(0.9, 0.9, 0.9, 1))
            btn_edit.bind(on_press=lambda inst, p=prod: self.cargar_formulario_edicion(p))
            
            btn_delete = Button(text="🗑️", background_normal='', background_color=(0.9, 0.4, 0.4, 0.2), color=(0.8, 0.2, 0.2, 1))
            btn_delete.bind(on_press=lambda inst, pid=prod["id"]: self.eliminar_producto_logica(pid))
            
            controles.add_widget(btn_edit)
            controles.add_widget(btn_delete)
            tarjeta.add_widget(controles)

            self.contenido_box.add_widget(tarjeta)

    def eliminar_producto_logica(self, prod_id):
        """Función: Eliminar Productos del CRUD"""
        global LISTA_PRODUCTOS
        LISTA_PRODUCTOS[:] = [p for p in LISTA_PRODUCTOS if p["id"] != prod_id]
        self.mostrar_vista_inventario()


    # =========================================================================
    # VISTA 3: FORMULARIOS ADMINISTRATIVOS (AGREGAR / EDITAR)
    # =========================================================================
    def mostrar_vista_formulario_agregar(self):
        self.producto_a_editar_id = None # Reset de estado
        self.generar_base_interfaz("Nuevo Producto")
        self.dibujar_formulario("", "", "", "", "")

    def cargar_formulario_edicion(self, producto):
        self.producto_a_editar_id = producto["id"]
        self.generar_base_interfaz("Editar Producto")
        self.dibujar_formulario(producto["nombre"], producto["categoria"], producto["descripcion"], str(producto["precio"]), producto["imagen"])

    def dibujar_formulario(self, nom, cat, desc, prec, img):
        """Estructura de Formulario Administrativo"""
        self.txt_nombre = TextInput(text=nom, hint_text="Nombre del postre", multiline=False, size_hint_y=None, height=40)
        self.txt_categoria = TextInput(text=cat, hint_text="Categoría (Tortas, Cupcakes, etc.)", multiline=False, size_hint_y=None, height=40)
        self.txt_descripcion = TextInput(text=desc, hint_text="Descripción", multiline=True, size_hint_y=None, height=60)
        self.txt_precio = TextInput(text=prec, hint_text="Precio (Ej: 12.50)", multiline=False, size_hint_y=None, height=40)
        self.txt_imagen = TextInput(text=img, hint_text="URL de la imagen", multiline=False, size_hint_y=None, height=40)

        # Inyección visual de etiquetas y campos de entrada
        self.contenido_box.add_widget(Label(text="Nombre del Producto:", color=colors.COLOR_CAFE, bold=True, size_hint_y=None, height=20))
        self.contenido_box.add_widget(self.txt_nombre)
        self.contenido_box.add_widget(Label(text="Categoría:", color=colors.COLOR_CAFE, bold=True, size_hint_y=None, height=20))
        self.contenido_box.add_widget(self.txt_categoria)
        self.contenido_box.add_widget(Label(text="Descripción:", color=colors.COLOR_CAFE, bold=True, size_hint_y=None, height=20))
        self.contenido_box.add_widget(self.txt_descripcion)
        self.contenido_box.add_widget(Label(text="Precio Comercial ($):", color=colors.COLOR_CAFE, bold=True, size_hint_y=None, height=20))
        self.contenido_box.add_widget(self.txt_precio)
        self.contenido_box.add_widget(Label(text="URL Imagen Ilustrativa:", color=colors.COLOR_CAFE, bold=True, size_hint_y=None, height=20))
        self.contenido_box.add_widget(self.txt_imagen)

        self.lbl_status = Label(text="", color=(0.2, 0.6, 0.2, 1), bold=True, size_hint_y=None, height=25)
        self.contenido_box.add_widget(self.lbl_status)

        # Botón de Guardado
        texto_boton = "GUARDAR CAMBIOS 💾" if self.producto_a_editar_id else "CREAR PRODUCTO 🍰"
        btn_guardar = Button(text=texto_boton, background_normal='', background_color=colors.COLOR_CAFE, color=colors.COLOR_BLANCO, bold=True, size_hint_y=None, height=46)
        btn_guardar.bind(on_press=self.procesar_formulario_crud)
        self.contenido_box.add_widget(btn_guardar)

    def procesar_formulario_crud(self, instance):
        """Lógica del CRUD: Agregar productos / Administrar precios"""
        try:
            nombre = self.txt_nombre.text.strip()
            categoria = self.txt_categoria.text.strip()
            descripcion = self.txt_descripcion.text.strip()
            precio = float(self.txt_precio.text.strip())
            imagen = self.txt_imagen.text.strip() or "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400"

            if not nombre or not categoria:
                self.lbl_status.color = (0.9, 0.2, 0.2, 1)
                self.lbl_status.text = "Error: Rellena los campos obligatorios."
                return

            if self.producto_a_editar_id:
                # OPERACIÓN: EDITAR / ADMINISTRAR PRECIOS
                for p in LISTA_PRODUCTOS:
                    if p["id"] == self.producto_a_editar_id:
                        p["nombre"] = nombre
                        p["categoria"] = categoria
                        p["descripcion"] = descripcion
                        p["precio"] = precio
                        p["imagen"] = imagen
                        break
                self.lbl_status.color = (0.2, 0.6, 0.2, 1)
                self.lbl_status.text = "¡Producto modificado con éxito!"
            else:
                # OPERACIÓN: AGREGAR NUEVO
                nuevo_id = str(len(LISTA_PRODUCTOS) + 1)
                nuevo_postre = {
                    "id": nuevo_id,
                    "nombre": nombre,
                    "categoria": categoria,
                    "descripcion": descripcion,
                    "precio": precio,
                    "imagen": imagen
                }
                LISTA_PRODUCTOS.append(nuevo_postre)
                self.lbl_status.color = (0.2, 0.6, 0.2, 1)
                self.lbl_status.text = "¡Producto creado exitosamente!"
                
                # Limpiar formulario
                self.txt_nombre.text = ""; self.txt_categoria.text = ""; self.txt_descripcion.text = ""; self.txt_precio.text = ""; self.txt_imagen.text = ""

        except ValueError:
            self.lbl_status.color = (0.9, 0.2, 0.2, 1)
            self.lbl_status.text = "Error: El precio debe ser un número válido."

    # Actualizadores de tamaño geométrico de Kivy
    def _update_nav(self, instance, value): self.nav_rect.pos = instance.pos; self.nav_rect.size = instance.size