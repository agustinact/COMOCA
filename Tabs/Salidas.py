
import tkinter as tk
from tkinter import ttk
from tkinter import *
from Auxiliares.Reporte_Salidas import reporte_salidas
from Auxiliares.sqlqueries import QueriesSQLite
from tkcalendar import DateEntry
from Tablas.Tablas import Salidas_table
from Auxiliares.Botonera import Botonera, Exportar
from Auxiliares.Busqueda_Codbar import ResultadosBusquedaPopup
from tkinter import messagebox
from Auxiliares.Completar_Remito import *
import datetime


class Salidas_Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        second_frame = ttk.Frame(self)
        second_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        
        self.label_codbar = ttk.Label(second_frame, text="Presione para crear una salida")
        self.label_codbar.pack(side='left', fill='x', padx=5)
        
        self.scan = ttk.Button(second_frame, text="Salida por Caja", command=self.salida)
        self.scan.pack(side='left', fill='both', padx=5)
        
        self.pallet_out = ttk.Button(second_frame, text="Salida por Pallet", command=self.salida_pallet)
        self.pallet_out.pack(side='left', fill='both', padx=5)
        
        self.reporte_btn = Exportar(second_frame, self.exportar)
        self.reporte_btn.pack(side='left', padx=5)

        table_frame = ttk.Frame(self)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True , pady=10)
        self.tabla = Salidas_table(table_frame)
        self.tabla.pack(fill='both', expand=True, padx=5)        
    
    def salida(self):
        self.remito_popup = Remito(self.tabla.cargar_datos, "Caja" ,self.tabla.lista_remitos)
        self.remito_popup.title("Scanner")
        self.remito_popup.grab_set()
    
    def salida_pallet(self):
        self.remito_popup = Remito(self.tabla.cargar_datos, "Pallet" ,self.tabla.lista_remitos)
        self.remito_popup.title("Scanner")
        self.remito_popup.grab_set()
    
    def exportar(self):
        items = self.tabla.tree.get_children()
        lista_valores =[]
        if items:
            for item in items:
                valores = self.tabla.tree.item(item, "values")
                lista_valores.append(valores)
            respuesta   = messagebox.askokcancel("Reporte","Desea generar reporte?")

            if respuesta:
                reporte_salidas(lista_valores)
    
        
