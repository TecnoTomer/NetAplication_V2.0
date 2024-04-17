import os
import logbook
import Variables
from datetime import datetime

def configurar_logs(log_doc):
    fecha_actual = datetime.now().strftime('%Y-%m-%d') #fecha actual
    hora_actual = datetime.now().strftime('%I:%M %p') #hora actual con formato 12 horas y pm o am
    
    # Configurar el archivo de logs con un Formatter personalizado
    logbook.FileHandler(log_doc, format_string=f'[{fecha_actual} {hora_actual}] {{record.level_name}}: {{record.message}}').push_application()

def agregar_log(mensaje):
    logbook.info(mensaje)

