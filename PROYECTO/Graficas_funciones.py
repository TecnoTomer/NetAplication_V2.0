import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import json
import numpy as np
import keyboard
from tkinter import messagebox
import os
from PIL import ImageTk, Image

import Perzonalizacion_botones
import Variables
import Menus_funciones
from Logs import agregar_log
import Alertas

menu_visible = False

ventana = None
frame_centro = None

def grafico_señal(frame):
    Msg = "Entro a ver grafico por señal"
    agregar_log(Msg)

    # Leer los datos del archivo JSON
    datos = leer_datos_json()

    # Obtener datos de nombre y señal
    nombres = datos["NOMBRE"]
    señales = list(map(int, datos["SEÑAL"]))
    # Invertir el orden de la intensidad de señal
    nombres.reverse()
    señales.reverse()

    # Crear una figura de Matplotlib con un color de fondo personalizado
    fig = Figure(figsize=(8, 6), facecolor='#FFFFFF') 
    ax = fig.add_subplot(111)
    ax.invert_yaxis()

    # Graficar las señales como una línea con un color más oscuro
    puntos, = ax.plot(señales, marker='o', color='#375F82', linestyle='--')

    # Ajustar el color del fondo donde se dibujan las líneas
    ax.set_facecolor('#D6F3AE') 

    # Añadir etiquetas a los puntos de la línea
    for i, (señal, nombre) in enumerate(zip(señales, nombres)):
        # Coordenadas del texto
        xy = (i, señal)
        xytext = (-10, -10) if i % 2 == 0 else (10, 10)  # Coloca el texto a la izquierda o derecha del punto
        if i > 0 and abs(señales[i] - señales[i-1]) < 5:
            xytext = (-10, -20) if xytext[0] < 0 else (10, 20)  # Ajusta la posición si los puntos están muy cerca
        ax.annotate(nombre, xy, textcoords="offset points", xytext=xytext, ha='center', fontsize=5)

    # Establecer etiquetas y límites en los ejes
    ax.set_ylabel('Intensidad de Señal')

    # Ajustar el tamaño del gráfico para que ocupe todo el espacio disponible
    fig.tight_layout()

    # Mostrar la figura en el frame
    global widget_grafico_actual
    widget_grafico_actual = FigureCanvasTkAgg(fig, master=frame)
    widget_grafico_actual.draw()
    widget_grafico_actual.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    # Crear la barra de herramientas
    toolbar = NavigationToolbar2Tk(widget_grafico_actual, frame)

    # Ocultar todos los botones excepto "Guardar"
    toolbar.update()
    for tool in toolbar.winfo_children():
        if isinstance(tool, tk.Button) and "Save" not in tool.cget('text'):
            tool.pack_forget()

    # Configurar manualmente el tamaño de la barra de herramientas
    toolbar.pack(side=tk.LEFT, padx=0, pady=0, anchor='center', expand=False)
    toolbar.pack_propagate(False)  # Evita que la barra de herramientas cambie de tamaño automáticamente
    toolbar.config(width=250, height=30)  # Establece el ancho y alto de la barra de herramientas

    return frame

