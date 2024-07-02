from datetime import datetime
from hmac import new
from multiprocessing import connection
from operator import itemgetter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from Auxiliares.sqlqueries import QueriesSQLite
from Auxiliares.Filtros import Filtros_Ingresos, Filtros_Salidas


class Proveedores_table(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.tree = ttk.Treeview(self, selectmode='browse')
        self.tree["columns"] = ("ID","Nombre","Domicilio", "CUIT", "Mail","Telefono", "CP", "Provincia")
        self.tree.heading("#0", text="#")
        self.tree.column("#0", minwidth=0, width=0, stretch=tk.NO)
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width="10", anchor="center")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.column("Nombre", width="100", anchor="center")
        self.tree.heading("Domicilio", text="Domicilio")
        self.tree.column("Domicilio", width="100", anchor="center")
        self.tree.heading("CUIT", text="CUIT")
        self.tree.column("CUIT", width="45", anchor="center")
        self.tree.heading("Mail", text="Mail")
        self.tree.column("Mail", width="110", anchor="center")
        self.tree.heading("Telefono", text="Telefono")
        self.tree.column("Telefono", width="45", anchor="center")
        self.tree.heading("CP", text="CP")
        self.tree.column("CP", width="25", anchor="center")
        self.tree.heading("Provincia", text="Provincia")
        self.tree.column("Provincia", width="25", anchor="center")
        self.title = Label(self, text="Tabla Proveedores")     
        self.title.pack(anchor="center")
        # self.tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        
        # Asignar evento de doble clic
        self.cargar_datos()
        
    def cargar_datos(self):
        # Limpiar árbol
        self.tree.delete(*self.tree.get_children())

        # Consultar datos de la tabla SQL
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        lectura = "SELECT * FROM proveedores"
        filas = QueriesSQLite.execute_read_query(connection, lectura)
        
        # Insertar datos en Treeview
        for fila in filas:
            self.tree.insert("", "end", text=fila[0], values=(fila[0],fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7]))    
    
    def seleccion_datos(self):
        # Obtener ítems seleccionados en el Treeview
        selection = self.tree.selection()
        
        # Verificar si hay algún ítem seleccionado
        if selection:
            # Si hay ítems seleccionados, obtener el primer ítem seleccionado
            item = selection[0]
            
            # Obtener los valores de la fila seleccionada
            self.values = self.tree.item(item, "values")
            
            return self.values
        else:
            # Si no hay ítems seleccionados, retornar None o cualquier otro valor indicativo
            return None        
        
class Productos_table(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.tree = ttk.Treeview(self, selectmode='browse')
        self.tree["columns"] = ("ID","Producto","Kg","Cantidad")
        self.tree.heading("#0", text="#")
        self.tree.column("#0", minwidth=0, width=0, stretch=tk.NO)
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width="10", anchor="center")
        self.tree.heading("Producto", text="Producto")
        self.tree.column("Producto", width="100", anchor="center")
        self.tree.heading("Kg", text="Kg")
        self.tree.column("Kg", width="15", anchor="center")
        self.tree.heading("Cantidad", text="Cantidad cajas")
        self.tree.column("Cantidad", width="50", anchor="center")
        self.title = Label(self, text="Tabla Productos")     
        self.title.pack(anchor="center")
          
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        yscroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        yscroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=yscroll.set) 
        
        
        
        self.cargar_datos()
        
    def cargar_datos(self):
        # Limpiar árbol
        self.tree.delete(*self.tree.get_children())

        # Consultar datos de la tabla SQL
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        lectura_productos = "SELECT * FROM productos"
        filas_productos = QueriesSQLite.execute_read_query(connection, lectura_productos)
        
        # Insertar datos en Treeview
        for fila in filas_productos:
            kilos=0
            cant_cajas=0
            lectura_stock = "SELECT * FROM stock WHERE id_producto = ?"
            items = QueriesSQLite.execute_read_query(connection, lectura_stock,(fila[0],))
            for item in items:    
                kilos += item[4] 
                cant_cajas += 1
            self.tree.insert("", "end", text=fila[0], values=(fila[0],fila[1], "{:.2f}".format(kilos), cant_cajas))
    
    def seleccion_datos(self):
        # Obtener ítems seleccionados en el Treeview
        selection = self.tree.selection()
        
        # Verificar si hay algún ítem seleccionado
        if selection:
            # Si hay ítems seleccionados, obtener el primer ítem seleccionado
            item = selection[0]
            
            # Obtener los valores de la fila seleccionada
            self.values = self.tree.item(item, "values")
            
            return self.values
        else:
            # Si no hay ítems seleccionados, retornar None o cualquier otro valor indicativo
            return None
        
