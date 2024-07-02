from email import message
from tkinter import Toplevel, messagebox
from openpyxl import Workbook, load_workbook
import openpyxl
from datetime import datetime
import os

def reporte_ingresos(lista_items):
    n_reporte =  datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    wb = load_workbook('Reportes/Ingresos/Reporte_Ingresos.xlsx')
    excel_file = f'Reportes/Ingresos/RING{n_reporte}.xlsx'
    hoja = wb.worksheets[0]


    indice_fila = 3
    total_peso = 0
    suma_bultos  = len(lista_items)

    for item in lista_items:
        total_peso += float(item[4])
        insertar_fila_y_ajustar_alto(hoja, indice_fila, item)
        indice_fila += 1
        
    hoja[f'D{indice_fila}'] = suma_bultos
    hoja[f'F{indice_fila}'] = total_peso
    
    # Guardar archivo excel
    wb.save(excel_file)
    respuesta = messagebox.askokcancel("Abrir Reporte", "Desea abrir el reporte generado?")
    if respuesta:
        # Abre el archivo con Excel
        os.system(f'start excel "{excel_file}"')
        
def insertar_fila_y_ajustar_alto(hoja, indice_fila, item):
    
    # Insertar una nueva fila en la posición especificada
    hoja.insert_rows(indice_fila)

    # Insertar los datos en la nueva fila
    #Articulo
    hoja[f'B{indice_fila}'] = item[0]
    #Detalle
    hoja[f'C{indice_fila}'] = item[1]
    #Bultos
    hoja[f'D{indice_fila}'] = item[2]
    #Pesos
    hoja[f'E{indice_fila}'] = item[3]
    #
    hoja[f'F{indice_fila}'] = item[4]
    hoja[f'G{indice_fila}'] = item[5]
    hoja[f'H{indice_fila}'] = item[6]
    hoja[f'I{indice_fila}'] = item[7]
    hoja[f'J{indice_fila}'] = item[8]
    hoja[f'K{indice_fila}'] = item[9]