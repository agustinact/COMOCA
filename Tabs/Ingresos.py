from multiprocessing import connection
from os import access
import tkinter as tk
from tkinter import ttk
from tkinter import *
from Auxiliares.sqlqueries import QueriesSQLite
from tkcalendar import DateEntry
from Tablas.Tablas import Stock_table
from Auxiliares.Botonera import Botonera, Exportar
from Auxiliares.Busqueda_Codbar import ResultadosBusquedaPopup
from Auxiliares.Seguridad import PasswordWindow
from tkinter import messagebox
from Auxiliares.Reporte_Ingresos import *
import datetime


class Ingresos_Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.id_pallet =""
        second_frame = ttk.Frame(self)
        second_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        
        self.label_codbar = ttk.Label(second_frame, text="Click para empezar a escanear")
        self.label_codbar.pack(side='left', fill='x', padx=5)
        
        self.scan = ttk.Button(second_frame, text="Nuevo Ingreso", command=self.abrir_ingreso)
        self.scan.pack(side='left', fill='both', padx=5)
        
        self.botonera = Botonera(second_frame, None, None, self.eliminar_safety)
        self.botonera.pack(side='left', padx=5)
        
        self.reporte_btn = Exportar(second_frame, self.exportar)
        self.reporte_btn.pack(side='left', padx=5)
        

        
        table_frame = ttk.Frame(self)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True , pady=10)
        self.tabla = Stock_table(table_frame)
        self.tabla.pack(fill='both', expand=True, padx=5)        
    
    def abrir_ingreso(self):
        self.nuevo_pallet()
        self.scan_popup = Scan_PopUp(self.tabla.cargar_datos, self.id_pallet, self.tabla.lista_facturas)
        self.scan_popup.title("Scanner")
        self.scan_popup.grab_set()
        
        
    def eliminar_safety(self):
        values = self.tabla.seleccion_datos()        
        if values:
            safety = PasswordWindow()
            access = safety.wait_response()
            if access:
                self.eliminar_ingreso()
        else:
            messagebox.showerror("Error", "Seleccione algún Producto")
    
    def nuevo_pallet(self):
        def extract_number(id_string):
            return int(id_string[2:])

        connection = QueriesSQLite.create_connection('nuevaDB.sqlite')
        query = "SELECT id_pallet FROM pallets"
        id_list = QueriesSQLite.execute_read_query(connection, query)

        if not id_list:
            print("No hay pallets en la base de datos.")
            # Devuelve el primer ID si no hay pallets en la base de datos
            self.id_pallet = 'CP1'
        else:
        # Extraer los valores de los id_pallet
            id_values = [row[0] for row in id_list]

            # Obtener el id máximo
            max_id = max(id_values, key=extract_number)
            
            # Extraer el número del id máximo, sumarle 1 y crear el nuevo id
            new_number = extract_number(max_id) + 1
            new_id = f'CP{new_number}'
            self.id_pallet = new_id

        
    def eliminar_ingreso(self):
        values = self.tabla.seleccion_datos()
        respuesta = messagebox.askokcancel("Eliminar",f"Eliminar ingreso:\n {values} ")

        if respuesta:
            connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
            query = "DELETE FROM stock WHERE id = (?)"
            QueriesSQLite.execute_query(connection, query, (values[0],))
            messagebox.showinfo("BBDD","Datos eliminados correctamente")
            self.tabla.cargar_datos()
            
    def exportar(self):
        items = self.tabla.tree.get_children()
        lista_valores =[]
        if items:
            for item in items:
                valores = self.tabla.tree.item(item, "values")
                lista_valores.append(valores)
            respuesta   = messagebox.askokcancel("Reporte",f"Desea generar reporte?")

            if respuesta:
                reporte_ingresos(lista_valores)        
        
