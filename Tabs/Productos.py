import tkinter as tk
from tkcalendar import DateEntry
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from Tablas.Tablas import Productos_table
from Auxiliares.sqlqueries import QueriesSQLite
from PIL import Image, ImageTk
import os
from Auxiliares.Botonera import Botonera

class Productos_Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Frame de Producto entry
        self.parent = parent
        producto_frame = ttk.Frame(self)
        producto_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        nombre_label = ttk.Label(producto_frame, text="Producto")
        nombre_label.pack(side="top", anchor="w", padx=5)
        self.producto_entry = ttk.Entry(producto_frame)
        self.producto_entry.pack(side="top", anchor="w", padx=5)
        
        id_label = ttk.Label(producto_frame, text="Código")
        id_label.pack(side="top", anchor="w", padx=5)
        self.id_entry = ttk.Entry(producto_frame)
        self.id_entry.pack(side="top", anchor="w", padx=5)
        
        # Frame botonera
        botonera_frame = ttk.Frame(self)
        botonera_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        self.botonera = Botonera(botonera_frame, self.busqueda_producto, self.nuevo_producto, self.eliminar_producto, self.modificar_producto)
        self.botonera.pack(fill="x", padx=5)
        
        # Frame Tabla productos
        table_frame = ttk.Frame(self)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True,pady=10)
        self.productos_table = Productos_table(table_frame)
        self.productos_table.pack(fill="both", expand=True, padx=5)
        
        #Evento doble click en tabla 
        self.productos_table.tree.bind("<Double-1>", self.on_double_click)
        
        
        
        
    def busqueda_producto(self):
        name = self.producto_entry.get()
        codigo= self.id_entry.get()
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        lista_sql =QueriesSQLite.execute_read_query(connection,"SELECT * FROM productos")
        values=[]
        if name:
            for producto in lista_sql:
                if producto[1].find(name.upper()) >= 0:    
                    kilos = 0
                    cant_cajas = 0
                    lectura_stock = "SELECT * FROM stock where id_producto = ?"
                    items = QueriesSQLite.execute_read_query(connection, lectura_stock,(producto[0],))
                    if items:
                        for item in items:  
                            kilos += item[4] 
                            cant_cajas += 1   
                        values.append({"ID":producto[0], "Producto":producto[1], "KG": "{:.2f}".format(kilos), "Cajas":cant_cajas})
                    else:    
                        values.append({"ID":producto[0], "Producto":producto[1], "KG": "{:.2f}".format(kilos), "Cajas":cant_cajas})
            if values:
                Productos_PopUp(values)
            else:
                messagebox.showwarning("BBDD", "Producto no encontrado")
                    
        elif codigo:
            for producto in lista_sql:
                if codigo == str(producto[0]):
                    kilos = 0
                    cant_cajas = 0    
                    lectura_stock = "SELECT * FROM stock where id_producto = ?"
                    items = QueriesSQLite.execute_read_query(connection, lectura_stock,(producto[0],))
                    if items:
                        for item in items:    
                            kilos += item[4] 
                            cant_cajas += 1       
                        values.append({"ID":producto[0], "Producto":producto[1], "KG": "{:.2f}".format(kilos), "Cajas":cant_cajas})
                    else:
                        values.append({"ID":producto[0], "Producto":producto[1], "KG": 0, "Cajas":0})
            if values:
                Productos_PopUp(values)
            else:
                messagebox.showwarning("BBDD", "Código no encontrado")
        else:
            messagebox.showerror("Error", "Ingrese nombre de Producto o Código")
                    
    def nuevo_producto(self):
        producto_entry = self.producto_entry.get().upper()
        
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        if producto_entry=="":
            messagebox.showerror("Campos vacíos", "Ingrese nombre de Producto: ")
        else:
            validacion =  self.validar_datos(connection, producto_entry, 'productos')
            if validacion:
                messagebox.showinfo("BBDD", "Ya existe este producto")
            else:
                query = "INSERT INTO productos (detalle) VALUES(?)"
                QueriesSQLite.execute_query(connection, query, (producto_entry,))
                messagebox.showinfo("BBDD", "Datos Cargados Correctamente")
                self.productos_table.cargar_datos()
    
    def eliminar_producto(self):
        
        values = self.productos_table.seleccion_datos()
        
        if values:
            respuesta = messagebox.askokcancel("Eliminar",f"Eliminar: {values[0]} - {values[1]}")
            
            if respuesta:
                connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
                query = "DELETE FROM productos WHERE id = (?)"
                QueriesSQLite.execute_query(connection, query, (values[0],))
                messagebox.showinfo("BBDD","Datos eliminados correctamente")
                self.productos_table.cargar_datos()
        else:
            messagebox.showerror("Error", "Seleccione algún Producto")
                
    def modificar_producto(self):
        new_name = self.producto_entry.get().upper()
        if new_name :
            values = self.productos_table.seleccion_datos()
            tuple_change = (new_name, values[0])
            respuesta = messagebox.askokcancel("Modificar",f"Modificar: {values[0]} - {values[1]} a {new_name}")
            
            if respuesta: 
                connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
                query = "UPDATE productos SET detalle = ? WHERE id = ?"
                QueriesSQLite.execute_query(connection, query, tuple_change)
                self.productos_table.cargar_datos()
        else:
            messagebox.showerror("Campos vacíos", "No se ha ingresado ningún nombre")
            
    def on_double_click(self, event):
        selection = self.productos_table.seleccion_datos()
        Stock_PopUp(selection)                
    
    def validar_datos(self,connection, dato, tabla):
        # connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        busqueda = f"SELECT * FROM {tabla}"
        resultados = QueriesSQLite.execute_read_query(connection, busqueda)
        for resultado in resultados:
            if dato in resultado[1]:
                return resultado
                
