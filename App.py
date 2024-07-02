import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Tabs.Ingresos import Ingresos_Frame
from Tabs.Proveedores import Proveedores_Frame
from Tabs.Productos import Productos_Frame
from Tabs.Romaneos import Romaneos_Frame
from Tabs.Salidas import Salidas_Frame
from Tabs.Clientes import Clientes_Frame


class AppWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # self.geometry("800x600")
        self.center_window()
        self.title("Gestión de Inventario")
        self.resizable(height=0, width=0)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.tab_proveedores = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_proveedores, text='Proveedores')

        self.tab_productos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_productos, text='Productos')
        
        self.tab_ingresos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ingresos, text='Ingresos')
        
        self.tab_salidas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_salidas, text='Salidas')
        
        self.tab_clientes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_clientes, text='Clientes')
        
        self.tab_romaneos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_romaneos, text='Romaneos')
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        


        self.create_widgets_proveedores()
        self.create_widgets_productos()
        self.create_widgets_ingresos()
        self.create_widgets_salidas()
        self.create_widgets_clientes()
        self.create_widgets_romaneos()
        
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
    def cerrar_app(self):
        self.quit()

    def create_widgets_proveedores(self):
        proveedores = Proveedores_Frame(self.tab_proveedores)
        # proveedores.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        proveedores.pack(fill="both", expand=True)

    def create_widgets_productos(self):
        self.productos = Productos_Frame(self.tab_productos)
        self.productos.pack(fill="both", expand=True)

        
    def create_widgets_ingresos(self): 
        self.ingresos = Ingresos_Frame(self.tab_ingresos)
        self.ingresos.pack(fill="both", expand=True)
        
    def create_widgets_salidas(self): 
        self.salidas = Salidas_Frame(self.tab_salidas)
        self.salidas.pack(fill="both", expand=True)
        
    def create_widgets_clientes(self):
        clientes = Clientes_Frame(self.tab_clientes)
        clientes.pack(fill="both", expand=True)   
        
    def create_widgets_romaneos(self):
        self.romaneos = Romaneos_Frame(self.tab_romaneos)
        self.romaneos.pack(fill="both", expand=True) 
             
    def center_window(self):
        # Obtener el ancho y alto de la ventana
        window_width = 1200
        window_height = 500

        # Obtener el ancho y alto de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
####

        # Calcular la posición del lado superior izquierdo de la ventana para centrarla
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Configurar la geometría de la ventana para centrarla
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        
    def on_tab_change(self, event):
        
        selected_tab = event.widget.tab(event.widget.index("current"), "text")
        if selected_tab == 'Productos':
            self.productos.productos_table.cargar_datos()

        if selected_tab == 'Ingresos':
            self.ingresos.tabla.cargar_datos()
        
        if selected_tab == 'Salidas':
            self.salidas.tabla.cargar_datos()
        
        if selected_tab == 'Romaneos':
            self.romaneos.listar_facturas()
        