class Scan_PopUp(tk.Toplevel):
    def __init__(self, cargar_datos_cb, pallet_id, cargar_factura):
        super().__init__()
        self.center_window()
        self.grab_set()
        self.cargar_factura = cargar_factura
        self.barcode = ""    
        self.send_prod = ""
        self.send_prov = ""
        self.send_idprov = ""
        self.send_idprod = ""
        self.fecha_vencimiento = None
        self.send_tropa = ""
        self.send_factura = ""
        self.peso_entry = None
        self.cargar_datos_cb = cargar_datos_cb
        self.pallet_id = pallet_id
        
        self.frame = ttk.Frame(self)
        self.frame.pack(fill='both', expand=True)
        
        self.main_frame = ttk.Frame(self.frame)
        self.main_frame.pack()
        
        self.frame_label = ttk.Frame(self.main_frame)
        self.frame_label.pack(side='left')
        self.frame_entry = ttk.Frame(self.main_frame)
        self.frame_entry.pack(side="left")
        
        self.label_ingresar = ttk.Label(self.frame_label, text="Seleccionar Producto a ingresar")
        self.label_ingresar.pack(fill='x', padx=5, pady=5)
        
        self.producto_desplegables  = ttk.Combobox(self.frame_entry, state="readonly")
        self.producto_desplegables.pack(fill='x', padx=5, pady=5)
        
        self.label_proveedor = ttk.Label(self.frame_label, text="Seleccione Proveedor")
        self.label_proveedor.pack(fill='x', padx=5, pady=5)
        
        self.proveedores_desplegables  = ttk.Combobox(self.frame_entry, state="readonly")
        self.proveedores_desplegables.pack(fill='x', padx=5, pady=5)
        
        self.label_vencimiento = ttk.Label(self.frame_label, text="Seleccione Fecha de Vencimiento")
        self.label_vencimiento.pack(fill='x', padx=5, pady=5)
        
        self.entry_vencimiento = DateEntry(self.frame_entry, width=12, background='darkblue',foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy", showweeknumbers=False)
        self.entry_vencimiento.pack(fill='x', padx=5, pady=5)
        
        self.label_tropa = ttk.Label(self.frame_label, text="Ingrese ID Tropa")
        self.label_tropa.pack(fill='x', padx=5, pady=5)
        
        self.entry_tropa  = ttk.Entry(self.frame_entry)
        self.entry_tropa.pack(fill='x', padx=5, pady=5)
        
        self.label_factura = ttk.Label(self.frame_label, text="Ingrese N° Factura")
        self.label_factura.pack(fill='x', padx=5, pady=5)
        
        self.entry_factura  = ttk.Entry(self.frame_entry)
        self.entry_factura.pack(fill='x', padx=5, pady=5)
        
        self.label_uno = ttk.Label(self.frame, text="------------------------------")
        self.label_uno.pack(pady=5, padx=5)
        self.entry = ttk.Entry(self.frame)
        self.entry.pack(fill="x", pady= 10, padx=5)
        self.entry.config(state=DISABLED)                         
        
        self.result_label = ttk.Label(self.frame, text="")
        self.result_label.pack(pady=10, padx=5)
        self.result_label2 = ttk.Label(self.frame, text="")
        self.result_label2.pack(fill='x', padx=5)
        
        self.botonera = Botonera(self.frame, self.search_codbar)
        # self.botonera = Botonera(self.frame, self.search_codbar, self.agregar_codebar)
        # self.botonera.agregar.config(state=DISABLED)
        self.botonera.pack(anchor="center", pady=10)
        
        self.cerrar_pallet_btn = ttk.Button(self.frame, text='Cerrar Pallet', command=self.cerrar_pallet)
        self.cerrar_pallet_btn.pack()
        self.cerrar_pallet_btn.config(state=DISABLED)
        
        self.producto_desplegables.bind("<<ComboboxSelected>>", self.get_entries)
        self.proveedores_desplegables.bind("<<ComboboxSelected>>", self.get_entries)
        self.entry_vencimiento.bind("<<ComboboxSelected>>", self.get_entries)
        self.entry_tropa.bind("<Return>", self.get_entries)
        self.entry_factura.bind("<Return>", self.get_entries)
        # self.entry.bind("<Return>",self.agregar_codebar)
        self.proveedores_lista()
        self.productos_lista()       
    
    def cerrar_pallet(self):
        respuesta = messagebox.askokcancel("Cerrar Pallet",f"Desea cerrar el pallet: {self.pallet_id}")
        if respuesta:
            self.insertar_pallet()
            self.destroy()
            # self.cerrar_pallet_btn.state(state=DISABLED)
        
    def insertar_pallet(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query = "SELECT * FROM stock WHERE id_pallet = ?"
        items_pallet = QueriesSQLite.execute_read_query(connection,query,(self.pallet_id))
        print("id pallet", self.pallet_id)
        print("items pallets", items_pallet)
        kilos = 0
        if items_pallet:
            print()
            for item in items_pallet:
                kilos += item[4]
        fecha = datetime.date.today()
        tupla_pallet = (self.pallet_id, self.send_prov, kilos, fecha, self.send_prod, 'INGRESADO')
        crear_pallet = """
        INSERT INTO 
            pallets (id_pallet, proveedor, peso_total, fecha, producto, estado)
        VALUES
            (?, ?, ?, ?, ?, ?)
        """
        QueriesSQLite.execute_query(connection, crear_pallet, tupla_pallet)
    
        

            
    def search_codbar(self):
        self.entry.config(state=NORMAL)
        self.entry.focus_set()
        self.entry.bind('<Return>', self.codbar_scaned)
        self.label_uno.config(text="Escanee el código de barras a buscar y presione Enter", foreground='blue')
        self.result_label.config(text="")
        self.result_label2.config(text="")
        self.botonera.busqueda.config(state=DISABLED)
        # self.botonera.agregar.config(state=DISABLED)
        
        
    def codbar_scaned(self, event):
        barcode = str(self.entry.get())
        if barcode:
            self.entry.delete(0, tk.END)
            self.buscar_codebar(barcode)
    
    def buscar_codebar(self, barcode):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        busqueda = "SELECT * FROM stock WHERE cod_caja = ?"
        tuple_item = QueriesSQLite.execute_read_query(connection, busqueda, (barcode,))
        item = list(tuple_item[0])
        if item:
           ResultadosBusquedaPopup(item)
           self.entry.config(state=DISABLED)
        else:
            messagebox.showinfo("BBDD", "Código de barras no encontrado")
        self.label_uno.config(text="------------------------------", foreground='black')
        self.botonera.busqueda.config(state=NORMAL)
        self.entry.config(state=DISABLED)
        
    def get_entries(self, event):
        get_producto = self.producto_desplegables.get()
        get_proveedor = self.proveedores_desplegables.get()
        get_vencimiento = self.entry_vencimiento.get_date()
        get_tropa = self.entry_tropa.get()
        get_factura = self.entry_factura.get()
        # self.botonera.agregar.config(state=DISABLED)
        if get_producto:
            id_prod = get_producto.split("-")
            self.send_idprod = id_prod[0] ########################################3
            if get_proveedor:
                id_prov = get_proveedor.split("-")
                self.send_idprov = id_prov[0] #######################################
                if get_vencimiento:
                    self.fecha_vencimiento = get_vencimiento
                    if get_tropa:
                        self.send_tropa = get_tropa
                        if get_factura:
                            self.send_factura = get_factura
                            self.label_uno.config(text="Ya puede escanear el código de Barras", foreground='blue')
                            self.entry.config(state=NORMAL)
                            self.entry.focus_set()
                            self.entry.bind('<Return>', self.scan)

    def scan(self, event):
        barcode = str(self.entry.get())
        if barcode:
            self.result_label.config(text=f"Código de Barras escaneado:", foreground='green')
            self.result_label2.config(text=barcode, anchor="center", background='white', relief="solid")
            self.entry.delete(0, tk.END)
            # self.enable_buttons(barcode)
            self.barcode = barcode
            self.agregar_codebar()
        else:
            messagebox.showinfo("Campos vacíos", "Scanee o ingrese código")
            
    # def enable_buttons(self, barcode=None):    
    #     if barcode:
    #         self.botonera.agregar.config(state=NORMAL)    
        
    def productos_lista(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query      = "SELECT * FROM productos"
        productos  = QueriesSQLite.execute_read_query(connection, query)
        if productos:
            lista_productos = [f"{producto[0]}-{producto[1]}" for producto in productos]
            self.producto_desplegables['values'] = lista_productos     
    
    def proveedores_lista(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query      = "SELECT * FROM proveedores"
        proveedores  = QueriesSQLite.execute_read_query(connection, query)
        if proveedores:
            lista_proveedores = [f"{proveedor[0]}-{proveedor[1]}" for proveedor in proveedores]
            self.proveedores_desplegables['values'] = lista_proveedores 
        
    def agregar_codebar(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        busqueda   = "SELECT * FROM stock WHERE cod_caja = ?"
        item       = QueriesSQLite.execute_read_query(connection, busqueda, (self.barcode,))
        if item:
            messagebox.showwarning("BBDD", "Ya ha ingresado un item con el mismo código")
            self.entry.focus_set()
        else:
            self.grab_release()
            self.ingreso_form(self.send_prod, self.send_prov, self.barcode)
        
    def ingreso_form(self, producto, proveedor, codbar):
            self.ingreso_popup = tk.Toplevel()
            self.ingreso_popup.geometry("400x350")
            self.ingreso_popup.overrideredirect(True)
            self.ingreso_popup.grab_set()
            
            frame_info = ttk.Frame(self.ingreso_popup)
            frame_info.pack()
            label_info1 = ttk.Label(frame_info, text="Está ingresando el producto: ", background='white')
            label_info1.pack(side='left')
            label_info2 = ttk.Label(frame_info, text=producto, foreground='blue', background='white')
            label_info2.pack(side='left')
            label_info3 = ttk.Label(frame_info, text=" del proveedor ", background='white')
            label_info3.pack(side='left')
            label_info4 = ttk.Label(frame_info, text=proveedor, foreground='blue', background='white')
            label_info4.pack(side='left')
            
            main_frame = ttk.Frame(self.ingreso_popup)
            main_frame.pack()
            
            frame_label = ttk.Frame(main_frame)
            frame_label.pack(side='left')
            frame_entry = ttk.Frame(main_frame)
            frame_entry.pack(side="left")
            
            label_codbar1 = ttk.Label(frame_label, text="Códido de Barras escaneado --->")
            label_codbar1.pack(padx=5,pady=5)
            label_codbar2 = ttk.Label(frame_entry, text=codbar, background='grey', relief='solid', font=('Arial', 12), borderwidth=2, anchor='center')
            label_codbar2.pack(padx=5,pady=5, fill='x')
            
            peso_label = tk.Label(frame_label, text='Ingrese KG de Caja')
            peso_label.pack(fill='both', padx=5, pady=5)
            peso_label.config(height=2)
            self.peso_entry = ttk.Entry(frame_entry, justify='center', font=('Calibri',18))
            self.peso_entry.pack(fill='y', padx=5, pady=5)
            self.peso_entry.focus_set()
            # self.peso_entry.bind('<Return>', lambda event=None: self.agregar)
            self.peso_entry.bind('<Return>', self.agregar)
            
            cancel_button = ttk.Button(self.ingreso_popup, text='Agregar', command=self.cancel_input)
            cancel_button.pack(side="bottom", fill="x", padx=5, pady=5)
            
    def cancel_input(self):
        self.ingreso_popup.destroy()
        
    def agregar(self, event):
        peso = self.peso_entry.get()
        fecha_i = datetime.date.today()
        fecha_v = self.fecha_vencimiento 
        
        if fecha_v and peso:
            self.close_ingresos()
            self.validate_inputs(self.barcode, self.send_idprod, self.send_idprov, peso, self.send_tropa, fecha_i, fecha_v, self.pallet_id, self.send_factura)
            self.cargar_datos_cb()
            self.cerrar_pallet_btn.config(state=NORMAL)
            # self.botonera.agregar.config(state=DISABLED)
            self.result_label.config(text="")
            self.result_label2.config(text="")
                  
        else:
            messagebox.showwarning("Campos vacíos", "Ingrese peso")


    def close_ingresos(self):
        self.ingreso_popup.grab_release()
        self.ingreso_popup.destroy()
        self.entry.focus_set()
        self.grab_set()
            
    def validate_inputs(self, codigo, id_producto, id_proveedor, peso, tropa, fecha_i, fecha_v, id_pallet, n_factura):
        alert = 'Error: '
        alert2 = ''
        validate = {}
        if not codigo:
            alert += 'Falta Código de caja. '
            validate['codigo'] = False
        else:
            validate['codigo'] = codigo       
                
        if not id_producto:
            alert += 'Falta Producto ID. '
            validate['id_producto'] = False
        else:
            try:
                numeric_idprod = int(id_producto)
                validate['id_producto'] = id_producto 
            except:
                alert2 += "Producto ID no válido. "
                validate['id_producto'] = False 
            
        if not id_proveedor:
            alert += 'Falta Proveedor. '
            validate['id_proveedor'] = False
        else:
            try:
                numeric_idprov = int(id_proveedor)
                validate['id_proveedor'] = id_proveedor 
            except:
                alert2 += "Proveedor ID no válido. "
                validate['id_proveedor'] = False
                
        if not peso:
            alert += 'Falta Peso. '
            validate['peso'] = False
        else:
            try:
                numeric_peso = float(peso)
                validate['peso'] = peso
            except:
                alert2 += "Peso no válido. "
                validate['peso'] = False 
                
        if not tropa:
            alert += 'Falta Código de caja. '
            validate['tropa'] = False
        else:
            validate['tropa'] = tropa 
        
        if not fecha_i:
            alert += 'Falta Fecha Ingreso. '
            validate['fecha_i'] = False
        else:
            validate['fecha_i'] = fecha_i 
                
        if not fecha_v:
            alert += 'Falta Fecha Vencimiento. '
            validate['fecha_v'] = False
        else:
            validate['fecha_v'] = fecha_v
        
        if not id_pallet:
            alert += 'Falta ID Pallet. '
            validate['id_pallet'] = False
        else:
            validate['id_pallet'] = id_pallet    
        
        if not n_factura:
            alert += 'Falta N° Factura. '
            validate['n_factura'] = False
        else:
            validate['n_factura'] = n_factura   
        

        valores = list(validate.values())
        
        if False in valores:
            messagebox.showwarning("Campos inválidos", f"{alert}\n{alert2}")
        else:
            self.agregar_validado(validate, True)
        
    def agregar_validado(self, validate=None, confirm=False):
        if confirm:
            stock_tuple = tuple(validate.values())
            connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
            crear_item = """
            INSERT INTO 
                stock (cod_caja, id_producto, id_proveedor, peso, tropa, fecha_ingreso, fecha_vencimiento, id_pallet, n_factura)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            QueriesSQLite.execute_query(connection, crear_item, stock_tuple)
            self.agregar_factura(stock_tuple[8], "INGRESADO")
            
    def agregar_factura(self, n_factura, estado):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query_search = "SELECT * FROM facturas WHERE n_factura = ?"
        busqueda = QueriesSQLite.execute_read_query(connection, query_search, (n_factura,))
        if not busqueda:
            query = "INSERT INTO facturas(n_factura, estado) VALUES (?,?)"
            QueriesSQLite.execute_query(connection, query, (n_factura, estado))
            
    def center_window(self):
    # Obtener el ancho y alto de la ventana
        window_width = 350
        window_height = 400

        # Obtener el ancho y alto de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular la posición del lado superior izquierdo de la ventana para centrarla
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Configurar la geometría de la ventana para centrarla
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
            