class Productos_PopUp(tk.Toplevel):
    def __init__(self, values):
        super().__init__()
        # self.on_double_click_cb = on_double_click_cb
        self.title("Existencia de Productos")
        self.resultados_tree = ttk.Treeview(self, columns=("ID", "Producto", "Kg", "Cantidad"))
        self.resultados_tree.heading("#0", text="ID")
        self.resultados_tree.column("#0", minwidth=0, width=0, stretch=tk.NO)
        self.resultados_tree.heading("ID", text="ID")
        self.resultados_tree.column("ID", anchor="center")
        self.resultados_tree.heading("Producto", text="Producto")
        self.resultados_tree.column("Producto", anchor="center")
        self.resultados_tree.heading("Kg", text="Kg")
        self.resultados_tree.column("Kg", anchor="center")
        self.resultados_tree.heading("Cantidad", text="Cantidad cajas")
        self.resultados_tree.column("Cantidad", anchor="center")
        self.resultados_tree.pack(fill=tk.BOTH, expand=True)
        self.values = values
        self.actualizar_resultados(self.values)
        
        self.resultados_tree.bind("<Double-1>", self.on_double_click)
        
    def actualizar_resultados(self, values):
        self.resultados_tree.delete(*self.resultados_tree.get_children())
        
        for value in values:
            self.resultados_tree.insert("", "end", text=value["ID"], values=(value["ID"],value["Producto"], value["KG"], value["Cajas"]))
    
    def on_double_click(self, event):
        selection = self.seleccion_datos()
        Stock_PopUp(selection)
        
    def seleccion_datos(self):
        # Obtener ítems seleccionados en el Treeview
        selection = self.resultados_tree.selection()
        
        # Verificar si hay algún ítem seleccionado
        if selection:
            # Si hay ítems seleccionados, obtener el primer ítem seleccionado
            item = selection[0]
            
            # Obtener los valores de la fila seleccionada
            self.values = self.resultados_tree.item(item, "values")
            
            return self.values
        else:
            # Si no hay ítems seleccionados, retornar None o cualquier otro valor indicativo
            return None
           
class Stock_PopUp(tk.Toplevel):
    def __init__(self, selection):
        super().__init__()
        self.title("Inventario")
        self.codigo = selection[0]
        self.producto = selection[1]
        self.label = ttk.Label(self, text=self.producto)
        self.label.pack(anchor="center")
        self.resultados_tree = ttk.Treeview(self, columns=("ID", "Codigo_Caja", "Kilos"))
        self.resultados_tree.heading("#0", text="#")
        self.resultados_tree.column("#0", minwidth=0, width=0, stretch=tk.NO)
        self.resultados_tree.heading("ID", text="ID Ingreso")
        self.resultados_tree.column("ID", anchor="center")
        self.resultados_tree.heading("Codigo_Caja", text="Código de Caja")
        self.resultados_tree.column("Codigo_Caja", anchor="center")
        self.resultados_tree.heading("Kilos", text="Kilos Netos")
        self.resultados_tree.column("Kilos", anchor="center")
        self.resultados_tree.pack(fill=tk.BOTH, expand=True)
        self.actualizar_resultados(self.codigo)
        
    def actualizar_resultados(self, codigo):
        self.resultados_tree.delete(*self.resultados_tree.get_children())
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query = "SELECT * FROM stock"
        stock = QueriesSQLite.execute_read_query(connection, query)

        if stock:
            for item in stock:
                if codigo == str(item[2]): 
                    self.resultados_tree.insert("", "end", text=item[0], values=(item[0], item[1], item[4]))
        