class Stock_table(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.tree = ttk.Treeview(self, selectmode='browse')
        self.tree["columns"] = ("ID","Codigo_Caja","Producto","Proveedor","Kg", "Tropa", "Fecha_ingreso", "Vencimiento", "ID_Pallet", "Factura")
        self.tree.heading("#0", text="#")
        self.tree.column("#0", minwidth=0, width=0, stretch=tk.NO)
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width="10", anchor="center")
        self.tree.heading("Codigo_Caja", text="Código de Caja")
        self.tree.column("Codigo_Caja", width="70", anchor="center")
        self.tree.heading("Producto", text="Producto")
        self.tree.column("Producto", width="70", anchor="center")
        self.tree.heading("Proveedor", text="Proveedor")
        self.tree.column("Proveedor", width="100", anchor="center")
        self.tree.heading("Kg", text="Kg")
        self.tree.column("Kg", width="15", anchor="center")
        self.tree.heading("Tropa", text="Tropa")
        self.tree.column("Tropa", width="25", anchor="center")
        self.tree.heading("Fecha_ingreso", text="Fecha de ingreso")
        self.tree.column("Fecha_ingreso", width="50", anchor="center")
        self.tree.heading("Vencimiento", text="Fecha de vencimiento")
        self.tree.column("Vencimiento", width="50", anchor="center")
        self.tree.heading("ID_Pallet", text="ID Pallet")
        self.tree.column("ID_Pallet", width="25", anchor="center")
        self.tree.heading("Factura", text="N° Facturas")
        self.tree.column("Factura", width="50", anchor="center")
        
        self.label_filtros = ttk.Label(self, text="")
        self.label_filtros.pack(fill='x', pady=5)
        
        self.filtros = Filtros_Ingresos(self, self.filtro_productos, self.filtro_proveedores, self.filtro_fechas, self.limpiar_filtros, self.filtro_pallet, self.filtro_factura)
        self.filtros.pack(fill='x')
    
        self.title = Label(self, text="Tabla Inventario")     
        self.title.pack(fill='x')

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        yscroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        yscroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=yscroll.set) 

        self.cargar_datos()
        self.lista_pallets()
        self.lista_facturas()
        
    def cargar_datos(self, tipo_filtro=None, ids=[]):
        # Limpiar árbol
        self.tree.delete(*self.tree.get_children())

        # Consultar datos de la tabla SQL
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        if tipo_filtro == 'Producto':
            lectura_stock = "SELECT * FROM stock where id_producto = ?"
            for id in ids:
                item_ingresos = QueriesSQLite.execute_read_query(connection, lectura_stock, (id,))
                print("item procesos: ",item_ingresos)
                for item in item_ingresos:
                    proveedores_query = "SELECT nombre FROM proveedores WHERE id = ?"
                    proveedor = QueriesSQLite.execute_read_query(connection, proveedores_query, (item[3],))
                    producto_query = "SELECT detalle FROM productos WHERE id = ?"
                    producto = QueriesSQLite.execute_read_query(connection, producto_query, (item[2],) )
                    self.tree.insert("", "end", text=item[0], values=(item[0],item[1], producto[0][0], proveedor, "{:.2f}".format(item[4]), item[5], item[6], item[7], item[8], item[9]))
        
        elif tipo_filtro == 'Proveedor':
            lectura_stock = "SELECT * FROM stock where id_proveedor = ?"
            for id in ids:
                item_ingresos = QueriesSQLite.execute_read_query(connection, lectura_stock, (id,))
                for item in item_ingresos:
                        proveedores_query = "SELECT nombre FROM proveedores WHERE id = ?"
                        proveedor = QueriesSQLite.execute_read_query(connection, proveedores_query, (item[3],))
                        producto_query = "SELECT detalle FROM productos WHERE id = ?"
                        producto = QueriesSQLite.execute_read_query(connection, producto_query, (item[2],) )
                        self.tree.insert("", "end", text=item[0], values=(item[0],item[1], producto[0][0], proveedor, "{:.2f}".format(item[4]), item[5], item[6], item[7], item[8], item[9]))
        
        elif tipo_filtro == 'Pallet':
            lectura_stock = "SELECT * FROM stock where id = ?"
            for id in ids:
                item_ingresos = QueriesSQLite.execute_read_query(connection, lectura_stock, (id,))
                for item in item_ingresos:
                        proveedores_query = "SELECT nombre FROM proveedores WHERE id = ?"
                        proveedor = QueriesSQLite.execute_read_query(connection, proveedores_query, (item[3],))
                        producto_query = "SELECT detalle FROM productos WHERE id = ?"
                        producto = QueriesSQLite.execute_read_query(connection, producto_query, (item[2],) )
                        self.tree.insert("", "end", text=item[0], values=(item[0],item[1], producto[0][0], proveedor, "{:.2f}".format(item[4]), item[5], item[6], item[7], item[8], item[9]))
        
        elif tipo_filtro == 'Factura':
            lectura_stock = "SELECT * FROM stock where id = ?"
            for id in ids:
                item_ingresos = QueriesSQLite.execute_read_query(connection, lectura_stock, (id,))
                for item in item_ingresos:
                        proveedores_query = "SELECT nombre FROM proveedores WHERE id = ?"
                        proveedor = QueriesSQLite.execute_read_query(connection, proveedores_query, (item[3],))
                        producto_query = "SELECT detalle FROM productos WHERE id = ?"
                        producto = QueriesSQLite.execute_read_query(connection, producto_query, (item[2],) )
                        self.tree.insert("", "end", text=item[0], values=(item[0],item[1], producto[0][0], proveedor, "{:.2f}".format(item[4]), item[5], item[6], item[7], item[8], item[9]))
        
        else:
            lectura_stock = "SELECT * FROM stock"
            item_ingresos = QueriesSQLite.execute_read_query(connection, lectura_stock)
            # Insertar datos en Treeview
            if item_ingresos:
                for item in item_ingresos:
                    proveedores_query = "SELECT nombre FROM proveedores WHERE id = ?"
                    proveedor = QueriesSQLite.execute_read_query(connection, proveedores_query, (item[3],))
                    producto_query = "SELECT detalle FROM productos WHERE id = ?"
                    producto = QueriesSQLite.execute_read_query(connection, producto_query, (item[2],) )
                    self.tree.insert("", "end", text=item[0], values=(item[0],item[1], producto[0][0], proveedor, "{:.2f}".format(item[4]), item[5], item[6], item[7], item[8], item[9]))
    
    def seleccion_datos(self):
        # Obtener ítems seleccionados en el Treeview
        selection = self.tree.selection()
        
        # Verificar si hay algún ítem seleccionado
        if selection:
            # Si hay ítems seleccionados, obtener el primer ítem seleccionado
            item = selection[0]
            
            # Obtener los valores de la fila seleccionada
            self.values = self.tree.item(item, "values")
            
            return self.values
        else:
            # Si no hay ítems seleccionados, retornar None o cualquier otro valor indicativo
            return None
        
    def filtro_factura(self):
        get_factura = self.filtros.factura_list.get().upper()
        connection = QueriesSQLite.create_connection('nuevaDB.sqlite')
        query = "SELECT * FROM stock"
        lista_facturas = QueriesSQLite.execute_read_query(connection, query)
        ids = []
        print("filtro facturas")
        if lista_facturas:
            print("lista_facturas", lista_facturas)
            for factura in lista_facturas:
                if factura[9] == get_factura:
                    ids.append(factura[0])
        if ids:
            self.cargar_datos('Factura', ids)
            print("ids fact", ids)
            self.label_filtros.config(text="* Filtros Activos: Facturas filtradas *", foreground='blue')    
    
    def filtro_productos(self):
        get_producto = self.filtros.producto_entry.get().upper()
        connection = QueriesSQLite.create_connection('nuevaDB.sqlite')
        query = "SELECT * FROM productos"
        lista_productos = QueriesSQLite.execute_read_query(connection, query)
        ids = []
        if get_producto:
            for producto in lista_productos:
                if producto[1].find(get_producto) >= 0:
                    ids.append(producto[0])
        if ids:
            self.cargar_datos('Producto', ids)
            self.label_filtros.config(text="* Filtros Activos: Producto filtrado *", foreground='blue')
        
        
    def filtro_proveedores(self):
        get_proveedores = self.filtros.proveedor_entry.get().upper()
        connection = QueriesSQLite.create_connection('nuevaDB.sqlite')
        query = "SELECT * FROM proveedores"
        lista_proveedores = QueriesSQLite.execute_read_query(connection, query)
        ids = []
        if get_proveedores:
            for proveedor in lista_proveedores:
                if proveedor[1].find(get_proveedores) >= 0:
                    ids.append(proveedor[0])
        if ids:
            self.cargar_datos('Proveedor', ids)
            self.label_filtros.config(text="* Filtros Activos: Proveedor filtrado *", foreground='blue')
            
    def filtro_pallet(self):
        get_pallet = self.filtros.pallet_list.get().upper()
        connection = QueriesSQLite.create_connection('nuevaDB.sqlite')
        query = "SELECT * FROM stock"
        lista_pallets = QueriesSQLite.execute_read_query(connection, query)
        ids = []
        if lista_pallets:
            for pallet in lista_pallets:
                if pallet[8].find(get_pallet) >= 0:
                    ids.append(pallet[0])
        if ids:
            self.cargar_datos('Pallet', ids)
            self.label_filtros.config(text="* Filtros Activos: Pallets filtrados *", foreground='blue')
            
    def limpiar_filtros(self):
        self.cargar_datos()
        self.label_filtros.config(text="")
        
    def filtro_fechas(self):
        # Obtener las fechas de inicio y fin desde los widgets de entrada
        start_date = self.filtros.fechai_entry.get_date()
        end_date = self.filtros.fechaf_entry.get_date()
        values = []
        
        for item in self.tree.get_children():
            date_str = self.tree.item(item, 'values')[6]
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            if start_date <= date and date <= end_date:
                values.append(self.tree.item(item, 'values'))
        
        if values:
            self.tree.delete(*self.tree.get_children())
        
            for item in values:
                self.tree.insert("", "end", text=item[0], values=(item[0],item[1], item[2], item[3], "{:.2f}".format(float(item[4])), item[5], item[6], item[7], item[8], item[9]))
            
            self.label_filtros.config(text="* Filtros Activos: Rango de Fechas activo *", foreground='blue')
            
    def lista_pallets(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query      = "SELECT DISTINCT id_pallet FROM stock"
        pallets  = QueriesSQLite.execute_read_query(connection, query)
        if pallets:
            lista_pallets = [pallet[0] for pallet in pallets]
            self.filtros.pallet_list['values'] = lista_pallets
            
    def lista_facturas(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query      = "SELECT DISTINCT n_factura FROM stock"
        facturas  = QueriesSQLite.execute_read_query(connection, query)
        if facturas:
            lista_facturas = [factura[0] for factura in facturas]
            self.filtros.factura_list['values'] = lista_facturas
        
class Salidas_table(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.tree = ttk.Treeview(self, selectmode='browse')
        self.tree["columns"] = ("ID","Remito","Codigo_Caja","Producto","Cliente","Kg","Tropa","Fecha_egreso","ID_Pallet")
        self.tree.heading("#0", text="#")
        self.tree.column("#0", minwidth=0, width=0, stretch=tk.NO)
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width="10", anchor="center")
        self.tree.heading("Remito", text="N° Remito")
        self.tree.column("Remito", width="100", anchor="center")
        self.tree.heading("Codigo_Caja", text="Código de Caja")
        self.tree.column("Codigo_Caja", width="100", anchor="center")
        self.tree.heading("Producto", text="Producto")
        self.tree.column("Producto", width="100", anchor="center")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.column("Cliente", width="100", anchor="center")
        self.tree.heading("Kg", text="Kg")
        self.tree.column("Kg", width="15", anchor="center")
        self.tree.heading("Tropa", text="Tropa")
        self.tree.column("Tropa", width="25", anchor="center")
        self.tree.heading("Fecha_egreso", text="Fecha de Salida")
        self.tree.column("Fecha_egreso", width="50", anchor="center")
        self.tree.heading("ID_Pallet", text="ID Pallet")
        self.tree.column("ID_Pallet", width="25", anchor="center")
        
        self.label_filtros = ttk.Label(self, text="")
        self.label_filtros.pack(fill='x', pady=5)
        
        self.filtros = Filtros_Salidas(self, self.filtro_remito, self.filtro_productos, self.filtro_clientes, self.filtro_fechas, self.limpiar_filtros, self.filtro_pallet)
        self.filtros.pack(fill='x')
        
        self.title = Label(self, text="Tabla Salidas")     
        self.title.pack(fill='x', pady=5)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        yscroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        yscroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=yscroll.set) 

        self.cargar_datos()
        self.lista_remitos()
        self.lista_pallets()
        
    def cargar_datos(self, tipo_filtro=None, ids=[]):
        # Limpiar árbol
        self.tree.delete(*self.tree.get_children())

        # Consultar datos de la tabla SQL
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        if tipo_filtro == 'Producto':
            lectura_stock = "SELECT * FROM salidas WHERE producto = ?"
            for id in ids:
                item_salidas = QueriesSQLite.execute_read_query(connection, lectura_stock, (id,))
                self.insertar_valores(item_salidas)
        
        elif tipo_filtro == 'Clientes':
            lectura_stock = "SELECT * FROM salidas WHERE cliente = ?"
            for id in ids:
                item_salidas = QueriesSQLite.execute_read_query(connection, lectura_stock, (id,))
                self.insertar_valores(item_salidas)
                
        elif tipo_filtro == 'Pallet':
            lectura_stock = "SELECT * FROM salidas WHERE id = ?"
            for id in ids:
                item_salidas = QueriesSQLite.execute_read_query(connection, lectura_stock, (id,))
                self.insertar_valores(item_salidas)
                
        else:
            lectura_salidas = "SELECT * FROM salidas"
            item_salidas = QueriesSQLite.execute_read_query(connection, lectura_salidas)
            # Insertar datos en Treeview
            if item_salidas:
                self.insertar_valores(item_salidas)
    
    def seleccion_datos(self):
        # Obtener ítems seleccionados en el Treeview
        selection = self.tree.selection()
        
        # Verificar si hay algún ítem seleccionado
        if selection:
            # Si hay ítems seleccionados, obtener el primer ítem seleccionado
            item = selection[0]
            
            # Obtener los valores de la fila seleccionada
            self.values = self.tree.item(item, "values")
            
            return self.values
        else:
            # Si no hay ítems seleccionados, retornar None o cualquier otro valor indicativo
            return None
        
    def lista_remitos(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query      = "SELECT * FROM remitos"
        remitos  = QueriesSQLite.execute_read_query(connection, query)
        if remitos:
            lista_remitos = [remito[1] for remito in remitos]
            self.filtros.remito_list['values'] = lista_remitos
            
    def lista_pallets(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query      = "SELECT DISTINCT id_pallet FROM salidas"
        pallets  = QueriesSQLite.execute_read_query(connection, query)
        print("pallets salidas", pallets)
        if pallets:
            lista_pallets = [pallet[0] for pallet in pallets]
            self.filtros.pallet_list['values'] = lista_pallets
        
    def filtro_remito(self):
        get_remito = self.filtros.remito_list.get()
        if get_remito:
            self.tree.delete(*self.tree.get_children())
            connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
            query = "SELECT * FROM salidas WHERE id_remito = ?"
            lista_remitos = QueriesSQLite.execute_read_query(connection, query, (get_remito,))
            self.insertar_valores(lista_remitos)
            self.label_filtros.config(text="* Filtros Activos: Remito filtrado *", foreground='blue')
            
    def filtro_productos(self):
        get_producto = self.filtros.producto_entry.get().upper()
        ids = []
 
        if get_producto:
            connection = QueriesSQLite.create_connection('nuevaDB.sqlite')
            query = "SELECT * FROM productos"
            lista_productos = QueriesSQLite.execute_read_query(connection, query)
            for producto in lista_productos:
                if producto[1].find(get_producto) >= 0:
                    ids.append(producto[1])
        if ids:
            self.cargar_datos('Producto', ids)
            self.label_filtros.config(text="* Filtros Activos: Producto filtrado *", foreground='blue')
        
    def filtro_clientes(self):
        get_clientes = self.filtros.cliente_entry.get().upper()
        connection = QueriesSQLite.create_connection('nuevaDB.sqlite')
        query = "SELECT * FROM clientes"
        lista_clientes = QueriesSQLite.execute_read_query(connection, query)
        ids = []
        if get_clientes:
            for cliente in lista_clientes:
                if cliente[1].find(get_clientes) >= 0:
                    ids.append(cliente[1])
        if ids:
            self.cargar_datos('Cliente', ids)
            self.label_filtros.config(text="* Filtros Activos: Cliente filtrado *", foreground='blue')
            
    def filtro_pallet(self):
        get_pallet = self.filtros.pallet_list.get().upper()
        connection = QueriesSQLite.create_connection('nuevaDB.sqlite')
        query = "SELECT * FROM salidas"
        lista_pallets = QueriesSQLite.execute_read_query(connection, query)
        ids = []
        if lista_pallets:
            for pallet in lista_pallets:
                if pallet[9].find(get_pallet) >= 0:
                    ids.append(pallet[0])
        if ids:
            self.cargar_datos('Pallet', ids)
            self.label_filtros.config(text="* Filtros Activos: Pallets filtrados *", foreground='blue')
        
    def filtro_fechas(self):
        # Obtener las fechas de inicio y fin desde los widgets de entrada
        start_date = self.filtros.fechai_entry.get_date()
        end_date = self.filtros.fechaf_entry.get_date()
        values = []
        
        for item in self.tree.get_children():
            date_str = self.tree.item(item, 'values')[7]
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            if start_date <= date and date <= end_date:
                values.append(self.tree.item(item, 'values'))
        
        if values:
            self.tree.delete(*self.tree.get_children())
        
            self.insertar_valores(values)
            
            self.label_filtros.config(text="* Filtros Activos: Rango de Fechas activo *", foreground='blue')
            
    def limpiar_filtros(self):
        self.cargar_datos()
        self.label_filtros.config(text="")
        
    def insertar_valores(self, lista_valores):
        for item in lista_valores:
                self.tree.insert("", "end", text=item[0], values=(item[0],item[1], item[2], item[3],item[4], "{:.2f}".format(float(item[5])), item[6], item[7], item[9]))
        
class Clientes_Table(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.tree = ttk.Treeview(self, selectmode='browse')
        self.tree["columns"] = ("ID","Nombre","Facturacion","Domicilio", "CUIT", "Mail","Telefono", "CP", "Provincia")
        self.tree.heading("#0", text="#")
        self.tree.column("#0", minwidth=0, width=0, stretch=tk.NO)
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width="10", anchor="center")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.column("Nombre", width="100", anchor="center")
        self.tree.heading("Facturacion", text="Facturación")
        self.tree.column("Facturacion", width="100", anchor="center")
        self.tree.heading("Domicilio", text="Domicilio")
        self.tree.column("Domicilio", width="100", anchor="center")
        self.tree.heading("CUIT", text="CUIT")
        self.tree.column("CUIT", width="45", anchor="center")
        self.tree.heading("Mail", text="Mail")
        self.tree.column("Mail", width="110", anchor="center")
        self.tree.heading("Telefono", text="Telefono")
        self.tree.column("Telefono", width="45", anchor="center")
        self.tree.heading("CP", text="CP")
        self.tree.column("CP", width="25", anchor="center")
        self.tree.heading("Provincia", text="Provincia")
        self.tree.column("Provincia", width="25", anchor="center")
        self.title = Label(self, text="Tabla Clientes")     
        self.title.pack(anchor="center")
        # self.tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        
        # Asignar evento de doble clic
        self.cargar_datos()
        
    def cargar_datos(self):
        # Limpiar árbol
        self.tree.delete(*self.tree.get_children())

        # Consultar datos de la tabla SQL
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        lectura = "SELECT * FROM clientes"
        filas = QueriesSQLite.execute_read_query(connection, lectura)
        
        # Insertar datos en Treeview
        for fila in filas:
            self.tree.insert("", "end", text=fila[0], values=(fila[0],fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8]))
            
    
    def seleccion_datos(self):
        # Obtener ítems seleccionados en el Treeview
        selection = self.tree.selection()
        
        # Verificar si hay algún ítem seleccionado
        if selection:
            # Si hay ítems seleccionados, obtener el primer ítem seleccionado
            item = selection[0]
            
            # Obtener los valores de la fila seleccionada
            self.values = self.tree.item(item, "values")
            
            return self.values
        else:
            # Si no hay ítems seleccionados, retornar None o cualquier otro valor indicativo
            return None   
        

class Romaneos_table(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.tree = ttk.Treeview(self, selectmode='browse')
        self.tree["columns"] = ("Cliente","Facturacion","Proveedor","Fecha","Producto","Kg","Precio","Total")
        self.tree.heading("#0", text="#")
        self.tree.column("#0", minwidth=0, width=0, stretch=tk.NO)
        self.tree.heading("Cliente", text="Cliente")
        self.tree.column("Cliente", width="100", anchor="center")
        self.tree.heading("Facturacion", text="Facturacion")
        self.tree.column("Facturacion", width="70", anchor="center")
        self.tree.heading("Proveedor", text="Proveedor")
        self.tree.column("Proveedor", width="100", anchor="center")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.column("Fecha", width="50", anchor="center")
        self.tree.heading("Producto", text="Producto")
        self.tree.column("Producto", width="100", anchor="center")
        self.tree.heading("Kg", text="Kg")
        self.tree.column("Kg", width="20", anchor="center")
        self.tree.heading("Precio", text="Precio x kg")
        self.tree.column("Precio", width="50", anchor="center")
        self.tree.heading("Total", text="Total")
        self.tree.column("Total", width="50", anchor="center")
        self.title = Label(self, text="Romaneos")     
        self.title.pack(anchor="center")
          
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        yscroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        yscroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=yscroll.set)         
        
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # self.cargar_datos()
        
    def cargar_datos(self, tupla_romaneo):
        # Limpiar árbol
        # self.limpiar_tabla()
        
        # Insertar datos en Treeview
        if tupla_romaneo:
            
            for fila in tupla_romaneo:
                peso = fila[5]
                precio = fila[6]
                total = peso * precio
                self.tree.insert("", "end", text=fila[0], values=(fila[0],fila[1],fila[2],fila[3],fila[4],"{:.2f}".format(peso),"{:.2f}".format(precio), "{:.2f}".format(total)))
    
    def seleccion_datos(self):
        # Obtener ítems seleccionados en el Treeview
        selection = self.tree.selection()
        
        # Verificar si hay algún ítem seleccionado
        if selection:
            # Si hay ítems seleccionados, obtener el primer ítem seleccionado
            item = selection[0]
            
            # Obtener los valores de la fila seleccionada
            self.values = self.tree.item(item, "values")
            
            return self.values
        else:
            # Si no hay ítems seleccionados, retornar None o cualquier otro valor indicativo
            return None
    
    def on_item_double_click(self, event):
        selected_item = self.tree.selection()[0]  # Obtener el elemento seleccionado
        values = self.tree.item(selected_item, 'values')
        self.popup_edit(selected_item, values)

    def popup_edit(self, item, values):
        # Crear ventana emergente
        popup = tk.Toplevel()
        popup.grab_set()
        popup.title("Editar Precio")

        tk.Label(popup, text=values[4]).pack(padx=5, pady=5)
        
        tk.Label(popup, text="Precio x kg").pack(padx=5, pady=5)
        precio_entry = tk.Entry(popup)
        precio_entry.pack(padx=5, pady=5)



        def save_changes():
            new_precio = float(precio_entry.get())
            new_values = list(values)
            new_values[6] = "{:.2f}".format(new_precio)
            new_total = new_precio * float(new_values[5])
            new_values[7] = "{:.2f}".format(new_total)
            self.tree.item(item, values=tuple(new_values))
            popup.destroy()

        save_button = ttk.Button(popup, text="Guardar", command=save_changes)
        save_button.pack(padx=5, pady=5)

        cancel_button = ttk.Button(popup, text="Cancelar", command=popup.destroy)
        cancel_button.pack(padx=5, pady=5)
        
    def limpiar_tabla(self):
        self.tree.delete(*self.tree.get_children())