def grafico_frecuencia(frame):
    Msg = "Entro a ver grafico por frecuencia"
    agregar_log(Msg)
    global grafica_actual
    global nombre_grafica
    nombre_grafica = "frecuencia.png"
    # Leer los datos del archivo JSON
    datos = leer_datos_json()

    # Obtener los nombres y frecuencias de las redes Wi-Fi
    nombres = datos["NOMBRE"]
    frecuencias = datos["FRECUENCIA (GHz)"]

    # Convertir las frecuencias a números
    frecuencias_numericas = [float(f) for f in frecuencias]

    # Contar la cantidad de redes por frecuencia
    frecuencia_count = {}
    frecuencia_nombres = {}  # Diccionario para almacenar los nombres de las redes por frecuencia
    for nombre, frecuencia in zip(nombres, frecuencias_numericas):
        if frecuencia in frecuencia_count:
            frecuencia_count[frecuencia] += 1
            frecuencia_nombres[frecuencia].append(nombre)
        else:
            frecuencia_count[frecuencia] = 1
            frecuencia_nombres[frecuencia] = [nombre]

    # Preparar los datos para graficar
    frecuencia_labels = list(frecuencia_count.keys())
    frecuencia_values = list(frecuencia_count.values())

    # Crear una figura de Matplotlib con un tamaño más alto
    fig = Figure(figsize=(7, 6))  # Ajusta el tamaño aquí
    ax = fig.add_subplot(111)

    grafica_actual = fig

    # Graficar los datos como un gráfico de barras
    bars = ax.bar(frecuencia_labels, frecuencia_values, color='skyblue')

    # Definir los valores específicos para las marcas en el eje y
    y_max = max(frecuencia_values) + 30  # Incrementa el límite superior en 30
    y_ticks = list(range(1, y_max, 5))  # Crear una secuencia de 0 a y_max con un paso de 10
    y_max = max(frecuencia_values)

    # Agregar los nombres de las redes al lado de las barras
    for bar, frecuencia in zip(bars, frecuencia_labels):
        nombres_frecuencia = '\n'.join(frecuencia_nombres[frecuencia])
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), nombres_frecuencia, ha='center', va='bottom', fontsize=6, wrap=True)

    # Calcular x_pos solo si hay más de un valor de frecuencia
    if len(frecuencia_labels) > 1:
        for bar, frecuencia in zip(bars, frecuencia_labels):
            x_pos = (frecuencia - min(frecuencia_labels)) / (max(frecuencia_labels) - min(frecuencia_labels))
            ax.axhline(y=bar.get_height(), xmin=0, xmax=x_pos, color='gray', linestyle='--')
    else:
        # Si solo hay un valor de frecuencia, coloca la línea en el centro del eje x
        for bar in bars:
            ax.axhline(y=bar.get_height(), xmin=0, xmax=0.5, color='gray', linestyle='--')

    # Establecer etiquetas y título
    ax.set_xlabel('Frecuencia (GHz)')
    ax.set_ylabel('Cantidad de Redes Wi-Fi')
    ax.set_title('Gráfico de Barras de Frecuencia de Redes Wi-Fi')

    # Ajustar el tamaño del gráfico para que ocupe todo el espacio disponible
    fig.tight_layout()

    # Establecer los valores de las marcas en el eje y
    ax.set_yticks(y_ticks)

    # Establecer las marcas personalizadas en el eje x
    ax.set_xticks(frecuencia_labels)
    ax.set_xticklabels([f'{freq:.1f}' for freq in frecuencia_labels])

    # Establecer el nombre del eje x
    ax.set_xlabel('Frecuencia (GHz)', fontsize=6)

    # Etiquetar las bandas de frecuencia y mejorar la precisión en el eje x
    for label, value in zip(ax.get_xticklabels(), frecuencia_labels):
        banda = etiquetar_banda(value)
        label.set_text(f'{value:.1f} GHz ({banda})')

    # Mostrar la figura en el frame
    widget_grafico_actual = FigureCanvasTkAgg(fig, master=frame)
    widget_grafico_actual.draw()
    widget_grafico_actual.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    # Crear la barra de herramientas
    toolbar = NavigationToolbar2Tk(widget_grafico_actual, frame)

    # Ocultar todos los botones excepto "Guardar"
    toolbar.update()
    for tool in toolbar.winfo_children():
        if isinstance(tool, tk.Button) and "Save" not in tool.cget('text'):
            tool.pack_forget()

    # Configurar manualmente el tamaño de la barra de herramientas
    toolbar.pack(side=tk.LEFT, padx=0, pady=0, anchor='center', expand=False)
    toolbar.pack_propagate(False)  # Evita que la barra de herramientas cambie de tamaño automáticamente
    toolbar.config(width=250, height=30)  # Establece el ancho y alto de la barra de herramientas

    return frame

