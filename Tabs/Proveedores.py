import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from Auxiliares.sqlqueries import QueriesSQLite
from Tablas.Tablas import Proveedores_table
from Auxiliares.Botonera import Botonera
from PIL import Image, ImageTk

class Proveedores_Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.proveedores_frame = ttk.Frame(self) 
        self.proveedores_frame.pack(fill="x")
        # Etiqueta de Cuadro
        self.label = ttk.Label(self.proveedores_frame, text="Proveedor")
        self.label.pack(side="left", padx=5, pady=5)
        # Cuadro de entrada
        self.cuadroNombre=ttk.Entry(self.proveedores_frame, takefocus=True)
        self.cuadroNombre.pack(side="left", padx=5, pady=5) #Se ubica en la fila 0, columna 1  
        self.botonera = Botonera(self, self.busqueda_nombre, self.agregar_proveedor, self.eliminar_proveedor, self.modificar_proveedor)
        self.botonera.pack(fill="x",anchor="center", padx=5, pady=5)
        # Tabla Proveedores
        self.proveedores_table = Proveedores_table(self)
        self.proveedores_table.pack(fill="both", expand=True)
        self.proveedores_table.tree.bind("<Double-1>", self.on_double_click)

    def agregar_proveedor(self):
        self.formulario_proveedor(self.validar_campos)
        self.label_titulo.config(text="Agregar Proveedor")

        
    def busqueda_nombre(self):
        entry = self.cuadroNombre.get().upper()
        if entry == "":
            messagebox.showerror("Error", "Ingrese nombre de Proveedores")
        else:
            connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
            query = "SELECT * FROM proveedores"
            proveedor = QueriesSQLite.execute_read_query(connection, query)
            resultado = []
            if proveedor:
                for proveedor in proveedor:
                    if proveedor[1].find(entry) >= 0:
                        resultado.append({"ID": proveedor[0], "Nombre": proveedor[1], "Domicilio": proveedor[2], "CUIT": proveedor[3], "Mail": proveedor[4],"Telefono": proveedor[5], "CP": proveedor[6], "Provincia": proveedor[7]})
                if resultado:
                    Proveedores_PopUp(resultado)
                else:
                    messagebox.showinfo("BBDD", "Proveedor no encontrado")
    
    def validar_campos(self):
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        busqueda   = "SELECT * FROM proveedores WHERE nombre = ?"
        nombre = self.nombre_entry.get().upper()
        resultado = QueriesSQLite.execute_read_query(connection, busqueda, (nombre,))
        if not resultado:
            domicilio = self.domicilio_entry.get().upper()
            cuit = self.cuit_entry.get()
            mail = self.mail_entry.get().lower()
            telefono = self.telefono_entry.get()
            cp = self.cp_entry.get()
            provincia = self.provincia_entry.get()
            
            
            alert = 'Error: '
            alert2 = ''
            validate = {}
            if not nombre:
                alert += 'Falta Nombre. '
                validate['nombre'] = False
            else:
                validate['nombre'] = nombre      
                    
            if not domicilio:
                alert += 'Falta Domicilio. '
                validate['domicilio'] = False
            else:
                validate['domicilio'] = domicilio 
                
            if not cuit:
                alert += 'Falta CUIT. '
                validate['cuit'] = False
            else:
                try:
                    numeric_cuit = int(cuit)
                    validate['cuit'] = cuit 
                except:
                    alert2 += "CUIT no válido. "
                    validate['cuit'] = False
            
            if not mail:
                validate['mail'] = '-'
            else:
                try:
                    numeric_telefono = str(mail)
                    validate['mail'] = mail
                except:
                    alert2 += "Mail no válido. "
                    validate['mail'] = False
                    
            if not telefono:
                validate['telefono'] = '-'
            else:
                try:
                    numeric_telefono = int(telefono)
                    validate['telefono'] = telefono
                except:
                    alert2 += "Teléfono no válido. "
                    validate['telefono'] = False 
                    
            if not cp:
                validate['cp'] = '-'
            else:
                try:
                    numeric_telefono = int(cp)
                    validate['cp'] = cp
                except:
                    alert2 += "CP no válido. "
                    validate['cp'] = False 
            
            if not provincia:
                validate['provincia'] = '-'
            else:
                validate['provincia'] = provincia 

            valores = list(validate.values())
            
            if False in valores:
                messagebox.showwarning("Campos inválidos", alert + alert2)
            else:
                self.nuevo_proveedor(validate)
        else:
            messagebox.showwarning("Proveedor existente", "Ya existe un proveedor con este nombre")
        
    def nuevo_proveedor(self, validate):
        tuple_validate = tuple(validate.values())
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query = "INSERT INTO proveedores (nombre, domicilio, cuit,mail,telefono,cp,provincia) VALUES(?,?,?,?,?,?,?)"
        QueriesSQLite.execute_query(connection, query, tuple_validate)
        messagebox.showinfo("BBDD", "Datos Cargados Correctamente")
        self.proveedores_table.cargar_datos()
        self.cuadroNombre.delete(0, tk.END)
        self.ingreso_popup.destroy()
    
    def eliminar_proveedor(self):
        values = self.proveedores_table.seleccion_datos()
        
        if values:
            respuesta = messagebox.askokcancel("Eliminar",f"Eliminar: {values[0]} - {values[1]}")
            
            if respuesta:
                connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
                query = "DELETE FROM proveedores WHERE id = (?)"
                QueriesSQLite.execute_query(connection, query, (values[0],))
                messagebox.showinfo("BBDD","Datos eliminados correctamente")
                self.proveedores_table.cargar_datos()
        else:
            messagebox.showerror("Error", "Seleccione algún proveedor")
            
    def modificar_proveedor(self):
        self.values_edit = self.proveedores_table.seleccion_datos()
        if self.values_edit:
            self.formulario_proveedor(self.actualizar_proveedor)
            self.id_proveedor = self.values_edit[0]
            self.label_titulo.config(text="Modificar Proveedor")
            self.nombre_entry.insert(0,self.values_edit[1])
            self.domicilio_entry.insert(0,self.values_edit[2])
            self.cuit_entry.insert(0,self.values_edit[3])
            self.mail_entry.insert(0,self.values_edit[4])
            self.telefono_entry.insert(0,self.values_edit[5])
            self.cp_entry.insert(0,self.values_edit[6])
            self.provincia_entry.insert(0,self.values_edit[7])
                
    def actualizar_proveedor(self):
        nombre = self.nombre_entry.get()
        domicilio = self.domicilio_entry.get()
        cuit = self.cuit_entry.get()
        mail = self.mail_entry.get()
        telefono = self.telefono_entry.get()
        cp = self.cp_entry.get()
        provincia = self.provincia_entry.get()
        tuple_change = (nombre,domicilio,cuit,mail,telefono,cp,provincia,self.values_edit[0])
        mensaje = 'Aplicar los siguientes cambios:\n'
        if nombre != self.values_edit[1]:
            mensaje += f"Nuevo nombre: {nombre}\n"
        if domicilio != self.values_edit[2]:
            mensaje += f"Nuevo Domicilio: {nombre}\n"
        if cuit != self.values_edit[3]:
            mensaje += f"Nuevo CUIT: {cuit}\n"
        if mail != self.values_edit[4]:
            mensaje += f"Nuevo Mail: {mail}\n"
        if telefono != self.values_edit[5]:
            mensaje += f"Nuevo Telefono: {telefono}\n"
        if cp != self.values_edit[6]:
            mensaje += f"Nuevo CP: {cp}\n"
        if provincia != self.values_edit[7]:
            mensaje += f"Nueva Provincia: {provincia}\n"
        
        respuesta = messagebox.askokcancel("Modificar",mensaje)
            
        if respuesta: 
            connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
            query = "UPDATE proveedores SET nombre = ?, domicilio = ?, cuit = ?, mail = ?, telefono = ?, cp = ?, provincia = ?  WHERE id = ?"
            QueriesSQLite.execute_query(connection, query, tuple_change)
            self.values_edit = []
            self.proveedores_table.cargar_datos()
            self.ingreso_popup.destroy()
        else:
            self.values_edit = []
            
    def formulario_proveedor(self, command):
        self.ingreso_popup = tk.Toplevel()
        self.ingreso_popup.geometry("400x350")
        self.ingreso_popup.overrideredirect(True)
        self.ingreso_popup.grab_set()
        
        main_frame = ttk.Frame(self.ingreso_popup)
        main_frame.pack()
        self.label_titulo = ttk.Label(main_frame,text="", font=('Arial Bold',16), anchor='center')
        self.label_titulo.pack(fill='x', pady=5)
        frame_label = ttk.Frame(main_frame)
        frame_label.pack(side='left')
        frame_entry = ttk.Frame(main_frame)
        frame_entry.pack(side="left")
        
        
        label_nombre = ttk.Label(frame_label, text="Nombre: ")
        label_nombre.pack(padx=5,pady=5)
        label_domicilio = ttk.Label(frame_label, text="Domicilio: ")
        label_domicilio.pack(padx=5,pady=5)
        label_cuit = ttk.Label(frame_label, text="CUIT: ")
        label_cuit.pack(padx=5,pady=5)
        label_mail = ttk.Label(frame_label, text="Mail: ")
        label_mail.pack(padx=5,pady=5)
        label_telefono = ttk.Label(frame_label, text="Teléfono: ")
        label_telefono.pack(padx=5,pady=5)
        label_cp = ttk.Label(frame_label, text="CP: ")
        label_cp.pack(padx=5,pady=5)
        label_provincia = ttk.Label(frame_label, text="Provincia: ")
        label_provincia.pack(padx=5,pady=5)

        self.nombre_entry = ttk.Entry(frame_entry)
        self.nombre_entry.pack(fill='y', padx=5, pady=4)
        self.domicilio_entry = ttk.Entry(frame_entry)
        self.domicilio_entry.pack(fill='y', padx=5, pady=4)
        self.cuit_entry = ttk.Entry(frame_entry)
        self.cuit_entry.pack(fill='y', padx=5, pady=4)
        self.mail_entry = ttk.Entry(frame_entry)
        self.mail_entry.pack(fill='y', padx=5, pady=4)
        self.telefono_entry = ttk.Entry(frame_entry)
        self.telefono_entry.pack(fill='y', padx=5, pady=4)
        self.cp_entry = ttk.Entry(frame_entry)
        self.cp_entry.pack(fill='y', padx=5, pady=4)
        self.provincia_entry = ttk.Combobox(frame_entry,values=['Buenos Aires', 'Entre Ríos', 'Santa Fé', 'Corrientes', 'Misiones', 'Chaco', 'Formosa', 'Jujuy','Salta', 'La Rioja', 'San Juan', 'Córdoba', 'Santiago del Estero', 'Tucuman', 'Mendoza', 'San Luis', 'Catamarca', 'La Pampa', 'Chubut', 'Río Negro', 'Santa Cruz', 'Tierra del Fuego', 'Neuquen'])
        self.provincia_entry.pack(fill='y', padx=5, pady=4)
        
        add_button = ttk.Button(self.ingreso_popup, text='Agregar', command=command)
        add_button.pack(side="bottom", fill="x", padx=5, pady=5)
        cancel_button = ttk.Button(self.ingreso_popup, text='Cancelar', command=self.ingreso_popup.destroy)
        cancel_button.pack(side="bottom", fill="x", padx=5, pady=5)
        
    
    def on_double_click(self, event):
        self.cuadroNombre.delete(0, tk.END)
        selection = self.proveedores_table.seleccion_datos()
        if selection:
            self.cuadroNombre.insert(0, selection[1])
            
        
                
                
