import subprocess #modulo para trabajar con procesos de en windows
import Variables #script con variables y funciones requeridas en varios puntos del programa!
import re #modulo para mannipular datos
import os #modulo para interactuar con el sistema operativo
import Alertas #script con las funciones de diferentes tipos de alertas!
import socket #modulo para funciones de red TCP/IP etc!
import psutil
import speedtest

from Logs import agregar_log

titulo = "Adaptador de Ethernet Ethernet:" 
titulo1 = "Adaptador de LAN inal mbrica Wi-Fi:"
titulo2 = "Adaptador de LAN inal mbrica Conexi¢n de  rea local* 1:"

def eliminar(archivo1): #funcion reutilizable para borrar cualquier archivo
    if os.path.exists(archivo1):
        os.remove(archivo1)
        Msg = f"Se elimino el archiv: {archivo1}"
        agregar_log(Msg)

def escanear(): #esta funcion ejecuta un comando ipconfig /all para sacar toda la infomacion en un archivo texto, datos que luego usare coo varibales
    # Ejecutar el comando 'ipconfig /all' y capturar la salida
    resultado = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
    resultado1 = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
    
    # Guardar la salida en un archivo de texto resultado
    with open("lib/data/temp/netp", 'w') as archivo:
        archivo.write(resultado.stdout)

    # Guardar la salida en un archivo de texto resultado1
    with open(Variables.conexion, 'w') as archivo:
        archivo.write(resultado1.stdout)

def eliminar_antes_de(): #funcion elimina cualquier cadena de caracteres que este antes del texto pasado como titulo
    #Leer el archivo procesado
    with open("lib/data/temp/netp", 'r') as archivo:
        lineas = archivo.readlines()

    try:
        #Encontrar la línea que contiene el título para Ethernet
        indice_titulo_eth = None
        for i, linea in enumerate(lineas):
            if titulo in linea:
                indice_titulo_eth = i
                break

        #Conservar solo las líneas después del título y guardar el resultado en un nuevo archivo
        lineas_limpas_eth = lineas[indice_titulo_eth:]

        with open("lib/data/temp/eth_temp", 'w') as archivo_limpiado_eth:
            archivo_limpiado_eth.writelines(lineas_limpas_eth)
    except:
        Msg = f"ocurrio un error durante la correcion de archivos Ethernet"
        agregar_log(Msg)

    try:
        # Encontrar la línea que contiene el título para Wireless
        indice_titulo_wireless = None
        for i, linea in enumerate(lineas):
            if titulo1 in linea:
                indice_titulo_wireless = i
                break

        # Conservar solo las líneas después del título y guardar el resultado en un nuevo archivo
        lineas_limpas_wireless = lineas[indice_titulo_wireless:]

        with open(Variables.wire, 'w') as archivo_limpiado_wireless:
            archivo_limpiado_wireless.writelines(lineas_limpas_wireless)
    except:
        Msg = f"ocurrio un error durante la correcion de archivos Wireless"
        agregar_log(Msg)

def eliminar_despues(): #funcion elimina cualquier texto despues del nombre del titulo (8,9,10)
    # Leer el archivo procesado
    with open("lib/data/temp/eth_temp", 'r') as archivo:
        lineas = archivo.readlines()

    try:
        # Encontrar la línea que contiene el título
        indice_titulo = None
        for j, linea in enumerate(lineas):
            if titulo2 in linea:
                indice_titulo = j
                break

        # Conservar solo las líneas antes del título y guardar el resultado en un nuevo archivo
        lineas_limpas = lineas[:indice_titulo]

        with open(Variables.eth, 'w') as archivo_limpiado:
            archivo_limpiado.writelines(lineas_limpas)
    except:
        Msg = f"Error al procesar el título para el archivo {i+1}"
        agregar_log(Msg)

def obtener_variable(archivo, titulo): #aqui se lee el documentos del output del comando cmd se le pasa eldocumento y el texto a buscar luego del texto ':' el valor despues de ese signo seria el valor de esa varibale
    with open(archivo, 'r') as f:
        for linea in f:
            if titulo in linea:
                valor = linea.split(':')[-1].strip()
                return valor

