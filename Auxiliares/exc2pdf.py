import excel2img
from PIL import Image

def excel_to_pdf(excel_file, sheet_name, pdf_file):
    # Genera una imagen de la hoja de Excel
    img_file = "temp_image.png"
    excel2img.export_img(excel_file, img_file, page=sheet_name)

    # Abre la imagen y la guarda como PDF
    image = Image.open(img_file)
    image.convert('RGB').save(pdf_file)

# Especifica los nombres de los archivos y la hoja de Excel a convertir
excel_file = 'remito_plantilla.xlsx'
sheet_name = 'Sheet1'  # Cambia esto al nombre de tu hoja
pdf_file = 'remito_plantilla.pdf'


