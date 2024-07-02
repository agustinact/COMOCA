
import tkinter as tk
from tkinter import ttk
from tkinter import *
from Auxiliares.Reporte_Romaneo import reporte_romaneo
from Auxiliares.sqlqueries import QueriesSQLite
from tkcalendar import DateEntry
from Tablas.Tablas import Romaneos_table
from Auxiliares.Botonera import Exportar
from Auxiliares.Busqueda_Codbar import ResultadosBusquedaPopup
from tkinter import messagebox
from Auxiliares.Completar_Remito import *
import datetime

class Romaneos_Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        second_frame = tk.Frame(main_frame)
        second_frame.pack(side=tk.LEFT, fill=tk.BOTH, pady=10)
        
        self.label_factura = ttk.Label(second_frame, text="Seleccionar Factura: ")
        self.label_factura.pack(fill='x', pady=5, padx=5) 
        
        self.lista_factura = ttk.Combobox(second_frame, state="readonly")
        self.lista_factura.pack(fill='x', padx=5)
        
        # self.label_facturacion = ttk.Label(second_frame, text="Facturación a nombre de: ")
        # self.label_facturacion.pack(fill='x', pady=5, padx=5)
        
        # self.facturacion_entry = ttk.Entry(second_frame)
        # self.facturacion_entry.pack(fill='x', padx=5)
        
        # self.label_fecha = ttk.Label(second_frame, text="Seleccionar Fecha de entrega: ")
        # self.label_fecha.pack(fill='x', pady=5, padx=5)
        
        # self.calendar = DateEntry(second_frame)
        # self.calendar.pack(fill='x', padx=5)
          
        self.export_btn = ttk.Button(second_frame, text="Aplicar", command=self.aplicar)
        self.export_btn.pack(fill='x', pady=10, padx=5)
        
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True , pady=10)
        self.tabla = Romaneos_table(table_frame)
        self.tabla.pack(fill='both', expand=True, padx=5) 
        
        self.borrar_btn = ttk.Button(second_frame, text="Borrar datos", command=self.tabla.limpiar_tabla)
        self.borrar_btn.pack(fill='x', padx=5)
        
        self.exportar_btn = Exportar(second_frame, self.exportar)
        self.exportar_btn.pack(pady=5)
        self.exportar_btn.export.config(state=DISABLED)
        
        
        self.listar_facturas()
        
    def listar_facturas(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query = "SELECT n_factura FROM facturas "
        facturas = QueriesSQLite.execute_read_query(connection, query)
        
        if facturas:
            # facturas = [f"{proveedor[0]}-{proveedor[1]}" for proveedor in proveedores]
            self.lista_factura['values'] = facturas
            
    
    def aplicar(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query_salidas = "SELECT * FROM salidas WHERE f_proveedor = ?"
        query_stock   = "SELECT * FROM stock WHERE n_factura = ?"
        query_clientes = "SELECT * FROM clientes WHERE nombre = ?"
        get_factura = self.lista_factura.get()
        lista_romaneo = []
        print("n_factura", get_factura)
        
        if get_factura:
            lista_salidas = QueriesSQLite.execute_read_query(connection, query_salidas, (get_factura,))
            lista_stock = QueriesSQLite.execute_read_query(connection, query_stock, (get_factura,))
            print("lista_salidas", lista_salidas)
            # get_date = self.calendar.get_date()
            # if get_date:
                
                # filtrados = [tupla for tupla in lista_salidas if tupla[7] == str(get_date)]
            if lista_salidas:    
                for item in lista_salidas:
                    producto = item[3]
                    cliente  = item[4]                    
                    peso     = item[5]
                    proveedor = item[8]
                    encontrado = False
                    for datos in lista_romaneo:
                        if producto == datos[4] and cliente == datos[0]:
                            datos[5] += peso
                            encontrado = True
                            break
                            
                    if not encontrado:
                    # Si no se encontró una tupla existente con el mismo producto y tropa, crea una nueva tupla
                        facturacion = QueriesSQLite.execute_read_query(connection, query_clientes, (cliente,))
                        nueva_tupla = [item[4], facturacion[0][2], proveedor, item[7], producto, peso, 0, 0]
                        lista_romaneo.append(nueva_tupla)
            
            if lista_stock:        
                for item in lista_stock:
                    producto = QueriesSQLite.execute_read_query(connection, "SELECT detalle FROM productos WHERE id = ?", (item[2],))
                    proveedor = QueriesSQLite.execute_read_query(connection, "SELECT nombre FROM proveedores WHERE id = ?", (item[3],))
                    estado  = 'EN STOCK'                    
                    peso     = item[4]
                    encontrado = False
                    for datos in lista_romaneo:
                        if producto == datos[4] and estado == 'EN STOCK':
                            datos[5] += peso
                            encontrado = True
                            break
                            
                    if not encontrado:
                    # Si no se encontró una tupla existente con el mismo producto y tropa, crea una nueva tupla
                        facturacion = QueriesSQLite.execute_read_query(connection, query_clientes, (cliente,))
                        nueva_tupla = [estado, '-', proveedor[0][0], item[6], producto[0][0], peso, 0, 0]
                        lista_romaneo.append(nueva_tupla)

        
        self.tabla.cargar_datos(lista_romaneo)
        if len(self.tabla.tree.get_children()) > 0:
            self.exportar_btn.export.config(state=NORMAL)
        
    def exportar(self):
        items = self.tabla.tree.get_children()
        lista_valores =[]
        if items:
            for item in items:
                valores = self.tabla.tree.item(item, "values")
                lista_valores.append(valores)
            respuesta   = messagebox.askokcancel("Reporte",f"Desea generar reporte?")

            if respuesta:
                reporte_romaneo(lista_valores) 
            