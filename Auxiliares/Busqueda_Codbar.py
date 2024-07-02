from tkinter import *
from tkinter import ttk
import tkinter as tk

class ResultadosBusquedaPopup(tk.Toplevel):
    def __init__(self, item):
        super().__init__()
        self.grab_set()
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=5,pady=5)
        # ------------ Frame Result -------------------
        self.result_frame = ttk.Frame(self.main_frame)
        self.result_frame.pack(pady=5, fill='x', expand=True)
        
        # ------------ Labels Results -------------------
        self.result_id = ttk.Label(self.result_frame, text=f"ID\n{item[0]}", relief='solid', background='white', foreground='blue', anchor='center')
        self.result_id.pack(side='left', fill='x', anchor='center', expand=True)
        
        self.result_codcaja = ttk.Label(self.result_frame, text=f"Código Caja\n{item[1]}", relief='solid', background='white', foreground='blue', anchor='center')
        self.result_codcaja.pack(side='left', fill='x', anchor='center', expand=True)
        
        self.result_idprod = ttk.Label(self.result_frame, text=f"ID Producto\n{item[2]}", relief='solid', background='white', foreground='blue', anchor='center')
        self.result_idprod.pack(side='left', fill='x', anchor='center', expand=True)
        
        self.result_idprov = ttk.Label(self.result_frame, text=f"ID Proveedor\n{item[3]}", relief='solid', background='white', foreground='blue', anchor='center')
        self.result_idprov.pack(side='left', fill='x', anchor='center', expand=True)
        
        self.result_peso = ttk.Label(self.result_frame, text=f"Kilos\n{item[4]}", relief='solid', background='white', foreground='blue', anchor='center')
        self.result_peso.pack(side='left', fill='x', anchor='center', expand=True)
        
        self.result_tropa = ttk.Label(self.result_frame, text=f"Tropa\n{item[5]}", relief='solid', background='white', foreground='blue', anchor='center')
        self.result_tropa.pack(side='left', fill='x', anchor='center', expand=True)
        
        self.result_ingreso = ttk.Label(self.result_frame, text=f"Fecha Ingreso\n{item[6]}", relief='solid', background='white', foreground='blue', anchor='center')
        self.result_ingreso.pack(side='left', fill='x', anchor='center', expand=True)
        
        self.result_vencimiento = ttk.Label(self.result_frame, text=f"Fecha Vencimiento\n{item[7]}", relief='solid', background='white', foreground='blue', anchor='center')
        self.result_vencimiento.pack(side='left', fill='x', anchor='center', expand=True)
        