def grafico_banda(frame):
    Msg = "Entro a ver grafico por banda"
    agregar_log(Msg)
    global grafica_actual
    global nombre_grafica
    nombre_grafica = "banda.png"
    # Leer los datos del archivo JSON
    datos = leer_datos_json()

    # Obtener los datos relevantes
    nombres = datos["NOMBRE"]
    frecuencias = datos["FRECUENCIA (GHz)"]
    bandas = datos["BANDA"]

    # Contar la cantidad de redes por banda
    banda_count = {"2.4 GHz": 0, "5 GHz": 0}
    redes_2_4 = []

    for nombre, banda in zip(nombres, bandas):
        if banda == "2.4 GHz":
            banda_count["2.4 GHz"] += 1
            redes_2_4.append(nombre)
        elif banda == "5 GHz":
            banda_count["5 GHz"] += 1

    # Preparar los datos para graficar
    banda_labels = list(banda_count.keys())
    banda_values = list(banda_count.values())

    # Crear una figura de Matplotlib
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    # Graficar los datos como un gráfico de barras
    ax.bar(banda_labels, banda_values, color='lightgreen')

    # Mostrar el nombre de las redes en forma de lista dentro de la barra correspondiente
    for banda, redes in zip(banda_labels, [redes_2_4]):
        redes_list = '\n'.join([', '.join(redes[i:i+3]) for i in range(0, len(redes), 3)])
        ax.text(banda, banda_count[banda] / 2, redes_list, ha='center', va='center', color='black', fontsize=6)

    # Establecer etiquetas y título
    ax.set_xlabel('Banda')
    ax.set_ylabel('Cantidad de Redes Wi-Fi: ' + str(sum(banda_values)))  # Establece el total de redes Wi-Fi
    ax.set_title('Gráfico de Barras de Banda de Redes Wi-Fi')

    # Ajustar el tamaño del gráfico para que ocupe todo el espacio disponible
    fig.tight_layout()

    # Mostrar la figura en el frame
    widget_grafico_actual = FigureCanvasTkAgg(fig, master=frame)
    widget_grafico_actual.draw()
    widget_grafico_actual.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    # Crear la barra de herramientas
    toolbar = NavigationToolbar2Tk(widget_grafico_actual, frame)

    # Ocultar todos los botones excepto "Guardar"
    toolbar.update()
    for tool in toolbar.winfo_children():
        if isinstance(tool, tk.Button) and "Save" not in tool.cget('text'):
            tool.pack_forget()

    # Configurar manualmente el tamaño de la barra de herramientas
    toolbar.pack(side=tk.LEFT, padx=0, pady=0, anchor='center', expand=False)
    toolbar.pack_propagate(False)  # Evita que la barra de herramientas cambie de tamaño automáticamente
    toolbar.config(width=250, height=30)  # Establece el ancho y alto de la barra de herramientas

    return frame

