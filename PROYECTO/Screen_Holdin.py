import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import font
from datetime import datetime
import getpass
import socket
import time #modulo para funciones de tiemp
import random #modulo para general randoms

#Variables datos de usuario del equipo
Host_nombre = socket.gethostname()
nombre_usuario = getpass.getuser()
host_y_usuario = f"{Host_nombre} / {nombre_usuario}"

def generar_numero_aleatorio(n1, n2):
    return random.randint(n1, n2)

def mostrar_imagen_con_texto():
    tiempo_espera = generar_numero_aleatorio(3000, 8000)
    root = tk.Tk()
    root.overrideredirect(True)  # Oculta la barra de título y bordes de la ventana

    # Obtener el ancho y alto de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcular la posición de la imagen para que aparezca en el centro
    x = (screen_width - 300) // 2  # Ajusta 300 al ancho deseado de la imagen
    y = (screen_height - 300) // 2  # Ajusta 300 al alto deseado de la imagen
    root.geometry("+{}+{}".format(x, y))  # Posición de la ventana

    # Cargar la imagen y cambiar su tamaño
    imagen = Image.open('lib/Data/loading.png')
    imagen = imagen.resize((300, 300))
    draw = ImageDraw.Draw(imagen)
    # Agregar texto a la imagen
    texto = "NetAplication V2"
    font = ImageFont.truetype("lib/Data/fuente/poppins.ttf", 20)
    draw.text((75, 180), texto, fill="black", font=font)

    texto = "Cargando..."
    font = ImageFont.truetype("lib/Data/fuente/poppins.ttf", 20)
    draw.text((100, 210), texto, fill="black", font=font)

    texto = host_y_usuario
    font = ImageFont.truetype("lib/Data/fuente/poppins.ttf", 10)
    draw.text((75, 270), texto, fill="black", font=font)

    # Crear una referencia global a img en la ventana principal
    root.img = ImageTk.PhotoImage(imagen)

    panel = tk.Label(root, image=root.img)
    panel.pack()

    root.after(tiempo_espera, root.destroy) cerrar ventana despues de tiempo_espera
    root.mainloop()

if __name__ == "__main__":
    mostrar_imagen_con_texto()
