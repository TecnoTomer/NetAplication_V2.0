import tkinter as tk
from  tkinter import ttk
import pandas as pd
import time
import keyboard

import Wireless_scanner
import Graficas_funciones
import Perzonalizacion_botones
import Variables
import Alertas
import pyperclip
import key_comands
from Logs import agregar_log

def start_resize_linea1(self, _):

    self.start_x_linea1 = _.x_root

    self.start_sash_linea1 = self.linea1.sash_coord(0)

    self.C_wireless1.bind("<B1-Motion>", self.resize_linea1)

def resize_linea1(self, event):
    #desplazamiento del ratón
    delta_x = event.x_root - self.start_x_linea1

    # Calcular la nueva posición de la línea de separación en C_wireless1
    new_sash_linea1 = self.start_sash_linea1 + delta_x

    # Ajustar la posición de la línea de separación en C_wireless1
    self.linea1.sash_place(0, new_sash_linea1, new_sash_linea1)

    # Redistribuir los tamaños de los frames en C_wireless1
    self.linea1.update()

def Centro_wireless(frame): 
    Msg = "Se entro a pantalla Wireless_scanner"
    agregar_log(Msg)
    # Crear el contenedor principal 
    C_wireless1_p = tk.Frame(frame, bg=Variables.c_centros)
    C_wireless1_p.pack(side="top", fill="both", expand=True)

    # Línea de separación entre subframes C_wireless1 y C_wireless2
    separacion = tk.PanedWindow(C_wireless1_p, bg=Variables.c_lina_separacion, orient="vertical", sashwidth=5, sashrelief="sunken")
    separacion.pack(side="top", fill="both", expand=True)

    # Agregar dos frames al PanedWindow
    C_wireless1 = tk.Frame(separacion, bg=Variables.c_centros)
    C_wireless2 = tk.Frame(separacion, bg=Variables.c_barras)
    separacion.add(C_wireless1)
    separacion.add(C_wireless2)

    ######################################################
    #   Seccion frame del centro                         #
    ######################################################
    global view_data
    #al inicio mostramos la lista vacida creando un treeview vacido
    view_data = Wireless_scanner.crear_treeview(C_wireless2)

    # Obtener el ancho de C_wireless1
    ancho_c_wireless1 = frame.winfo_width()
    global ancho_subframes
    ancho_subframes = ancho_c_wireless1 // 3 #dividir valor en 3
    ######################################################
    #   seccion de Opciones de Escaneo subframe 1        #
    ######################################################
    sub_frame1 = tk.Frame(C_wireless1, bg=Variables.c_centros, width=ancho_subframes, height=300)
    sub_frame1.pack(side="left", fill="both", expand=True)

    # Objectos del subframe 1
    etiqueta1 = tk.Label(sub_frame1, text="Opciones de Escaneo", bg=Variables.c_centros, font=(Variables.poppins_negrita, 12))
    etiqueta1.place(x=5, y=5, width=ancho_subframes) 

    # Botón para buscar el ComboBox con las interfaces Wi-Fi
    boton_actualizar = tk.Button(sub_frame1, text="Buscar Interfaces", command=Wireless_scanner.actualizar_combobox, font=(Variables.poppins, 9))
    boton_actualizar.place(x=15, y=40)
    Perzonalizacion_botones.selecion_boton(boton_actualizar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_centros, sub_frame1, 
    "Presiona 'Buscar interfaces' para buscar las interfaces wifi que tengas actualmente luego presiona el boton de 'Iniciar Escaneo'", 124, 42) 
    

    # ComboBox para seleccionar una interfaz Wi-Fi
    canal = tk.StringVar()
    global combo_int
    combo_int = ttk.Combobox(sub_frame1, textvariable=canal)
    combo_int.place(x= 180, y= 40, width=270, height=25)
    
    # Botón para iniciar escaneo
    boton_escaneo = tk.Button(sub_frame1, text="Iniciar Escaneo", 
        command=B_Iniciar_Escaneo, font=(Variables.poppins, 9))
    boton_escaneo.place(x=15, y=80)
    Perzonalizacion_botones.selecion_boton(boton_escaneo)
    Perzonalizacion_botones.boton_ayuda(Variables.c_centros, sub_frame1, 
    "Este botón inicia el escaneo y puede tardar un máximo de 30 segundos. Una vez que haya finalizado, haz clic en 'Actualizar Output'.", 124, 82) 
    
    # Botón para Actualizar Escaneo
    boton_actualizar = tk.Button(sub_frame1, text="Actualizar OutPut", 
        command=B_actualizar_output, font=(Variables.poppins, 9))
    boton_actualizar.place(x=15, y=120)
    Perzonalizacion_botones.selecion_boton(boton_actualizar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_centros, sub_frame1, 
    "Este botón actualiza la salida después de cada escaneo o al importar un archivo.", 124, 122)

    # Botón para limpiar output
    boton_limpiar = tk.Button(sub_frame1, text="Limpiar OutPut", 
        command=B_limpiar_output, font=(Variables.poppins, 9))
    boton_limpiar.place(x=15, y=160)
    Perzonalizacion_botones.selecion_boton(boton_limpiar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_centros, sub_frame1, 
    "Este botón borra el resultado (Output).", 124, 162)
    
    #mostrar informacion en texto!
    global total_redes
    total_redes = tk.Label(sub_frame1, text="", bg=Variables.c_centros, font=(Variables.poppins, 9))
    total_redes.place(x=250 , y=82)
    Wireless_scanner.recuento_escaneados(total_redes)

    #mostrar informacion redes mostrada en treeview
    total_redes_treeview = tk.Label(sub_frame1, text="", bg=Variables.c_centros, font=(Variables.poppins, 9))
    total_redes_treeview.place(x=250 , y=122)
    Wireless_scanner.recuento(total_redes_treeview, view_data)

    #mostrar datos selecionados
    total_seleccion = tk.Label(sub_frame1, text="", bg=Variables.c_centros, font=(Variables.poppins, 9))
    total_seleccion.place(x=250 , y=162)
    Wireless_scanner.obtener_seleccion(view_data, total_seleccion)

    separacion2 = tk.Frame(C_wireless1, bg=Variables.c_lina_separacion, width=5)
    separacion2.pack(side="left", fill="y")

    ######################################################
    #   seccion de Opciones de Datos subframe 2          #
    ######################################################
    sub_frame2 = tk.Frame(C_wireless1, bg=Variables.c_centros, width=ancho_subframes)
    sub_frame2.pack(side="left", fill="both", expand=True)

    #objectos frame 2
    etiqueta2 = tk.Label(sub_frame2, text="Opciones de Datos", bg=Variables.c_centros, font=(Variables.poppins_negrita, 12))
    etiqueta2.place(x=5, y=5, width=ancho_subframes)

    # Botón para exportar
    boton_exportar = tk.Button(sub_frame2, text="Exportar Datos", 
        command=B_exportar_output, font=(Variables.poppins, 9))
    boton_exportar.place(x=15, y=40)
    Perzonalizacion_botones.selecion_boton(boton_exportar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_centros, sub_frame2, 
    "Este botón exporta los datos del output a un archivo Excel para su análisis posterior.", 124, 42)

    # Botón para Importar
    boton_Importar = tk.Button(sub_frame2, text="Importar Datos", command=B_importar, font=(Variables.poppins, 9))
    boton_Importar.place(x=15, y=80)
    Perzonalizacion_botones.selecion_boton(boton_Importar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_centros, sub_frame2,
    "Este botón se utiliza para importar los datos previamente exportados.", 124, 82)

    # Botón para copiar al portapapeles
    boton_Seleccionar = tk.Button(sub_frame2, text="Seleccionar Todo", command=B_copar_todo_portapapeles, font=(Variables.poppins, 9))
    boton_Seleccionar.place(x=15, y=120)
    Perzonalizacion_botones.selecion_boton(boton_Seleccionar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_centros, sub_frame2, 
    "Este botón sirve para seleccionar todos los datos del output.", 124, 122)

    # Botón para Copiar Seleccion Al Portapapeles
    boton_copiar_selec = tk.Button(sub_frame2, text="Copiar Seleccion", command=B_copar_selecion_portapapeles, font=(Variables.poppins, 9))
    boton_copiar_selec.place(x=15, y=160)
    Perzonalizacion_botones.selecion_boton(boton_copiar_selec)
    Perzonalizacion_botones.boton_ayuda(Variables.c_centros, sub_frame2, 
    "Usa 'Ctrl' y mouse, para copiar un dato o selecciona un rango sosteniendo 'Ctrl' o usando 'Shift'. Luego, haz clic en 'Copiar Seleccion', o presionando 'Ctrl + C'.", 124, 162)

    # Botón para graficar datos
    boton_copiar_selec = tk.Button(sub_frame2, text="Graficar Datos", command=Graficas_funciones.Barra_superior, font=(Variables.poppins, 9))
    boton_copiar_selec.place(x=15, y=200)
    Perzonalizacion_botones.selecion_boton(boton_copiar_selec)
    Perzonalizacion_botones.boton_ayuda(Variables.c_centros, sub_frame2, 
    "Este botón muestra en graficos los datos que actual se encuentran en el OutPut", 124, 202)


    separacion3 = tk.Frame(C_wireless1, bg=Variables.c_lina_separacion, width=5)
    separacion3.pack(side="left", fill="y")

    ######################################################
    #   seccion de Opciones de Filtros subframe 3        #
    ######################################################
    sub_frame3 = tk.Frame(C_wireless1, bg=Variables.c_centros, width=ancho_subframes)
    sub_frame3.pack(side="left", fill="both", expand=True)

    #objectos frame 3
    etiqueta3 = tk.Label(sub_frame3, text="Opciones de Filtros", bg=Variables.c_centros, font=(Variables.poppins_negrita, 12))
    etiqueta3.place(x=5, y=5, width=442, height=25)

    # Botón para ordenar
    boton_Ordenar = tk.Button(sub_frame3, text="Ordenar Datos", command=B_ordenar, font=(Variables.poppins, 9))
    boton_Ordenar.place(x=15, y=40)
    Perzonalizacion_botones.selecion_boton(boton_Ordenar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_centros, sub_frame3, "Ordenar datos del output desde la A - Z.", 125, 42)

    # Botón para filtar por señal
    boton_señal = tk.Button(sub_frame3, text="Intensidad Señal", command=B_ordenar_intensidad, font=(Variables.poppins, 9))
    boton_señal.place(x=15, y=80)
    Perzonalizacion_botones.selecion_boton(boton_señal)
    Perzonalizacion_botones.boton_ayuda_izquierda(Variables.c_centros, sub_frame3, "Filtar datos por Intensidad de señal mas fuerte a mas debil.", 125, 82)

    # Botón para filtrar por Seguridad
    boton_seguridad = tk.Label(sub_frame3, text="Seguridad", bg=Variables.c_centros, font=(Variables.poppins)) # por ejemplo, WPA2, WPA3
    boton_seguridad.place(x=15, y=120)
    # Lista de opciones de seguridad
    opciones_seguridad = ["FREE", "WEP", "WPA", "WPA2", "WPA3"]
    canal = tk.StringVar()
    global combo_seguridad
    combo_seguridad = ttk.Combobox(sub_frame3, textvariable=canal, values=opciones_seguridad)
    combo_seguridad.place(x=100, y=120)
    Perzonalizacion_botones.boton_ayuda(Variables.c_centros, sub_frame3, "Filtar por tipo de seguridad de la red.", 254, 121)
    
    # Botónes para filtrar por bandas
    boton_bandas = tk.Label(sub_frame3, text="Bandas", bg=Variables.c_centros, font=(Variables.poppins)) 
    boton_bandas.place(x=15, y=160)
    # Checkbutton para filtrar por banda
    global var_canal_2
    var_canal_2 = tk.IntVar() # variable para almacenar el estado del checkbox
    check_canal = tk.Checkbutton(sub_frame3, text="2.4 GHz", variable=var_canal_2, bg=Variables.c_barras, font=(Variables.poppins))
    check_canal.place(x=100, y=160)
    # Checkbutton para filtrar por banda
    global var_canal_5
    var_canal_5 = tk.IntVar() # variable para almacenar el estado del checkbox
    check_canal = tk.Checkbutton(sub_frame3, text="5 GHz", variable=var_canal_5, bg=Variables.c_barras, font=(Variables.poppins))
    check_canal.place(x=180, y=160)
    Perzonalizacion_botones.boton_ayuda_izquierda(Variables.c_centros, sub_frame3, "Filtar por tipo de banda de la red.", 254, 161)
    
    # Botón para filtrar por canal
    boton_canal = tk.Label(sub_frame3, text="Canal", bg=Variables.c_centros, font=(Variables.poppins))
    boton_canal.place(x=15, y=200)

    # Lista de números del 1 al 14
    numeros = list(range(1, 15))
    global combo_canal
    canal = tk.StringVar() 
    combo_canal = ttk.Combobox(sub_frame3, textvariable=canal, values=numeros)
    combo_canal.place(x=100, y=200)
    Perzonalizacion_botones.boton_ayuda_izquierda(Variables.c_centros, sub_frame3, "Filtar por tipo de canal de la red.", 254, 201)

    # Botón para filtar
    boton_filtar = tk.Button(sub_frame3, text="Aplicar Filtros", command=B_aplicar_filtros, font=(Variables.poppins, 9))
    boton_filtar.place(x=15, y=240)
    Perzonalizacion_botones.selecion_boton(boton_filtar)
    Perzonalizacion_botones.boton_ayuda_izquierda(Variables.c_centros, sub_frame3, "Una ves seleciones uno o mas filtros aplicalos dando click aqui!.", 102, 242)
    
    Msg = "Se cargaron textos, titulos, iconos , botones, y etc de la ventana"
    agregar_log(Msg)

    keyboard.hook(key_comands.on_key_event)
    
    return frame