def grafico_canales(frame):
    Msg = "Entro a ver grafico por canales"
    agregar_log(Msg)
    global grafica_actual
    global nombre_grafica
    nombre_grafica = "canales.png"
    # Leer los datos del archivo JSON
    datos = leer_datos_json()

    # Obtener los datos relevantes
    nombres = datos["NOMBRE"]
    canales = datos["CANAL"]

    # Contar la cantidad de redes por canal
    canal_count = {}
    for canal in canales:
        if canal in canal_count:
            canal_count[canal] += 1
        else:
            canal_count[canal] = 1

    # Función para encontrar los canales con pocos o muchos usos
    def encontrar_canales_pocos_muchos_usados(canal_count):
        canales_pocos_usados = [canal for canal, count in canal_count.items() if count < 5]
        canales_muchos_usados = [canal for canal, count in canal_count.items() if count >= 5]
        return canales_pocos_usados, canales_muchos_usados

    # Preparar los datos para graficar
    canal_labels = list(canal_count.keys())
    canal_values = list(canal_count.values())

    # Crear una figura de Matplotlib
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    grafica_actual = fig

    # Graficar los datos como un gráfico de puntos con líneas
    ax.plot(canal_labels, canal_values, marker='o', color='#972FB9', linestyle='-')

    # Establecer etiquetas y título
    ax.set_xlabel('Canal')
    ax.set_ylabel('Cantidad de Redes Wi-Fi')
    ax.set_title('Gráfico de Puntos de Cantidad de Redes Wi-Fi por Canal')

    # Ajustar el tamaño del gráfico para que ocupe todo el espacio disponible
    fig.tight_layout()

    # Calcular el límite superior del eje y
    y_max = max(canal_values) + 20  # Incrementa el límite superior en 20

    # Establecer los valores de las marcas en el eje y
    y_ticks = np.arange(0, y_max + 2)
    ax.set_yticks(y_ticks)

    # Mostrar los canales con menos de 5 redes conectadas
    canales_pocos_usados, canales_muchos_usados = encontrar_canales_pocos_muchos_usados(canal_count)
    ax.text(0.5, 0.95, f'Canales con menor congestion: {", ".join(map(str, canales_pocos_usados))}', ha='center', va='center', transform=ax.transAxes, fontsize=10)
    ax.text(0.5, 0.9, f'Canales con más congestion: {", ".join(map(str, canales_muchos_usados))}', ha='center', va='center', transform=ax.transAxes, fontsize=10)

    # Mostrar la figura en el frame
    widget_grafico_actual = FigureCanvasTkAgg(fig, master=frame)
    widget_grafico_actual.draw()
    widget_grafico_actual.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    # Crear la barra de herramientas
    toolbar = NavigationToolbar2Tk(widget_grafico_actual, frame)

    # Ocultar todos los botones excepto "Guardar"
    toolbar.update()
    for tool in toolbar.winfo_children():
        if isinstance(tool, tk.Button) and "Save" not in tool.cget('text'):
            tool.pack_forget()

    # Configurar manualmente el tamaño de la barra de herramientas
    toolbar.pack(side=tk.LEFT, padx=0, pady=0, anchor='center', expand=False)
    toolbar.pack_propagate(False)  # Evita que la barra de herramientas cambie de tamaño automáticamente
    toolbar.config(width=250, height=30)  # Establece el ancho y alto de la barra de herramientas

    return frame

def grafico_senal_vs_canal(frame):
    Msg = "Entro a ver grafico por señal vs canales"
    agregar_log(Msg)
    global grafica_actual
    global nombre_grafica
    nombre_grafica = "senal_vs_canal.png"
    # Leer los datos del archivo JSON
    datos = leer_datos_json()

    # Obtener los datos relevantes
    nombres = datos["NOMBRE"]
    canales = datos["CANAL"]
    señales = datos["SEÑAL"]

    # Crear una figura de Matplotlib
    fig = Figure(figsize=(10, 6))
    ax = fig.add_subplot(111)

    # Graficar los datos como un diagrama de dispersión
    scatter = ax.scatter(canales, señales, color='#4CAF50', alpha=0.6)

    # Agregar el nombre de la red al lado derecho de cada punto
    for nombre, canal, señal in zip(nombres, canales, señales):
        # Verificar si hay más de un nombre de red en el mismo canal y señal
        mismo_canal_señal = [(n, c) for n, c, s in zip(nombres, canales, señales) if c == canal and s == señal]
        if len(mismo_canal_señal) > 1:
            nombres_mismo_canal_señal = ', '.join(n for n, c in mismo_canal_señal)
            ax.text(canal, señal, nombres_mismo_canal_señal, fontsize=6, ha='left', va='center')
        else:
            ax.text(canal, señal, nombre, fontsize=6, ha='left', va='center')

    # Establecer etiquetas y título
    ax.set_xlabel('Canal')
    ax.set_ylabel('Señal Wi-Fi')
    ax.set_title('Diagrama de Dispersión de Señal vs Canal')

    # Ajustar el tamaño del gráfico para que ocupe todo el espacio disponible
    fig.tight_layout()
    grafica_actual = fig

    # Mostrar la figura en el frame
    widget_grafico_actual = FigureCanvasTkAgg(fig, master=frame)
    widget_grafico_actual.draw()
    widget_grafico_actual.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    # Crear la barra de herramientas
    toolbar = NavigationToolbar2Tk(widget_grafico_actual, frame)

    # Ocultar todos los botones excepto "Guardar"
    toolbar.update()
    for tool in toolbar.winfo_children():
        if isinstance(tool, tk.Button) and "Save" not in tool.cget('text'):
            tool.pack_forget()

    # Configurar manualmente el tamaño de la barra de herramientas
    toolbar.pack(side=tk.LEFT, padx=0, pady=0, anchor='center', expand=False)
    toolbar.pack_propagate(False)  # Evita que la barra de herramientas cambie de tamaño automáticamente
    toolbar.config(width=250, height=30)  # Establece el ancho y alto de la barra de herramientas

    return frame

