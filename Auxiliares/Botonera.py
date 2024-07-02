from tkinter import *
from tkinter import ttk
import tkinter as tk
from turtle import left
from tkcalendar import DateEntry
import os
from PIL import Image, ImageTk
# class Botonera:
class Botonera(tk.Frame):
    def __init__(self, parent, busqueda=None, nuevo=None, eliminar=None, modificar=None):
        super().__init__(parent)

        if busqueda:
            self.search_button_image = ImageTk.PhotoImage(self.resize_images("search"))
            self.busqueda = ttk.Button(self, text="Buscar", image=self.search_button_image, compound="top", command=busqueda)
            self.busqueda.pack(side="left", fill="x", padx=5)
            
        if nuevo:
            self.add_button_image    = ImageTk.PhotoImage(self.resize_images("add"))
            self.agregar = ttk.Button(self, text="Agregar", image=self.add_button_image, compound="top", command=nuevo)
            self.agregar.pack(side="left", fill="x", padx=5)
            
        if eliminar:
            self.delete_button_image = ImageTk.PhotoImage(self.resize_images("delete"))
            self.eliminar = ttk.Button(self, text="Eliminar", image=self.delete_button_image, compound="top", command=eliminar)
            self.eliminar.pack(side="left", fill="x", padx=5)
            
        if modificar:
            self.edit_button_image   = ImageTk.PhotoImage(self.resize_images("edit"))
            self.modificar = ttk.Button(self, text="Modificar", image=self.edit_button_image, compound="top", command=modificar)
            self.modificar.pack(side="left", fill="x", padx=5)
            
    def resize_images(self, icon):
        open_image = Image.open(f"images/{icon}.png")
        resize_image = open_image.resize((30,30))
        return resize_image
    
class Exportar(tk.Frame):
    def __init__(self, parent, export):
        super().__init__(parent)
        
        self.export_button_image   = ImageTk.PhotoImage(self.resize_images("exportar"))
        self.export = ttk.Button(self, text="Exportar", image=self.export_button_image, compound="top", command=export)
        self.export.pack(side="left", fill="x", padx=5)
        
    def resize_images(self, icon):
        open_image = Image.open(f"images/{icon}.png")
        resize_image = open_image.resize((30,30))
        return resize_image
        