#########################
        #BOTONES
#########################
#BOTONES OPCIONES ESCANEO
def B_Iniciar_Escaneo():
    Msg = "Se inicio el escaneo de redes"
    agregar_log(Msg)
    inter = Wireless_scanner.obtener_indice_int(combo_int)
    interfas_selecionada_combobox = combo_int.get()
    if not interfas_selecionada_combobox:
        Msg = "Por favor, selecciona una interfaz antes de iniciar el escaneo."
        Alertas.alerta_aceptar(Variables.titulo, Variables.alerta_error, Msg)
        Msg = "Se intento iniciar escaner pero no seleciono interfaz"
        agregar_log(Msg)
        return
    Msg = "Tenga en cuenta que este escaneo de red puede no ser 100% preciso, ya que depende de factores de SOFTWARE Y HARDWARE del equipo"
    Alertas.alerta_Amarilla(Variables.titulo, Variables.alerta_aviso, Msg)
    Msg = f"Se detecto la interfaz {interfas_selecionada_combobox}, se inicio el escaneo"
    agregar_log(Msg)
    Wireless_scanner.scan_wifi(inter) #escanea todas las redes wifi del alcance

def B_actualizar_output():
    Wireless_scanner.actualizar_datos(view_data, Variables.Excel_wifi_lleno)
    Wireless_scanner.guardar_datos_en_json(view_data)
    Msg = "Se actualizaron los valores en el output"
    agregar_log(Msg)