class Remito(tk.Toplevel):
    def __init__(self, actualizar_tabla_cb, tipo_salida, lista_remitos_cb):
        super().__init__()
        self.actualizar_tabla_cb = actualizar_tabla_cb
        self.lista_remitos_cb = lista_remitos_cb
        self.tipo_salida = tipo_salida
        self.center_window()
        # self.grab_set()
        self.barcode = ""
        self.id_cliente = ""
        self.items_salida = []
        self.id_remito = self.num_remito()
        # self.cargar_datos_cb = cargar_datos_cb
        
        self.frame = ttk.Frame(self)
        self.frame.pack(fill='both', expand=True)
        
        main_frame = ttk.Frame(self.frame)
        main_frame.pack()
        
        self.frame_label = ttk.Frame(main_frame)
        self.frame_label.pack(side='left')
        self.frame_entry = ttk.Frame(main_frame)
        self.frame_entry.pack(side="left")
        
        self.label_clientes = ttk.Label(self.frame_label, text="Seleccione Cliente")
        self.label_clientes.pack(fill='x', padx=5, pady=5)
        
        self.clientes_desplegables  = ttk.Combobox(self.frame_entry, state="readonly")
        self.clientes_desplegables.pack(fill='x', padx=5, pady=5)
        
        self.label_factura = ttk.Label(self.frame_label, text="Factura correspondiente:")
        self.label_factura.pack(fill='x', padx=5, pady=5)
        
        self.factura_entry  = ttk.Entry(self.frame_entry)
        self.factura_entry.pack(fill='x', padx=5, pady=5)
        
        self.label_uno = ttk.Label(self.frame, text="------------------------------")
        self.label_uno.pack(pady=5, padx=5)
        
        if self.tipo_salida == "Caja":
            self.entry = ttk.Entry(self.frame)
            self.entry.pack(fill="x", pady= 10, padx=5)
            self.entry.config(state=DISABLED)                         
            
            self.result_label = ttk.Label(self.frame, text="")
            self.result_label.pack(pady=10, padx=5)
            self.result_label2 = ttk.Label(self.frame, text="")
            self.result_label2.pack(fill='x', padx=5)
            
            self.botonera = Botonera(self.frame, None, self.agregar_codebar)
            self.botonera.agregar.config(state=DISABLED)
            self.botonera.pack(anchor="center", pady=10)
            
            
            self.salida_button = Button(self.frame, text="Confirmar Salida", command=self.dar_salida)
            self.clientes_desplegables.bind("<<ComboboxSelected>>", self.get_entries)

            self.entry.bind('<Return>', lambda event: self.agregar_codebar())
        elif self.tipo_salida == "Pallet":
            self.lista_pallets = ttk.Combobox(self.frame, state="readonly")
            self.lista_pallets.pack(fill="x", pady= 10, padx=5)
            # self.lista_pallets.config(state=DISABLED)                         
            
            # self.result_label = ttk.Label(self.frame, text="")
            # self.result_label.pack(pady=10, padx=5)
            # self.result_label2 = ttk.Label(self.frame, text="")
            # self.result_label2.pack(fill='x', padx=5)
            
            self.botonera = Botonera(self.frame, None, self.agregar_pallet)
            self.botonera.agregar.config(state=DISABLED)
            self.botonera.agregar.config(text="Agregar Pallet")
            self.botonera.pack(anchor="center", pady=10)
            
            self.salida_button = Button(self.frame, text="Confirmar Salida", command=self.dar_salida)
            self.stock_pallets()
            self.lista_pallets.bind("<<ComboboxSelected>>", self.enable_btn)
            self.clientes_desplegables.bind("<<ComboboxSelected>>", self.enable_btn)
            
        self.salida_button.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        self.salida_button.config(state=DISABLED)
        
        
        self.clientes_lista()
    
    def enable_btn(self, event):
        get_cliente = self.clientes_desplegables.get() 
        if get_cliente:
            id_cliente = get_cliente.split("-")
            self.id_cliente = id_cliente[0]
            self.cliente = id_cliente[1]
            get_pallet = self.lista_pallets.get()
            if get_pallet:
                self.botonera.agregar.config(state=NORMAL)


    
    def stock_pallets(self):
        connection = QueriesSQLite.create_connection('nuevaDB.sqlite')
        query = "SELECT DISTINCT id_pallet FROM stock"
        listar_pallets = QueriesSQLite.execute_read_query(connection, query)
        if listar_pallets:
            self.lista_pallets['values'] = listar_pallets
            
    def info_pallet(self, pallet_id, pallet, proveedor, producto):
        peso = sum(caja[4] for caja in pallet)
        bultos = len(pallet)
        respuesta = messagebox.askokcancel(f"Agregar pallet: {pallet_id}", f"Desea agregar al remito N°: {self.id_remito} \n Producto: {producto} \n Cant bultos: {bultos}\n Peso: {peso}\n Proveedor: {proveedor}")
        return respuesta
     
    def agregar_pallet(self):
        get_pallet = self.lista_pallets.get()
        if get_pallet:
            connection = QueriesSQLite.create_connection('nuevaDB.sqlite')
            query = "SELECT * FROM stock WHERE id_pallet = ?"
            pallet = QueriesSQLite.execute_read_query(connection, query, (get_pallet,))
            id_prov = QueriesSQLite.execute_read_query(connection, "SELECT DISTINCT id_proveedor FROM stock WHERE id_pallet = ?", (get_pallet,))
            id_prod = QueriesSQLite.execute_read_query(connection, "SELECT DISTINCT id_producto FROM stock WHERE id_pallet = ?", (get_pallet,))
            proveedor = QueriesSQLite.execute_read_query(connection, "SELECT nombre FROM proveedores WHERE id = ?", id_prov[0])
            producto = QueriesSQLite.execute_read_query(connection, "SELECT detalle FROM productos WHERE id = ?", id_prod[0])
            respuesta = self.info_pallet(get_pallet, pallet, proveedor[0][0], producto[0][0])
            if respuesta:
                for box in pallet:
                    # item_salida = (remito_id, cod_caja, producto, cliente, peso, tropa, fecha, id_proveedor, pallet_id)
                    box_list = list(box)
                    box_list[0] = self.id_remito
                    box_list[2] = producto[0][0]
                    box_list[3] = self.cliente
                    box_list[6] = datetime.date.today()
                    box_list[7] = proveedor[0][0]
                    box = tuple(box_list)
                    self.items_salida.append(box)
                self.botonera.agregar.config(state=DISABLED)
                self.salida_button.config(state=NORMAL)
            
    def search_codbar(self):
        self.entry.config(state=NORMAL)
        self.entry.focus_set()
        # self.entry.bind('<Return>', self.codbar_scaned)
        self.label_uno.config(text="Escanee el código de barras a buscar y presione Enter", foreground='blue')
        self.result_label.config(text="")
        self.result_label2.config(text="")
        self.botonera.busqueda.config(state=DISABLED)
        self.botonera.agregar.config(state=DISABLED)
        

        
    def get_entries(self, event):
        get_cliente = self.clientes_desplegables.get()
        id_cliente = get_cliente.split("-")
        self.id_cliente = id_cliente[0]
        if get_cliente:
            self.label_uno.config(text="Ya puede escanear el código de Barras", foreground='blue')
            self.entry.config(state=NORMAL)
            self.entry.focus_set()
            self.entry.bind('<Return>', self.scan)

    def scan(self, event):
        barcode = self.entry.get()
        if barcode:
            self.result_label.config(text=f"Código de Barras escaneado:", foreground='green')
            self.result_label2.config(text=barcode, anchor="center", background='white', relief="solid")
            self.entry.delete(0, tk.END)
            self.enable_buttons(barcode)
            self.barcode = barcode
        else:
            messagebox.showinfo("Campos vacíos", "Scanee o ingrese código")
            
    def enable_buttons(self, barcode=None):    
        if barcode:
            self.botonera.agregar.config(state=NORMAL)        
    
    def clientes_lista(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query      = "SELECT * FROM clientes"
        clientes  = QueriesSQLite.execute_read_query(connection, query)
        if clientes:
            lista_clientes = [f"{cliente[0]}-{cliente[1]}" for cliente in clientes]
            self.clientes_desplegables['values'] = lista_clientes 
        
    def agregar_codebar(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        busqueda   = "SELECT * FROM salidas WHERE cod_caja = ?"
        item       = QueriesSQLite.execute_read_query(connection, busqueda, (self.barcode,))
        if item:
            messagebox.showwarning("BBDD", "Ya ha ingresado un item con el mismo código")
        else:
            query = "SELECT * FROM stock WHERE cod_caja = ?"
            item_stock = QueriesSQLite.execute_read_query(connection, query, (self.barcode,))
            if item_stock:
                remito_id = self.id_remito
                cod_caja = item_stock[0][1]
                producto = QueriesSQLite.execute_read_query(connection, "SELECT detalle FROM productos WHERE id = ?", (item_stock[0][2],))
                cliente  = QueriesSQLite.execute_read_query(connection, "SELECT nombre FROM clientes WHERE id = ?", (self.id_cliente,))
                id_proveedor = item_stock[0][3]
                peso     = item_stock[0][4]
                tropa    = item_stock[0][5]
                fecha    = datetime.date.today()
                pallet_id = item_stock[0][8]
                n_factura = item_stock[0][9]
                self.confirmar_codebar(remito_id, cod_caja, producto[0][0], cliente[0][0], peso, tropa, fecha, id_proveedor, pallet_id, n_factura)
            else:
                messagebox.showwarning("BBDD", "No se ha encontrado el código en el inventario")                    
                
    def confirmar_codebar(self, remito_id, cod_caja, producto, cliente, peso, tropa, fecha, id_proveedor, pallet_id, n_factura):
        respuesta = messagebox.askokcancel("Confirmación", f"""Desea agregar al remito N°{remito_id}:\n{cod_caja} - {producto} - {peso} - {tropa}.\nCon destino al cliente: {cliente}""")
        existe = False
        
        if respuesta:
            item_salida = (remito_id, cod_caja, producto, cliente, peso, tropa, fecha, id_proveedor, pallet_id, n_factura)
            
            for item in self.items_salida:
                if item_salida[1] in item:
                    existe = True
                    
            if not existe:
                self.items_salida.append(item_salida)
                self.salida_button.config(state=NORMAL)
            else:
                messagebox.showwarning("Salidas","Este producto ya está en la campaña de salida")
        self.entry.focus_set()
        self.botonera.agregar.config(state=DISABLED)
                
    def delete_ingreso(self, cod_caja):
        connection =  QueriesSQLite.create_connection("nuevaDB.sqlite")
        delete = "DELETE FROM stock WHERE cod_caja = ?"
        QueriesSQLite.execute_query(connection, delete, (cod_caja,))
        # messagebox.showinfo("BBDD","Datos eliminados correctamente")
        
        
    def dar_salida(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query = "INSERT INTO salidas (id_remito, cod_caja, producto, cliente, peso, tropa, fecha_egreso, id_proveedor, id_pallet, f_proveedor) VALUES (?,?,?,?,?,?,?,?,?,?)"
        if self.items_salida:
            for salida in self.items_salida:
                QueriesSQLite.execute_query(connection, query, salida)
                self.delete_ingreso(salida[1])
                self.actualizar_tabla_cb
            self.salida_button.config(state=DISABLED)
            self.crear_remito()
            self.destroy()
        
    def num_remito(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        contar = "SELECT COUNT(*) FROM remitos"
        siguiente = QueriesSQLite.execute_read_query(connection, contar)
        if siguiente:
            format = "{:08}".format(siguiente[0][0]+1)
            remito_id = f"0001-{format}"
            return remito_id
        
    def crear_remito(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query_cliente = "SELECT * FROM clientes WHERE id = ?"
        datos_cliente = QueriesSQLite.execute_read_query(connection, query_cliente, (self.id_cliente,))
        tupla_cliente = tuple(datos_cliente[0])
        lista_salida  = QueriesSQLite.execute_read_query(connection, "SELECT * FROM salidas WHERE id_remito = ?", (self.id_remito,))
        factura = self.factura_entry.get()
        if not factura:
            factura = "-"
        datos_remito = []

        for tupla in lista_salida:
            id_producto = QueriesSQLite.execute_read_query(connection, "SELECT id FROM productos WHERE detalle = ?", (tupla[3],))
            producto = tupla[3]
            peso = tupla[5]
            tropa = tupla[6]
            
            encontrado = False
            for datos_tupla in datos_remito:
                if producto == datos_tupla[1] and tropa == datos_tupla[2]:
                    datos_tupla[3] += 1  # Incrementa el número de bultos
                    datos_tupla[4].append(peso)  # Añade el peso a la lista de pesos
                    encontrado = True
                    break

            if not encontrado:
                # Si no se encontró una tupla existente con el mismo producto y tropa, crea una nueva tupla
                nueva_tupla = [id_producto[0][0], producto, tropa, 1, [peso]]
                datos_remito.append(nueva_tupla)

        adjudicar_remito(self.id_remito, tupla_cliente, datos_remito, factura)
        self.insert_remito(datos_remito, datos_cliente[0][1])
        self.actualizar_tabla_cb()
        self.lista_remitos_cb()
        self.clientes_lista()
        
    def insert_remito(self, datos_remito, cliente):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        insert = "INSERT INTO remitos(id_remito, cliente, total, fecha, factura) VALUES (?,?,?,?,?)"
        total = 0
        fecha = datetime.date.today()
        factura = self.factura_entry.get()
        
        for lista in datos_remito:
            for peso in lista[4]:
                total += peso
        QueriesSQLite.execute_query(connection, insert, (self.id_remito, cliente, total, fecha, factura))

        
    def center_window(self):
    # Obtener el ancho y alto de la ventana
        window_width = 300
        window_height = 325

        # Obtener el ancho y alto de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular la posición del lado superior izquierdo de la ventana para centrarla
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Configurar la geometría de la ventana para centrarla
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
            