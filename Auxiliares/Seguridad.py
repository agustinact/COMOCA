from tkinter import *
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from Auxiliares.sqlqueries import QueriesSQLite
import tkinter as tk

class PasswordWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        # self.window = Toplevel()
        self.title("Seguridad")
        self.resizable(width=0,height=0)
        # self.geometry("200x250")
        self.center_window()
        self.grab_set()
        self.granted = False
        
        self.frame_login = Frame(self)
        self.frame_login.pack()

        self.label_password = ttk.Label(self.frame_login, text="Contraseña:")
        self.label_password.pack()
        self.entry_password = ttk.Entry(self.frame_login, show="*")
        self.entry_password.pack(padx=5,pady=5)
        self.label_info = ttk.Label(self.frame_login, text="")
        self.label_info.pack()

        self.btn_login = ttk.Button(self.frame_login, text="Ingresar", command=self.login)
        self.btn_login.pack()
        self.access = False
        
        # self.window.protocol("WM_DELETE_WINDOW", self.cerrar_login)

        
    # def cerrar_login(self):
    #     self.window.quit()
    def wait_response(self):
        self.wait_window()
        return self.access
    

    def login(self):
        entry = str(self.entry_password.get()).strip()
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query = "SELECT * FROM usuarios WHERE password = ?"
        users = QueriesSQLite.execute_read_query(connection, query, (entry,))
        cont_admin = 0
        # if users:
        #     for user in users:
        #         if user[3] == 'admin':
        #             cont_admin += 1
        #     if cont_admin > 0:
        #         self.access = True
        #         self.destroy()
        #     else:
        #         self.label_info.config(text="No posee los permisos.", foreground="red") 
        # else:
        #     self.label_info.config(text="Contraseña incorrecta", foreground="red") 
        if entry:
            if entry == '110784mc':
                self.access = True
                self.destroy()
            else:
                self.label_info.config(text="Contraseña incorrecta", foreground="red") 
            

            
    def center_window(self):
        # Obtener el ancho y alto de la ventana
        window_width = 200
        window_height = 100

        # Obtener el ancho y alto de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular la posición del lado superior izquierdo de la ventana para centrarla
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Configurar la geometría de la ventana para centrarla
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')