def buscar_direccion_ip(eth, wire, conexion): #aqui se saca varios datos de estos archivos, ip, ssid, estado etc etc!
    #buscar en archivo eth si la ip esta ahi!
    Msg = f"Se inicio recolecion de algunos datos necesarios"
    agregar_log(Msg)
    Variables.D_ip = obtener_variable(eth, "Direcci¢n IPv4")
    if Variables.D_ip and any(char.isdigit() for char in Variables.D_ip): #si dentro de la cadena str hay numeros entonces se toma como valido!
        Variables.net_stado = "conectado"
        Variables.drive = "Ethernet" # dato salio de la int eth
        Variables.v_canal = "N/D"
        Variables.v_señal = "N/D"
        Variables.v_recepcion = "N/D"
        Variables.v_transmision = "N/D"
        #Variables.net_ssid = "Ethernet"
        try:
            # Ejecutar el comando PowerShell para obtener el nombre de la red
            comando_powershell = 'Get-NetConnectionProfile | Where-Object {$_.InterfaceAlias -eq "Ethernet"} | Select-Object -ExpandProperty Name'
            resultado_powershell = subprocess.run(['powershell', comando_powershell], capture_output=True, text=True, check=True)

            # Obtener el nombre de la red desde la salida de PowerShell
            Variables.net_ssid = resultado_powershell.stdout.strip()

        except subprocess.CalledProcessError as e:
            Msg = f"Error al obtener el nombre de la red: {e}"
            agregar_log(Msg)
            return None

        if "(Preferido)" in Variables.D_ip: #si la ip tiene el texto (Preferido) eliminarlo!
            Variables.D_ip = Variables.D_ip.replace("(Preferido)", "")
        # Buscar DNS en archivo wire
        Variables.v_dns = obtener_variable(eth, "Sufijo DNS espec¡fico para la conexi¢n")

        # Verificar si la variable está vacía o contiene solo espacios en blanco
        if Variables.v_dns.isspace() or not Variables.v_dns:
            # La variable está vacía o contiene solo espacios en blanco, asignar "N/A"
            Variables.v_dns = "N/A"
    else:
        Variables.net_ssid = obtener_variable(conexion, "SSID")
        Variables.v_canal = obtener_variable(conexion, "Canal")
        Variables.v_señal = obtener_variable(conexion, "Se¤al ")
        Variables.v_recepcion = obtener_variable(conexion, "Velocidad de recepci¢n (Mbps)")
        Variables.v_transmision = obtener_variable(conexion, "Velocidad de transmisi¢n (Mbps)")

        # Buscar en archivo wire si la ip esta ahi!
        Variables.D_ip = obtener_variable(wire, "Direcci¢n IPv4")
        if Variables.D_ip and any(char.isdigit() for char in Variables.D_ip):
            # Si el valor contiene caracteres numéricos, tomarlo como válido
            Variables.net_stado = "conectado"
            Variables.drive = "Wi-Fi"
            if "(Preferido)" in Variables.D_ip:
                Variables.D_ip = Variables.D_ip.replace("(Preferido)", "")
            #buscar dns sufijo en archivo wire!
            Variables.v_dns = obtener_variable(wire, "Sufijo DNS espec¡fico para la conexi¢n")
            # Verificar si la variable está vacía o contiene solo espacios en blanco
            if Variables.v_dns.isspace() or not Variables.v_dns:
                # La variable está vacía o contiene solo espacios en blanco, asignar "N/A"
                Variables.v_dns = "N/A"
        else:
            Variables.D_ip = "127.0.0.1"
            Variables.drive = "N/A"
            Variables.net_ssid = "N/A"
            Variables.v_dns = "N/A"
            Variables.net_stado = "desconectado"
            Variables.v_recepcion = "N/D"
            Variables.v_transmision = "N/D"
            Msg = f"No se detecto conexion por {Variables.drive}, se aplicaron valores 'N/D' o 'N/A' por defecto"
            agregar_log(Msg)

def obtener_ip(): #aqui se obtiene la ip actual, para luego verificar si cambio de red
    try:
        # Obtener el nombre del host
        host_name = socket.gethostname()

        # Obtener la dirección IP del host
        ip_address = socket.gethostbyname(host_name)

        return ip_address

    except socket.error as e:
        Variables.D_ip = "127.0.0.1"
        Msg = f"Ha ocurrido un error {e}"
        agregar_log(Msg)
        return Variables.D_ip

def verificar_cambio_de_red(etiqueta): #aqui se actualizan los datos despues de que se desconecta o conecta a una nueva red
    obtener_data_net()
    nueva_ip = obtener_ip()
    if nueva_ip != Variables.D_ip:
        buscar_direccion_ip(Variables.eth, Variables.wire, Variables.conexion)
        Variables.D_ip = nueva_ip
    else:
        pass

    #texto = f"{Variables.v_dns}/{Variables.nombre_usuario}     Net: {Variables.net_stado}/{Variables.drive}/{Variables.net_ssid}/{Variables.D_ip}     Rx = ({Variables.v_recepcion}) Mbps     Tx = ({Variables.v_transmision}) Mbps"
    texto = f"Dns: {Variables.v_dns}     User: {Variables.nombre_usuario}     Estado: {Variables.net_stado}     Señal: {Variables.v_señal}     Canal: {Variables.v_canal}     Adaptador: {Variables.drive}     Nombre: {Variables.net_ssid}     Ip: {Variables.D_ip}     Rx = ({Variables.v_recepcion}) Mbps     Tx = ({Variables.v_transmision}) Mbps"
    etiqueta.config(text=texto)
    etiqueta.after(5000, lambda: verificar_cambio_de_red(etiqueta))

def obtener_data_net(): #se pone todo a funcionar
    Msg = "Obtencion de data inicada"
    agregar_log(Msg)

    escanear()
    eliminar_antes_de()
    eliminar_despues()
    eliminar("lib/data/temp/eth_temp")
    eliminar("lib/data/temp/netp")
    buscar_direccion_ip(Variables.eth, Variables.wire, Variables.conexion)
    Msg = "Obtencion de data finalizada"
    agregar_log(Msg)