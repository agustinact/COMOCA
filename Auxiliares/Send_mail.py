import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def enviar_correo_con_adjuntos(destinatario, n_remito, cliente, factura, archivo_adjuntos):
    # Crear el objeto de mensaje
    remitente = 'marianofchaves@outlook.com'
    contraseña = '110784mc'
    asunto = f'Comprobante de entrega: {str(n_remito)}'  # Asegúrate de que n_remito es una cadena
    cuerpo = f'Estimado {str(cliente)}. Adjuntamos el comprobante de envío correspondiente a la Factura N° {str(factura)}'  # Asegúrate de que cliente y factura son cadenas
    mensaje = MIMEMultipart()
    mensaje['From'] = str(remitente)
    mensaje['To'] = str(destinatario)
    mensaje['Subject'] = str(asunto)

    # Agregar el cuerpo del correo
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Adjuntar el archivo
    for archivo in archivo_adjuntos:
        # Abre el archivo en modo binario
        with open(archivo, 'rb') as adjunto:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(adjunto.read())

        # Codificar el archivo en base64
        encoders.encode_base64(mime_base)

        # Agregar el encabezado al archivo
        mime_base.add_header('Content-Disposition', f'attachment; filename={archivo}')

        # Adjuntar el archivo al mensaje
        mensaje.attach(mime_base)

    # Configurar el servidor SMTP
    servidor = smtplib.SMTP('smtp-mail.outlook.com', 587)
    servidor.starttls()
    servidor.login(remitente, contraseña)

    # Convertir el mensaje en una cadena de texto y enviarlo
    texto = mensaje.as_string()
    servidor.sendmail(remitente, destinatario, texto)

    # Cerrar la conexión con el servidor
    servidor.quit()
