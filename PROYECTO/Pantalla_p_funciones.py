import tkinter as tk
import subprocess
import psutil

import Variables
import Perzonalizacion_botones
import Menus_funciones
import Net_datos_funciones
import Home_funciones
import Conexiones_funciones
from Battery_funciones import stop_server
from Logs import agregar_log

def Barra_superior():
	#  BARRA SUPERIOR
	barra_opcion = tk.Frame(Variables.root, bg=Variables.c_barras)
	barra_opcion.pack(side='top', fill='x')

	# Boton Home
	b_home = tk.Label(barra_opcion, text='Home', bg=Variables.c_barras, width=10, font=(Variables.poppins, 10)) #boton Monitores
	b_home.pack(side='left', padx=0)
	b_home.bind("<Button-1>", Menus_funciones.B_home) #accion al hacer click en boton
	Perzonalizacion_botones.selecion_boton(b_home) #efecto al selecionar boton

	# Boton Monitores
	b_conexiones = tk.Label(barra_opcion, text='Conexiones', bg=Variables.c_barras, width=10, font=(Variables.poppins, 10)) #boton Monitores
	b_conexiones.pack(side='left', padx=0)
	b_conexiones.bind("<Button-1>", Menus_funciones.B_conexiones) #accion al hacer click en boton
	Perzonalizacion_botones.selecion_boton(b_conexiones) #efecto al selecionar boton

	# Boton Monitores
	b_scanners = tk.Label(barra_opcion, text='Monitores', bg=Variables.c_barras, width=10, font=(Variables.poppins, 10)) #boton Monitores
	b_scanners.pack(side='left', padx=0)
	b_scanners.bind("<Button-1>", Menus_funciones.mostrar_ocultar_menu) #accion al hacer click en boton
	Perzonalizacion_botones.selecion_boton(b_scanners) #efecto al selecionar boton

	#boton ayuda
	b_ayuda = tk.Label(barra_opcion, text='Ayuda', bg=Variables.c_barras, width=10, font=(Variables.poppins, 10)) #boton ayuda
	Perzonalizacion_botones.selecion_boton(b_ayuda) #efecto al selecionar boton
	b_ayuda.pack(side='left', padx=0)
	b_ayuda.bind("<Button-1>", Menus_funciones.B_ayuda) #accion al hacer click en boton

	#boton ayuda
	b_ayuda = tk.Label(barra_opcion, text=f'{Variables.Host_nombre} / {Variables.nombre_usuario}', bg=Variables.c_barras) #boton ayuda
	b_ayuda.pack(side='right', padx=10)

	
	Msg = "Barra superior cargada correctamente"
	agregar_log(Msg)

def Barra_inferior():
	# BARRA IINFERIOR
	barra_estado = tk.Frame(Variables.root, bg=Variables.c_barras)
	barra_estado.pack(side='bottom', fill='x')

	#etiqueta que muestra fecha y hora actualizada cada 30 segundos
	global etiqueta1
	etiqueta1 = tk.Label(barra_estado, text="", bg=Variables.c_barras)
	etiqueta1.pack(side='right', padx=10)
	Variables.obtener_fecha_hora(etiqueta1) #obtiene y actualiza la fecha y hora cada 30 segundos en la barra inferior
	
	global etiqueta2 # parte de la barra inferiro donde se muestra los datos de la conexcion red
	etiqueta2 = tk.Label(barra_estado, text="", bg=Variables.c_barras)
	etiqueta2.pack(side="left", padx=10)
	Net_datos_funciones.verificar_cambio_de_red(etiqueta2) #obtiene y actualiza datos de la red

	Msg = "Barra inferior cargada correctamente"
	agregar_log(Msg)

def on_cerrar_ventana():
	Net_datos_funciones.eliminar(Variables.Excel_wifi_lleno) #elimina el archivo que ocontiene el scan del wifi!
	stop_server()
	Variables.root.destroy()  # Cierra la ventana principal

def HoldingScreen():
    Msg = "Inicializando el Screen_Holdin"
    agregar_log(Msg)
    subprocess.run(["lib/Screen_Holdin.exe"])

def crear_windows_principal(titulo, icono): #funcion inicia el programa principal! root
	Msg = "Finalizo el Screen_Holdin correctamente"
	agregar_log(Msg)

	Variables.root.title(titulo) #Titulo
	Msg = f"Titulo: {titulo}, aplicado"
	agregar_log(Msg)

	Variables.root.iconbitmap(icono) #icono
	Msg = "Icono aplicado"
	agregar_log(Msg)

	n_alto_p = Variables.alto_p - Variables.barra_tareas #nuevo tamaño ancho para la ventana principal
	Msg = f"Tamaño ventana: {n_alto_p}, aplicado"
	agregar_log(Msg)

	Variables.root.geometry(f"{Variables.ancho_p}x{n_alto_p}") #aplicar zise a ventana
	Variables.root.resizable(0,1) #bloquear tamaño ventana ancho, alto
	Variables.root.state('zoomed') #abrir la ventana maximizada
	Msg = "Variables aplicadas correctamente"
	agregar_log(Msg)

	Net_datos_funciones.obtener_data_net()
	
	Barra_superior()
	Home_funciones.Centro_principal(Variables.root)
	Barra_inferior()

	Variables.root.mainloop() #inicializar loop ventana root