def etiquetar_banda(frecuencia):
    frecuencia_float = float(frecuencia)
    if 2.4 <= frecuencia_float <= 2.4835:
        return "2.4 GHz"
    elif 5.1 <= frecuencia_float <= 5.9:
        return "5 GHz"
    else:
        return "Otra Banda"

def leer_datos_json():
    # Leer los datos del archivo JSON
    with open('lib/networks.json', 'r') as file:
        datos = json.load(file)
    return datos

def Barra_superior():
    Msg = "Entro a pantalla graficos"
    agregar_log(Msg)
    global ventana, barra_opcion, frame_centro
    ventana = tk.Toplevel()
    ventana.title("NetAplication V2 - Graficos NetWorks")
    
    ventana.state('zoomed')

    barra_opcion = tk.Frame(ventana, bg="white")
    barra_opcion.pack(side='top', fill='x')

    # Botón Home
    b_senal = tk.Label(barra_opcion, text='Graficar por', bg=Variables.c_barras, font=(Variables.poppins, 10))
    b_senal.pack(side='left', padx=10)
    b_senal.bind("<Button-1>", mostrar_ocultar_menu) #accion al hacer click en boton
    Perzonalizacion_botones.selecion_boton(b_senal)

    frame_centro = tk.Frame(ventana, bg="white")
    frame_centro.pack(side="left", fill="both", expand=True)
    
    # Conectar el evento de cierre de la ventana al método quit
    ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)

    ventana.mainloop()

def cerrar_ventana(): #solo cerrar la ventana con el titulo que quiero
    if ventana.wm_title() == "NetAplication V2 - Graficos NetWorks":
        ventana.destroy()

#BOTONES
def b_grafico_señal():
    Menus_funciones.cambio_ventana(grafico_señal, frame_centro)

def b_grafico_frecuencia():
    Menus_funciones.cambio_ventana(grafico_frecuencia, frame_centro)

def b_grafico_banda():
    Menus_funciones.cambio_ventana(grafico_banda, frame_centro)

def b_grafico_canales():
    Menus_funciones.cambio_ventana(grafico_canales, frame_centro)

def b_grafico_senal_vs_canal():
    Menus_funciones.cambio_ventana(grafico_senal_vs_canal, frame_centro)

# Menu boton Monitores
menu = tk.Menu(ventana, tearoff=0)
menu.add_command(label="Intensidad señal", command=b_grafico_señal, font=(Variables.poppins, 10))#se llama a la funcion Wireless
menu.add_command(label="Frecuencia", command=b_grafico_frecuencia, font=(Variables.poppins, 10)) #por hacer
menu.add_command(label="Canal", command=b_grafico_canales, font=(Variables.poppins, 10)) #por hacer
menu.add_command(label="Banda", command=b_grafico_banda, font=(Variables.poppins, 10)) #por hacer
menu.add_command(label="Señal vs Canal", command=b_grafico_senal_vs_canal, font=(Variables.poppins, 10)) #por hacer

def mostrar_opciones(event):
    global menu_visible

    # Obtener la posición del Label
    x = ventana.winfo_rootx() + event.widget.winfo_x()
    y = ventana.winfo_rooty() + event.widget.winfo_y() + event.widget.winfo_height() + 0

    ventana.after(200, lambda: menu.post(x, y))
    menu_visible = True

def mostrar_ocultar_menu(event):
    global menu_visible

    # Si el menú no está visible, se mostramos
    if not menu_visible:
        mostrar_opciones(event)
    # Si el menú está visible, no se mostramos
    else:
        menu.unpost()
        menu_visible = False

if __name__ == "__main__":
    Barra_superior()