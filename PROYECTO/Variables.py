import tkinter as tk #modulo para la creacion de ventanas y frames widgets
from tkinter import font
import ctypes
from datetime import datetime
import os
import getpass
import time #modulo para funciones de tiempo
import random #modulo para general randoms
import socket
import psutil
from cryptography.fernet import Fernet
import base64

##########################
        #FUNCIONES
##########################

def generar_clave_maestra():
    return b'\x9290\xe3,\xf8\xb9j\xd2\xe6\x8aV\x1a\xe0\x8a\xf4z\x0e\xd8\xc9\x90\xad\xef\x9f\xc4\x05o\xd0\x91,\xcf\xd1'

def generar_numero_aleatorio(n1, n2):
    return random.randint(n1, n2)

def obtener_fecha_hora(etiqueta):
    global cadena_fecha_hora
    # Obtener la fecha y hora actual
    fecha_hora_actual = datetime.now()
    cadena_fecha_hora = fecha_hora_actual.strftime("%Y-%m-%d    %I:%M %p")
    etiqueta.config(text=cadena_fecha_hora)
    
    # Programar la próxima actualización después de un tiempo en milisegundos
    etiqueta.after(1500, lambda: obtener_fecha_hora(etiqueta))

##########################
        #VARIBALES
##########################
#Variables inicializador de ventana
root = tk.Tk() #inicializar tk ventana root
ancho_p = root.winfo_screenwidth() #obtener ancho pantalla widnows
alto_p = root.winfo_screenheight() #obtener alto pantalla widnows
barra_tareas = ctypes.windll.user32.GetSystemMetrics(2) #obtener tamaño barra tareas

#Variables tiempo
Tiempo = generar_numero_aleatorio(3, 6)
fecha = datetime.now().strftime("%Y-%m-%d")
hora = datetime.now().strftime("%I:%M %p")

#Variables archivos rutas
titulo = "NetAplication_v2" #titulo de las ventanas

alerta_aviso = "Aviso" #titulo alerta 
alerta_error = "Error" #titulo alerta error

icono_v = "lib/data/icono.ico" #icono de las ventanas
icono_help = "lib/data/help.png" #icono del boton informativo help

#Variables datos de usuario del equipo
Host_nombre = socket.gethostname()
nombre_usuario = getpass.getuser()
host_y_usuario = f"{Host_nombre} / {nombre_usuario}"
ruta_escritorio = os.path.join(os.path.expanduser("~"), "Desktop")

#Variables archivos
ruta = "lib/data/Docs_plantilla/"
Excel_lleno = "DB_w.xlsx"
Excel_wifi_lleno = os.path.join(ruta, Excel_lleno)
eth = "lib/data/temp/eth"
wire = "lib/data/temp/wire"
conexion = "lib/data/temp/Conexion"

#Variables de archivo a exportar wireless
Nombre_Excel_exportar = f"{'Data_wireless'}_{fecha}.xlsx" #nombre del archivo a exportar + fecha
Excel_wifi_exportado = os.path.join(ruta_escritorio, Nombre_Excel_exportar) #nombre con ruta y Nombre_Excel_exportar

#Variables colores
c_barras = "#FFFFFF" #color barras superior e inferior
c_s_b = "#C9EDF8" #color selecionar boton
c_centros = "#EBEBEB" #color centro
c_lina_separacion = "#AAAAAA" #color linea de separacion de frames

#Variables Net
drive = ""
D_ip = ""
net_ssid = ""
net_stado = ""
v_dns = ""

v_recepcion = ""
v_transmision = ""
v_canal = ""
v_señal = ""

# Variables recuentos de redes escaneadas
v_recuento = 0 #guarda el recuento de todas las redes escaneada del documento!
treeview_recuento = 0 #guarda el recuento de datos en el treeview
selecion_recuento = 0

# fuente
ruta_fuente = "lib/Data/fuente/poppins.ttf" # ruta de la fuente poppins
poppins_negrita = font.Font(family="Popins", weight="bold")
poppins = font.Font(family="Popins")

#clave maestra
Clave_maestra = b'\x9290\xe3,\xf8\xb9j\xd2\xe6\x8aV\x1a\xe0\x8a\xf4z\x0e\xd8\xc9\x90\xad\xef\x9f\xc4\x05o\xd0\x91,\xcf\xd1'
# Codificar en base64 para obtener la clave Fernet válida
clave_maestra = base64.urlsafe_b64encode(Clave_maestra)

networks = "lib/networks.json" #variable de la ruta del archivo con los datos de las networks