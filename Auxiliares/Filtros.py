import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry


class Filtros_Ingresos(tk.Frame):
    def __init__(self, parent, filtro_producto=None, filtro_proveedor=None, filtro_fecha=None, limpiar_filtro=None, filtro_pallet=None, filtro_factura=None) :
        super().__init__(parent)
        
        self.primer_frame = tk.Frame(self)
        self.primer_frame.pack(fill='x', expand=True) 
        
        if filtro_producto:
            self.filtro_producto = ttk.Button(self.primer_frame, text="Filtro Producto", command=filtro_producto)
            self.filtro_producto.pack(side="left", padx=5)
            self.producto_entry = ttk.Entry(self.primer_frame)
            self.producto_entry.pack(side="left", padx=5)
            
        if filtro_proveedor:
            self.filtro_proveedor = ttk.Button(self.primer_frame, text="Filtro Proveedor", command=filtro_proveedor)
            self.filtro_proveedor.pack(side="left", padx=5)
            self.proveedor_entry = ttk.Entry(self.primer_frame)
            self.proveedor_entry.pack(side="left", padx=5)
            
        if filtro_pallet:
            self.filtro_pallet_btn = ttk.Button(self.primer_frame, text="Filtro Pallet", command=filtro_pallet)
            self.filtro_pallet_btn.pack(side="left", padx=5)
            self.pallet_list = ttk.Combobox(self.primer_frame, state='readonly')
            self.pallet_list.pack(side="left", padx=5)
            

        self.label_fechai = ttk.Label(self.primer_frame, text='Desde: ')
        self.label_fechai.pack(side='left', padx=5)
        self.fechai_entry = DateEntry(self.primer_frame)
        self.fechai_entry.pack(side="left", fill="x", padx=5)
        self.label_fechaf = ttk.Label(self.primer_frame, text='Hasta: ')
        self.label_fechaf.pack(side='left', padx=5)
        self.fechaf_entry = DateEntry(self.primer_frame)
        self.fechaf_entry.pack(side="left", fill="x", padx=5)
        self.filtro_proveedor = ttk.Button(self.primer_frame, text="Filtrar Fecha", command=filtro_fecha)
        self.filtro_proveedor.pack(side="left", fill="x", padx=5)
        
        self.segundo_frame = tk.Frame(self)
        self.segundo_frame.pack(fill='x', expand=True, pady=5)   
        
        if filtro_factura:
            self.filtro_factura_btn = ttk.Button(self.segundo_frame, text="Filtro Factura", command=filtro_factura)
            self.filtro_factura_btn.pack(side="left", padx=5)
            self.factura_list = ttk.Combobox(self.segundo_frame, state='readonly')
            self.factura_list.pack(side="left", padx=5)
            
        if limpiar_filtro:
            self.limpiar_filtro = tk.Button(self.segundo_frame, text="Limpiar Filtros", command=limpiar_filtro, background='blue', foreground='white')
            self.limpiar_filtro.pack(side="left", padx=5)
            self.producto_entry.delete(0,tk.END)
            self.proveedor_entry.delete(0,tk.END)
            self.pallet_list.delete(0,tk.END)
            
            

class Filtros_Salidas(tk.Frame):
    def __init__(self, parent, filtro_remito=None, filtro_producto=None, filtro_cliente=None, filtro_fecha=None, limpiar_filtro=None, filtro_pallet=None, filtro_factura=None) :
        super().__init__(parent)
        
        self.primer_frame = tk.Frame(self)
        self.primer_frame.pack(fill='x', expand=True) 
        
        if filtro_remito:
            self.filtro_remito = ttk.Button(self.primer_frame, text="Filtro Remito", command=filtro_remito)
            self.filtro_remito.pack(side="left", padx=5)
            self.remito_list = ttk.Combobox(self.primer_frame, state='readonly')
            self.remito_list.pack(side="left", padx=5)
            
        if filtro_producto:
            self.filtro_producto = ttk.Button(self.primer_frame, text="Filtro Producto", command=filtro_producto)
            self.filtro_producto.pack(side="left", padx=5)
            self.producto_entry = ttk.Entry(self.primer_frame)
            self.producto_entry.pack(side="left", padx=5)
            
        if filtro_cliente:
            self.filtro_cliente = ttk.Button(self.primer_frame, text="Filtro Cliente", command=filtro_cliente)
            self.filtro_cliente.pack(side="left", padx=5)
            self.cliente_entry = ttk.Entry(self.primer_frame)
            self.cliente_entry.pack(side="left", padx=5)
        
        if filtro_pallet:
            self.filtro_pallet_btn = ttk.Button(self.primer_frame, text="Filtro Pallet", command=filtro_pallet)
            self.filtro_pallet_btn.pack(side="left", padx=5)
            self.pallet_list = ttk.Combobox(self.primer_frame, state='readonly')
            self.pallet_list.pack(side="left", padx=5)
        
        self.segundo_frame = tk.Frame(self)
        self.segundo_frame.pack(fill='x', expand=True, pady=5)    

        self.label_fechai = ttk.Label(self.segundo_frame, text='Desde: ')
        self.label_fechai.pack(side='left', padx=5)
        self.fechai_entry = DateEntry(self.segundo_frame)
        self.fechai_entry.pack(side="left", padx=5)
        self.label_fechaf = ttk.Label(self.segundo_frame, text='Hasta: ')
        self.label_fechaf.pack(side='left', padx=5)
        self.fechaf_entry = DateEntry(self.segundo_frame)
        self.fechaf_entry.pack(side="left", padx=5)
        self.filtro_proveedor = ttk.Button(self.segundo_frame, text="Filtrar Fecha", command=filtro_fecha)
        self.filtro_proveedor.pack(side="left", padx=5)
        
        if filtro_factura:
            self.filtro_factura_btn = ttk.Button(self.segundo_frame, text="Filtro Factura", command=filtro_factura)
            self.filtro_factura_btn.pack(side="left", padx=5)
            self.factura_list = ttk.Combobox(self.segundo_frame, state='readonly')
            self.factura_list.pack(side="left", padx=5)
            
        if limpiar_filtro:
            self.limpiar_filtro = tk.Button(self.segundo_frame, text="Limpiar Filtros", command=limpiar_filtro, background='blue', foreground='white')
            self.limpiar_filtro.pack(side="left", padx=5)
            self.producto_entry.delete(0,tk.END)
            self.cliente_entry.delete(0,tk.END)
            self.pallet_list.delete(0,tk.END)