def B_limpiar_output():
    Wireless_scanner.limpiar_datos(view_data)
    Msg = "Se limpiaron los valores en el output"
    agregar_log(Msg)

#BOTONES OPCIONES DATOS
def B_exportar_output():
    Wireless_scanner.exportar_a_excel(Variables.Excel_wifi_lleno, Variables.Excel_wifi_exportado)
    Msg = "Se se exportaron valores del escaneo wireless"
    agregar_log(Msg)

def B_importar():
    Wireless_scanner.importar_desde_excel(view_data)
    Wireless_scanner.guardar_datos_en_json(view_data)
    Msg = "Se inicio la importacion de un documento con un registro de escaneo externo"
    agregar_log(Msg)

def B_copar_todo_portapapeles():
    Wireless_scanner.seleccionar_todos_los_elementos(view_data)
    Msg = "Se copiaron todos los datos al portapapeles"
    agregar_log(Msg)

def B_copar_selecion_portapapeles():
    Wireless_scanner.copiar_seleccion_al_portapapeles(view_data)
    Msg = "Se copio la selecion al portapapeles"
    agregar_log(Msg)

#def B_graficar_datos_treeview():

#BOTONES OPCIONES FILTROS
def B_ordenar():
    Wireless_scanner.ordenar_por_columna(view_data, 0)
    Msg = "Se ordenaron los datos por nombre de la A - Z"
    agregar_log(Msg)

