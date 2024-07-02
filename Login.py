import  tkinter    as     tk
from    tkinter    import ttk
from    tkinter    import messagebox
from    Auxiliares.sqlqueries import QueriesSQLite
from    App        import AppWindow

class LoginWindow():
    QueriesSQLite.create_tables()
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Inicio de Sesión")
        self.window.resizable(width=0,height=0)
        # self.geometry("200x250")
        self.center_window()
        
        self.frame_login = tk.Frame(self.window)
        self.frame_login.pack()

        self.label_username = ttk.Label(self.frame_login, text="Usuario:")
        self.label_username.pack()
        self.entry_username = ttk.Entry(self.frame_login)
        self.entry_username.pack(padx=5,pady=5)

        self.label_password = ttk.Label(self.frame_login, text="Contraseña:")
        self.label_password.pack()
        self.entry_password = ttk.Entry(self.frame_login, show="*")
        self.entry_password.pack(padx=5,pady=5)

        self.btn_login = ttk.Button(self.frame_login, text="Iniciar Sesión", command=self.login)
        self.btn_login.pack()
        
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar_login)
        
        self.window.mainloop()
        
    def cerrar_login(self):
        self.window.quit()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")
        query_username = "SELECT * FROM usuarios WHERE username = ?"
        usuario = QueriesSQLite.execute_read_query(connection, query_username, (username,))
        if usuario:
            if password == usuario[0][2]:
                self.window.destroy()  # Cerrar la ventana de inicio de sesión
                AppWindow().mainloop  # Mostrar la aplicación principal
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        # Aquí puedes añadir la lógica de autenticación.
        # Por ejemplo, puedes comparar el usuario y la contraseña con un valor predeterminado.

        # if username == "" and password == "":
        #     self.window.destroy()  # Cerrar la ventana de inicio de sesión
        #     AppWindow().mainloop  # Mostrar la aplicación principal
        # else:
        #     messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def center_window(self):
        # Obtener el ancho y alto de la ventana
        window_width = 200
        window_height = 150

        # Obtener el ancho y alto de la pantalla
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calcular la posición del lado superior izquierdo de la ventana para centrarla
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Configurar la geometría de la ventana para centrarla
        self.window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        
        