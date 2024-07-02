import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Auxiliares.sqlqueries import QueriesSQLite
from Tablas.Tablas import Clientes_Table
from Auxiliares.Botonera import Botonera

class Clientes_Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario del frame de clientes."""
        self.clientes_frame = tk.Frame(self)
        self.clientes_frame.pack(fill="x")

        # Etiqueta de Cuadro
        self.label = ttk.Label(self.clientes_frame, text="Cliente")
        self.label.pack(side="left", padx=5, pady=5)

        # Cuadro de entrada
        self.cuadroNombre = ttk.Entry(self.clientes_frame, takefocus=True)
        self.cuadroNombre.pack(side="left", padx=5, pady=5)

        # Botonera
        self.botonera = Botonera(
            self, self.busqueda_nombre, self.agregar_cliente, 
            self.eliminar_cliente, self.modificar_cliente
        )
        self.botonera.pack(fill="x", anchor="center", padx=5, pady=5)

        # Tabla Clientes
        self.clientes_table = Clientes_Table(self)
        self.clientes_table.pack(fill="both", expand=True)
        self.clientes_table.tree.bind("<Double-1>", self.on_double_click)

    def agregar_cliente(self):
        """Abre el formulario para agregar un cliente."""
        self.formulario_cliente(self.validar_campos)
        self.label_titulo.config(text="Agregar Cliente")

    def busqueda_nombre(self):
        """Busca clientes por nombre en la base de datos."""
        entry = self.cuadroNombre.get().upper()
        if not entry:
            messagebox.showerror("Error", "Ingrese nombre de Clientes")
            return

        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query = "SELECT * FROM clientes"
        clientes = QueriesSQLite.execute_read_query(connection, query)
        resultado = [self.cliente_dict(cliente) for cliente in clientes if cliente[1].find(entry) >= 0]

        if resultado:
            Clientes_PopUp(resultado)
        else:
            messagebox.showinfo("BBDD", "Cliente no encontrado")

    @staticmethod
    def cliente_dict(cliente):
        """Convierte una tupla de cliente a un diccionario."""
        return {
            "ID": cliente[0], "Nombre": cliente[1], "Facturacion": cliente[2],
            "Domicilio": cliente[3], "CUIT": cliente[4], "Mail": cliente[5],
            "Telefono": cliente[6], "CP": cliente[7], "Provincia": cliente[8]
        }

    def validar_campos(self):
        """Valida los campos del formulario de cliente."""
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        busqueda = "SELECT * FROM clientes WHERE nombre = ?"
        nombre = self.nombre_entry.get().upper()
        resultado = QueriesSQLite.execute_read_query(connection, busqueda, (nombre,))

        if not resultado:
            validate = self.obtener_datos_formulario()
            if False in validate.values():
                messagebox.showwarning("Campos inválidos", self.alertas(validate))
            else:
                self.nuevo_cliente(validate)
        else:
            messagebox.showwarning("Cliente existente", "Ya existe un cliente con este nombre")

    def obtener_datos_formulario(self):
        """Obtiene y valida los datos del formulario."""
        validate = {}
        validate['nombre'] = self.nombre_entry.get().upper() or self.alert('Falta Nombre')
        validate['facturacion'] = self.facturacion_entry.get() or self.alert('Falta Facturación')
        validate['domicilio'] = self.domicilio_entry.get().upper() or self.alert('Falta Domicilio')
        validate['cuit'] = self.validar_numerico(self.cuit_entry.get(), 'CUIT no válido')
        validate['mail'] = self.mail_entry.get().lower() or '-'
        validate['telefono'] = self.validar_numerico(self.telefono_entry.get(), 'Teléfono no válido')
        validate['cp'] = self.validar_numerico(self.cp_entry.get(), 'CP no válido')
        validate['provincia'] = self.provincia_entry.get() or '-'
        return validate

    def validar_numerico(self, campo, error):
        """Valida que el campo sea numérico."""
        try:
            int(campo)
            return campo
        except ValueError:
            self.alert(error)
            return False

    def alert(self, mensaje):
        """Agrega un mensaje a la alerta."""
        if hasattr(self, 'alertas_texto'):
            self.alertas_texto += f' {mensaje}'
        else:
            self.alertas_texto = f'Error: {mensaje}'

    def alertas(self, validate):
        """Genera los mensajes de alerta para los campos inválidos."""
        return self.alertas_texto

    def nuevo_cliente(self, validate):
        """Inserta un nuevo cliente en la base de datos."""
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query = """
        INSERT INTO clientes (nombre, facturacion, domicilio, cuit, mail, telefono, cp, provincia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        QueriesSQLite.execute_query(connection, query, tuple(validate.values()))
        messagebox.showinfo("BBDD", "Datos Cargados Correctamente")
        self.clientes_table.cargar_datos()
        self.cuadroNombre.delete(0, tk.END)
        self.ingreso_popup.destroy()

    def eliminar_cliente(self):
        """Elimina un cliente seleccionado de la base de datos."""
        values = self.clientes_table.seleccion_datos()
        if not values:
            messagebox.showerror("Error", "Seleccione algún cliente")
            return

        respuesta = messagebox.askokcancel("Eliminar", f"Eliminar: {values[0]} - {values[1]}")
        if respuesta:
            connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
            query = "DELETE FROM Clientes WHERE id = ?"
            QueriesSQLite.execute_query(connection, query, (values[0],))
            messagebox.showinfo("BBDD", "Datos eliminados correctamente")
            self.clientes_table.cargar_datos()

    def modificar_cliente(self):
        """Abre el formulario para modificar un cliente existente."""
        self.values_edit = self.clientes_table.seleccion_datos()
        if self.values_edit:
            self.formulario_cliente(self.actualizar_cliente)
            self.id_cliente = self.values_edit[0]
            self.label_titulo.config(text="Modificar Cliente")
            self.rellenar_formulario(self.values_edit)

    def actualizar_cliente(self):
        """Actualiza los datos de un cliente en la base de datos."""
        datos_actualizados = self.obtener_datos_formulario()
        if False in datos_actualizados.values():
            messagebox.showwarning("Campos inválidos", self.alertas(datos_actualizados))
            return

        mensaje = self.generar_mensaje_cambios(datos_actualizados)
        respuesta = messagebox.askokcancel("Modificar", mensaje)
        if respuesta:
            connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
            query = """
            UPDATE clientes 
            SET nombre = ?, facturacion = ?, domicilio = ?, cuit = ?, mail = ?, telefono = ?, cp = ?, provincia = ?
            WHERE id = ?
            """
            QueriesSQLite.execute_query(connection, query, tuple(datos_actualizados.values()) + (self.id_cliente,))
            self.clientes_table.cargar_datos()
            self.ingreso_popup.destroy()

    def generar_mensaje_cambios(self, datos_actualizados):
        """Genera un mensaje con los cambios a aplicar."""
        mensaje = 'Aplicar los siguientes cambios:\n'
        for campo, valor in datos_actualizados.items():
            if valor != self.values_edit[self.indices_campo()[campo]]:
                mensaje += f"Nuevo {campo}: {valor}\n"
        return mensaje

    @staticmethod
    def indices_campo():
        """Devuelve un diccionario con los índices de los campos en la tupla de valores."""
        return {
            'nombre': 1, 'facturacion': 2, 'domicilio': 3,
            'cuit': 4, 'mail': 5, 'telefono': 6, 'cp': 7, 'provincia': 8
        }

    def rellenar_formulario(self, values):
        """Rellena el formulario con los datos del cliente a modificar."""
        self.nombre_entry.insert(0, values[1])
        self.facturacion_entry.insert(0, values[2])
        self.domicilio_entry.insert(0, values[3])
        self.cuit_entry.insert(0, values[4])
        self.mail_entry.insert(0, values[5])
        self.telefono_entry.insert(0, values[6])
        self.cp_entry.insert(0, values[7])
        self.provincia_entry.insert(0, values[8])

    def formulario_cliente(self, command):
        """Abre el formulario de entrada de datos de clientes."""
        self.ingreso_popup = tk.Toplevel()
        self.ingreso_popup.geometry("400x350")
        self.ingreso_popup.overrideredirect(True)
        self.ingreso_popup.grab_set()

        main_frame = ttk.Frame(self.ingreso_popup)
        main_frame.pack()
        self.label_titulo = ttk.Label(main_frame, text="", font=('Arial Bold', 16), anchor='center')
        self.label_titulo.pack(fill='x', pady=5)

        frame_label = ttk.Frame(main_frame)
        frame_label.pack(side='left')
        frame_entry = ttk.Frame(main_frame)
        frame_entry.pack(side="left")

        # Creación de etiquetas y entradas
        self.crear_etiqueta_entrada(frame_label, frame_entry, "Nombre: ", "nombre_entry")
        self.crear_etiqueta_entrada(frame_label, frame_entry, "Facturación a Nombre: ", "facturacion_entry")
        self.crear_etiqueta_entrada(frame_label, frame_entry, "Domicilio: ", "domicilio_entry")
        self.crear_etiqueta_entrada(frame_label, frame_entry, "CUIT: ", "cuit_entry")
        self.crear_etiqueta_entrada(frame_label, frame_entry, "Mail: ", "mail_entry")
        self.crear_etiqueta_entrada(frame_label, frame_entry, "Teléfono: ", "telefono_entry")
        self.crear_etiqueta_entrada(frame_label, frame_entry, "CP: ", "cp_entry")

        label_provincia = ttk.Label(frame_label, text="Provincia: ")
        label_provincia.pack(padx=5, pady=5)
        self.provincia_entry = ttk.Combobox(frame_entry, values=[
            'Buenos Aires', 'Entre Ríos', 'Santa Fé', 'Corrientes', 'Misiones', 'Chaco', 
            'Formosa', 'Jujuy', 'Salta', 'La Rioja', 'San Juan', 'Córdoba', 'Santiago del Estero', 
            'Tucumán', 'Mendoza', 'San Luis', 'Catamarca', 'La Pampa', 'Chubut', 'Río Negro', 
            'Santa Cruz', 'Tierra del Fuego', 'Neuquén'
        ])
        self.provincia_entry.pack(fill='y', padx=5, pady=4)

        add_button = ttk.Button(self.ingreso_popup, text='Agregar', command=command)
        add_button.pack(side="bottom", fill="x", padx=5, pady=5)
        cancel_button = ttk.Button(self.ingreso_popup, text='Cancelar', command=self.ingreso_popup.destroy)
        cancel_button.pack(side="bottom", fill="x", padx=5, pady=5)

    def crear_etiqueta_entrada(self, frame_label, frame_entry, text, var_name):
        """Crea una etiqueta y una entrada en el formulario."""
        label = ttk.Label(frame_label, text=text)
        label.pack(padx=5, pady=5)
        setattr(self, var_name, ttk.Entry(frame_entry))
        getattr(self, var_name).pack(fill='y', padx=5, pady=4)

    def on_double_click(self, event):
        """Maneja el evento de doble clic en la tabla."""
        self.cuadroNombre.delete(0, tk.END)
        selection = self.clientes_table.seleccion_datos()
        if selection:
            self.cuadroNombre.insert(0, selection[1])

class Clientes_PopUp(tk.Toplevel):
    def __init__(self, values):
        super().__init__()
        self.title("Resultados de Búsqueda")
        self.setup_ui(values)

    def setup_ui(self, values):
        """Configura la interfaz de usuario del popup de resultados."""
        self.resultados_tree = ttk.Treeview(self, columns=(
            "ID", "Nombre", "Domicilio", "CUIT", "Telefono", "CP", "Provincia"
        ))
        self.resultados_tree.heading("#0", text="ID")
        self.resultados_tree.column("#0", minwidth=0, width=0, stretch=tk.NO)
        self.crear_columna("ID", "ID", 20)
        self.crear_columna("Nombre", "Nombre", 100)
        self.crear_columna("Domicilio", "Domicilio", 100)
        self.crear_columna("CUIT", "CUIT", 75)
        self.crear_columna("Telefono", "Telefono", 75)
        self.crear_columna("CP", "CP", 25)
        self.crear_columna("Provincia", "Provincia", 100)
        self.resultados_tree.pack(fill=tk.BOTH, expand=True)
        self.actualizar_resultados(values)

    def crear_columna(self, id_columna, texto, ancho):
        """Crea una columna en el Treeview."""
        self.resultados_tree.heading(id_columna, text=texto)
        self.resultados_tree.column(id_columna, width=ancho, anchor="center")

    def actualizar_resultados(self, values):
        """Actualiza los resultados del Treeview."""
        self.resultados_tree.delete(*self.resultados_tree.get_children())
        for value in values:
            self.resultados_tree.insert("", "end", text=value["ID"], values=(
                value["ID"], value["Nombre"], value["Domicilio"], value["CUIT"], 
                value["Telefono"], value["CP"], value["Provincia"]
            ))