def B_ordenar_intensidad():
    Wireless_scanner.ordenar_por_intensidad(view_data)
    Msg = "Se ordenaron los datos por intensidad de señal"
    agregar_log(Msg)

def B_aplicar_filtros():
    # Verificar si el Treeview tiene elementos y aplicar filtros
    if view_data.get_children():
        seguridad_seleccionada = combo_seguridad.get()
        canal_seleccionado = combo_canal.get()

        B_actualizar_output()
        time.sleep(2)

        # Verificar si las variables tienen valores antes de aplicar los filtros
        if seguridad_seleccionada:
            Wireless_scanner.aplicar_filtro_seguridad(view_data, seguridad_seleccionada)

        if var_canal_2.get() or var_canal_5.get():
            Wireless_scanner.aplicar_filtro_banda(view_data, var_canal_2, var_canal_5)

        if canal_seleccionado:
            Wireless_scanner.aplicar_filtro_canal(view_data, canal_seleccionado)
        Msg = "se aplicaron filtros del output de redes wireless"
        agregar_log(Msg)

        Wireless_scanner.guardar_datos_en_json(view_data)
    else:
        Msg = "No hay datos en el OutPut"
        Alertas.alerta_ok(Variables.titulo, Variables.alerta_aviso, Msg)
        Msg = "Intento aplicar filtros pero no se detectaton datos en el output"
        agregar_log(Msg)
        pass