class Proveedores_PopUp(tk.Toplevel):
    def __init__(self, values):
        super().__init__()
        self.title("Resultados de Búsqueda")  
        self.resultados_tree = ttk.Treeview(self, columns=("ID", "Nombre", "Domicilio", "CUIT", "Telefono", "CP", "Provincia"))
        self.resultados_tree.heading("#0", text="ID")
        self.resultados_tree.column("#0", minwidth=0, width=0, stretch=tk.NO)
        self.resultados_tree.heading("ID", text="ID")
        self.resultados_tree.column("ID", width="20", anchor="center")
        self.resultados_tree.heading("Nombre", text="Nombre")
        self.resultados_tree.column("Nombre", width="100", anchor="center")
        self.resultados_tree.heading("Domicilio", text="Domicilio")
        self.resultados_tree.column("Domicilio", width="100", anchor="center")
        self.resultados_tree.heading("CUIT", text="CUIT")
        self.resultados_tree.column("CUIT", width="75", anchor="center")
        self.resultados_tree.heading("Telefono", text="Telefono")
        self.resultados_tree.column("Telefono", width="75", anchor="center")
        self.resultados_tree.heading("CP", text="CP")
        self.resultados_tree.column("CP", width="25", anchor="center")
        self.resultados_tree.heading("Provincia", text="Provincia")
        self.resultados_tree.column("Provincia", width="100", anchor="center")
        self.resultados_tree.pack(fill=tk.BOTH, expand=True)
        self.values = values

        self.actualizar_resultados(self.values)
        
    def actualizar_resultados(self, values):
        self.resultados_tree.delete(*self.resultados_tree.get_children())
        for value in values:
            self.resultados_tree.insert("", "end", text=value["ID"], values=(value["ID"], value["Nombre"], value["Domicilio"], value["CUIT"], value["Telefono"], value["CP"], value["Provincia"]))