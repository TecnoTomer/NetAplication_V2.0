import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from PIL import ImageTk, Image
import paramiko
import telnetlib3
import sys
import os
from cryptography.fernet import Fernet
import base64
import json
import re
import time
import subprocess
import telnetlib

import Variables
import Perzonalizacion_botones
import Alertas
from Logs import agregar_log

#varibales
instancia_ssh_actual = None 
lista_etiquetas_perfiles = []
MAX_PERFILES = 5

def Centro_conexiones(frame): 
    Msg = "Entro a pantalla de conexiones"
    agregar_log(Msg)
    # contenedor principal 
    C_conexiones_p = tk.Frame(frame, bg=Variables.c_centros)
    C_conexiones_p.pack(side="top", fill="both", expand=True)

    # Línea de separación entre subframes C_conexiones1 y C_conexiones2
    separacion = tk.PanedWindow(C_conexiones_p, bg=Variables.c_lina_separacion, orient="vertical", sashwidth=30, sashrelief="sunken")
    separacion.pack(side="top", fill="both", expand=True)
    
    # Agregar dos frames al PanedWindow
    global C_conexiones2
    C_conexiones1 = tk.Frame(separacion, bg=Variables.c_barras)
    C_conexiones2 = tk.Frame(separacion, bg="black")
    separacion.add(C_conexiones1)
    separacion.add(C_conexiones2)

    ######################################################
    #   seccion opciones subframe 1  dispositivos        #
    ######################################################
    sub_frame1 = tk.Frame(C_conexiones1, bg=Variables.c_centros, width=210, height=280) #la altura de aqui depente la pocision inicial de la barra separacion!
    sub_frame1.pack(side="left", fill="both", expand=False)

    dispositivos = tk.Label(sub_frame1, text="Dispositivos", bg=Variables.c_centros, font=(Variables.poppins_negrita, 12))
    dispositivos.place(x=50, y=10, width=100) 

    texto_con_punto = "• Windows\n• Unix\n• Cisco\n    - Switches\n    - Routers\n• Huawei\n    - Switches\n    - Routers"
    label_with_bullet = tk.Label(sub_frame1, text=texto_con_punto, justify=tk.LEFT, bg=Variables.c_centros, font=(Variables.poppins, 10))
    label_with_bullet.place(x=25, y=35, width=100)

    dispositivos = tk.Label(sub_frame1, text="Conexiones", bg=Variables.c_centros, font=(Variables.poppins_negrita, 12))
    dispositivos.place(x=50, y=180, width=100) 

    texto_con_punto = "• Ssh\n• Telnet\n• PowerShell\n• WinRS/WinRM"
    label_with_bullet = tk.Label(sub_frame1, text=texto_con_punto, justify=tk.LEFT, bg=Variables.c_centros, font=(Variables.poppins, 10))
    label_with_bullet.place(x=35, y=200, width=100)

    separacion1 = tk.Frame(C_conexiones1, bg=Variables.c_lina_separacion, width=5)
    separacion1.pack(side="left", fill="y")

    ######################################################
    #   seccion opciones subframe 2 establecer Conexion  #
    ######################################################

    sub_frame2 = tk.Frame(C_conexiones1, bg=Variables.c_barras, width=600)
    sub_frame2.pack(side="left", fill="both", expand=False)

    dispositivos = tk.Label(sub_frame2, text="Establecer Conexion", bg=Variables.c_barras, font=(Variables.poppins_negrita, 12))
    dispositivos.place(x=230, y=10, width=200) 

    Perfil = tk.Label(sub_frame2, text="Perfil:", bg=Variables.c_barras, font=(Variables.poppins, 10))
    Perfil.place(x=25, y=35) 

    global Perfil_entry
    Perfil_entry = tk.Entry(sub_frame2, bg="lightgray")
    Perfil_entry.place(x=100, y=36, width=145, height=20)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, 
        "Establece un nombre con el cual se guardara el perfil de la conexion.", 
        7, 36) 

    dispositivos = tk.Label(sub_frame2, text="Dispositivo:", bg=Variables.c_barras, font=(Variables.poppins, 10))
    dispositivos.place(x=25, y=70) 
    opciones_dispositivos = ["Windows", "Unix", "Switch", "Router"]
    canal = tk.StringVar()
    global combo_dispositivos
    combo_dispositivos = ttk.Combobox(sub_frame2, textvariable=canal, values=opciones_dispositivos)
    combo_dispositivos.place(x=100, y=71)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, "Elejir un dispositivo.", 7, 71)

    Protocolo = tk.Label(sub_frame2, text="Protocolo:", bg=Variables.c_barras, font=(Variables.poppins, 10))
    Protocolo.place(x=25, y=105) 
    opciones_Protocolo = ["Ssh", "Telnet", "PowerShell", "WinRS/WinRM"]
    canal = tk.StringVar()
    global combo_Protocolo
    combo_Protocolo = ttk.Combobox(sub_frame2, textvariable=canal, values=opciones_Protocolo)
    combo_Protocolo.place(x=100, y=106)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, "Elejir un protocolo de conexion.", 7, 106)

    Puerto = tk.Label(sub_frame2, text="Puerto:", bg=Variables.c_barras, font=(Variables.poppins, 10))
    Puerto.place(x=25, y=140) 
    global Puerto_entry
    Puerto_entry = tk.Entry(sub_frame2, bg="lightgray")
    Puerto_entry.place(x=100, y=141, width=145, height=20)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, 
        "Ingresar el numero del puerto por defecto o por el cual corre el servicio.", 
        7, 141)

    host_ip = tk.Label(sub_frame2, text="Host/Ip:", bg=Variables.c_barras, font=(Variables.poppins, 10))
    host_ip.place(x=25, y=175) 

    global host_ip_entry
    host_ip_entry = tk.Entry(sub_frame2, bg="lightgray")
    host_ip_entry.place(x=100, y=176, width=145, height=20)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, 
        "Ingresar la direccion IP o nombre del host destino.", 
        7, 176)

    usuario = tk.Label(sub_frame2, text="Usuario:", bg=Variables.c_barras, font=(Variables.poppins, 10))
    usuario.place(x=25, y=205) 
    global usuario_entry
    usuario_entry = tk.Entry(sub_frame2, bg="lightgray")
    usuario_entry.place(x=100, y=206, width=145, height=20)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, 
        "Ingresar el usuario de la session.", 
        7, 206)

    password = tk.Label(sub_frame2, text="Contraseña:", bg=Variables.c_barras, font=(Variables.poppins, 10))
    password.place(x=25, y=245) 
    global password_entry
    password_entry = tk.Entry(sub_frame2, bg="lightgray", show="*")
    password_entry.place(x=100, y=246, width=145, height=20)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, 
        "Ingresar la Contraseña del usuario de la sesion.", 
        7, 246)

    #BOTONES

    Boton_conectar = tk.Button(sub_frame2, text="Conectar", command=conectar, font=(Variables.poppins))
    Boton_conectar.place(x=400, y=45, width=140)
    Perzonalizacion_botones.selecion_boton(Boton_conectar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, 
        "Crea una sesion en el recuadro de Hosts, la cual dando click puedes escojer el modo de conexion.", 
        540, 50)

    Boton_guardar = tk.Button(sub_frame2, text="Guardar Perfil", command=B_guardar, font=(Variables.poppins))
    Boton_guardar.place(x=400, y=90, width=140)
    Perzonalizacion_botones.selecion_boton(Boton_guardar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, 
        "Guarda los datos de sesion en un archivo como perfil cifrado y seguro.", 
        540, 95)

    Boton_cargar = tk.Button(sub_frame2, text="Cargar Perfil", command=importar_desde_bin, font=(Variables.poppins))
    Boton_cargar.place(x=400, y=135, width=140)
    Perzonalizacion_botones.selecion_boton(Boton_cargar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, 
        "Carga un perfil guardado con anterioridad cifrado y seguro.", 
        540, 140)

    Boton_limpiar = tk.Button(sub_frame2, text="Limpiar Formulario", command=limpiar_casillas, font=(Variables.poppins))
    Boton_limpiar.place(x=400, y=180, width=140)
    Perzonalizacion_botones.selecion_boton(Boton_limpiar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, 
        "Limpia los datos ingresados en los campos para la conexion.", 
        540, 185)

    Boton_limpiar = tk.Button(sub_frame2, text="Limpiar Hosts", command=limpiar_perfiles, font=(Variables.poppins))
    Boton_limpiar.place(x=400, y=225, width=140)
    Perzonalizacion_botones.selecion_boton(Boton_limpiar)
    Perzonalizacion_botones.boton_ayuda(Variables.c_barras, sub_frame2, 
        "Limpia los perfiles cargados en el apartado de Hosts.", 
        540, 230)

    separacion2 = tk.Frame(C_conexiones1, bg=Variables.c_lina_separacion, width=5)
    separacion2.pack(side="left", fill="y")

    ######################################################
    #   seccion opciones subframe 2 hosts                #
    ######################################################
    global sub_frame3
    sub_frame3 = tk.Frame(C_conexiones1, bg=Variables.c_barras, width=0)
    sub_frame3.pack(side="left", fill="both", expand=True)

    dispositivos = tk.Label(sub_frame3, text="Hosts", bg=Variables.c_barras, font=(Variables.poppins_negrita, 12))
    dispositivos.place(x=230, y=10, width=80)

    return frame

def limpiar_casillas():# Función para limpiar todas las casillas de entrada
    perfil = Perfil_entry.get()
    dispositivo = combo_dispositivos.get()
    protocolo = combo_Protocolo.get()
    puerto = Puerto_entry.get()
    host_ip = host_ip_entry.get()
    usuario = usuario_entry.get()
    password = password_entry.get()
    # Verificar si todos los campos están completos
    if perfil or dispositivo or protocolo or puerto or host_ip or usuario or password:
        Perfil_entry.delete(0, tk.END)
        Puerto_entry.delete(0, tk.END)
        host_ip_entry.delete(0, tk.END)
        usuario_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        combo_dispositivos.set("")
        combo_Protocolo.set("")
        Msg = "Limpio registro de formulario conexiones"
        agregar_log(Msg)
    else:
        Msg = "No se detectan valores en las celdas que limpiar"
        Alertas.alerta_ok(Variables.titulo, Variables.alerta_aviso, Msg)

def guardar_datos_cifrados(perfil, dispositivo, protocolo, puerto, host_ip, usuario, password, clave_maestra, archivo):
    Msg = "Inicio guardado de datos cifrados"
    agregar_log(Msg)
    cifrador = Fernet(clave_maestra)

    # diccionario con datos a guardar
    datos_dict = {
        "perfil": perfil,
        "dispositivo": dispositivo,
        "protocolo": protocolo,
        "puerto": puerto,
        "host_ip": host_ip,
        "usuario": usuario,
        "password": password
    }

    # diccionarion a JSON
    datos_json = json.dumps(datos_dict)

    # Cifrar los datos
    datos_cifrados = cifrador.encrypt(datos_json.encode())

    # Guardar los datos cifrados en el archivo
    with open(archivo, "wb") as f:
        f.write(datos_cifrados)
        Msg = "El perfil cifrado se guardo correctamente"
        agregar_log(Msg)

def importar_desde_bin():
    Msg = "Inicio la importacion de un archivo con el perfil de la conexion"
    agregar_log(Msg)
    try:
        # Abrir el explorador de archivos para seleccionar el archivo .bin
        archivo_bin = filedialog.askopenfilename(filetypes=[("Archivos Binarios", "*.bin")])

        if len(Variables.Clave_maestra) != 32:
            raise ValueError("La clave maestra debe ser de 32 bytes")

        clave_maestra_codificada = base64.urlsafe_b64encode(Variables.Clave_maestra) # Codificar en base64 para obtener la clave Fernet válida

        cifrador = Fernet(clave_maestra_codificada) # Crear el objeto Fernet con la clave codificada

        # Leer datos
        with open(archivo_bin, 'rb') as file:
            datos_cifrados = file.read()

        datos_descifrados = cifrador.decrypt(datos_cifrados) # decodificar datos

        datos_dict = json.loads(datos_descifrados.decode('utf-8')) #JSON a diccionario
 
        # Obtener valores
        perfil = datos_dict.get('perfil', '')
        dispositivo = datos_dict.get('dispositivo', '')
        protocolo = datos_dict.get('protocolo', '')
        puerto = datos_dict.get('puerto', '')
        host_ip = datos_dict.get('host_ip', '')
        usuario = datos_dict.get('usuario', '')
        password = datos_dict.get('password', '')

        # Actualizar las variables de la interfaz gráfica con los valores obtenidos
        Perfil_entry.delete(0, 'end')
        Perfil_entry.insert(0, perfil)
        combo_dispositivos.set(dispositivo)
        combo_Protocolo.set(protocolo)
        Puerto_entry.delete(0, 'end')
        Puerto_entry.insert(0, puerto)
        host_ip_entry.delete(0, 'end')
        host_ip_entry.insert(0, host_ip)
        usuario_entry.delete(0, 'end')
        usuario_entry.insert(0, usuario)
        password_entry.delete(0, 'end')
        password_entry.insert(0, password)


    except Exception as e:
        Msg = f"Error al importar desde archivo binario: {e}"
        agregar_log(Msg)

def filter_ansi_escape(text):
    # Filtrar las secuencias de escape ANSI
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def B_guardar():
    perfil = Perfil_entry.get()
    dispositivo = combo_dispositivos.get()
    protocolo = combo_Protocolo.get()
    puerto = Puerto_entry.get()
    host_ip = host_ip_entry.get()
    usuario = usuario_entry.get()
    password = password_entry.get()
    # Verificar si todos los campos están completos
    if perfil and dispositivo and protocolo and puerto and host_ip and usuario and password:
        archivo = f"{perfil}.bin"
        rutacompleta = os.path.join(Variables.ruta_escritorio, archivo)
        guardar_datos_cifrados(perfil, dispositivo, protocolo, puerto, host_ip, usuario, password, Variables.clave_maestra, rutacompleta)
        Msg = f"Perfil de sesión guardado correctamente, en la ruta: {rutacompleta}, se guardan de forma encriptada asi que estara seguro!"
        Alertas.alerta_Amarilla(Variables.titulo, Variables.alerta_aviso, Msg)
    else:
        Msg = f"Te falta completar algunos campos antes de guardar el perfil"
        Alertas.alerta_Amarilla(Variables.titulo, Variables.alerta_aviso, Msg)

def limpiar_perfiles():
    global lista_etiquetas_perfiles

    if len(lista_etiquetas_perfiles) == 0:
        Msg = "No hay perfiles cargados."
        Alertas.alerta_Amarilla(Variables.titulo, Variables.alerta_aviso, Msg)
    else:
        # Limpiar los widgets de perfiles en sub_frame3
        for etiqueta_perfil in lista_etiquetas_perfiles:
            etiqueta_perfil.destroy()
        
        # Restaurar la lista de etiquetas de perfiles
        lista_etiquetas_perfiles = []
        
        # Reiniciar el contador o variable de recuento a cero
        VMAX_PERFILES = 0

        # Actualizar la lista de etiquetas en la interfaz de usuario
        actualizar_lista_etiquetas()

        Msg = "Se limpiaron los perfiles de conexiones"
        agregar_log(Msg)

def start_ssh_or_telnet(host, username, password, protocolo, port):
    if protocolo == "Ssh":
        Msg = "Inicio una conexion de administracion por el modulo putty"
        agregar_log(Msg)
        # Ruta completa al ejecutable PuTTY
        putty_path = r'lib\Emulator\putty.exe'

        # Construir el comando para iniciar la sesión SSH en PuTTY
        putty_command = f'{putty_path} -ssh {username}@{host} -pw {password}'

        # Ejecutar PuTTY con el comando
        subprocess.run(putty_command, shell=True)
    elif protocolo == "Telnet":
        Msg = "Inicio una conexión de administración por el modulo putty usando Telnet"
        agregar_log(Msg)
        # Ruta completa al ejecutable PuTTY
        putty_path = r'lib\Emulator\putty.exe'

        # Construir el comando para iniciar la sesión Telnet en PuTTY
        putty_command = f'{putty_path} -telnet {host} -P {port}'

        # Ejecutar PuTTY con el comando
        subprocess.run(putty_command, shell=True)

def cargar_imagen_dispositivo(dispositivo):
    ruta_imagen = None
    if dispositivo == "Windows":
        ruta_imagen = "lib/Data/Dispositivos/Windows.png"
    elif dispositivo == "Unix":
        ruta_imagen = "lib/Data/Dispositivos/Unix.png"
    elif dispositivo == "Switch":
        ruta_imagen = "lib/Data/Dispositivos/Switch.png"
    elif dispositivo == "Router":
        ruta_imagen = "lib/Data/Dispositivos/Router.png"
    
    if ruta_imagen:
        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen)
        return imagen_tk
    else:
        return None

def conectar(): #cuando de clic en boton conectar me crea el perfil en hosts
    Msg = "presiono en boton conectar, creando una sesion en el recuadro de Hosts"
    agregar_log(Msg)
    perfil = Perfil_entry.get()
    dispositivo = combo_dispositivos.get()
    global protocolo
    protocolo = combo_Protocolo.get()
    global puerto
    puerto = Puerto_entry.get()
    host_ip = host_ip_entry.get()
    usuario = usuario_entry.get()
    password = password_entry.get()

    # Verificar si todos los campos están completos
    if perfil and dispositivo and protocolo and puerto and host_ip and usuario and password:
        if len(lista_etiquetas_perfiles) >= MAX_PERFILES:
            # Si ya hay 5 perfiles, mostrar un mensaje de error y salir de la funcion
            Msg = "Se ha alcanzado el número máximo de perfiles (5)."
            Alertas.alerta_Amarilla(Variables.titulo, Variables.alerta_aviso, Msg)
            return

        def admin_or_consultar():
            global elecion
            elecion= tk.Toplevel()
            elecion.title("Seleccionar") #Titulo
            elecion.iconbitmap(Variables.icono_v) #icono
            n_ancho_elecion = Variables.ancho_p // 3
            n_alto_elecion = Variables.alto_p // 3
            elecion.geometry(f"{n_ancho_elecion}x{n_alto_elecion}") #aplicar zise a ventana
            elecion.resizable(0,0) #bloquear tamaño ventana
            tk.Label(elecion, text="¡Seleccione una Opcion de Conexion!").pack()

            Boton_admin = tk.Button(elecion, text="Conexion Administrativa", command=b_admin, font=(Variables.poppins))
            Boton_admin.place(x=90, y=40, width=250)
            Perzonalizacion_botones.selecion_boton(Boton_admin)

            Boton_consulta = tk.Button(elecion, text="Conexion Consultar", command=b_sonsulta, font=(Variables.poppins))
            Boton_consulta.place(x=90, y=80, width=250)
            Perzonalizacion_botones.selecion_boton(Boton_consulta)

        def b_admin():
            start_ssh_or_telnet(host_ip, usuario, password, protocolo, puerto)
            elecion.destroy()

        def b_sonsulta():
            crear_nueva_instancia()
            elecion.destroy()
            Msg = "Inicio una conexion de consulta desde el mismo aplicativo"
            agregar_log(Msg)

        # Función para crear una nueva instancia de SSHShellUI
        def crear_nueva_instancia():
            global instancia_ssh_actual
            # Destruir la instancia anterior de SSHShellUI si existe
            if instancia_ssh_actual:
                # Destruir los widgets dentro de la instancia anterior
                for widget in instancia_ssh_actual.master.winfo_children():
                    widget.destroy()

            # Destruir el contenido actual de C_conexiones2
            for widget in C_conexiones2.winfo_children():
                widget.destroy()

            # Crear una nueva instancia de SSHShellUI
            instancia_ssh_actual = SSHShellUI(C_conexiones2, perfil, protocolo, puerto, host_ip, usuario, password)

        # Mostrar el nombre único del perfil junto con la dirección IP y el usuario en sub_frame3
        nombre_perfil = f"{perfil}-{host_ip}-{usuario}"
        label_perfil = tk.Label(sub_frame3, bg=Variables.c_barras, font=(Variables.poppins_negrita, 12))
        Perzonalizacion_botones.selecion_boton(label_perfil)

        # Agregar la imagen del dispositivo a la izquierda del texto
        imagen_dispositivo = cargar_imagen_dispositivo(dispositivo)
        if imagen_dispositivo:
            label_perfil.img = imagen_dispositivo
            label_perfil.configure(image=imagen_dispositivo, compound="left")

        # Agregar el texto "Activo:" después de la imagen
        label_perfil.configure(text=f"Activo: {nombre_perfil}")

        # Establecer el color del texto a azul
        label_perfil.config(foreground="blue")

        # Subrayar el texto
        label_perfil.config(underline=True)

        # Agregar una línea debajo
        label_perfil.config(borderwidth=1, relief="solid")

        # Posicionar la etiqueta en una posición específica dentro del sub_frame3
        label_perfil.pack(side="top", padx=5, pady=5)

        # Agregar la etiqueta a la lista de etiquetas de perfiles
        lista_etiquetas_perfiles.append(label_perfil)

        # Asociar la acción a la etiqueta al hacer clic en ella
        label_perfil.bind("<Button-1>", lambda event: admin_or_consultar())

        # Actualizar la lista de etiquetas en la interfaz de usuario
        actualizar_lista_etiquetas()

    else:
        Msg = "Diligencie los campos necesarios para su tipo de conexión"
        Alertas.alerta_Amarilla(Variables.titulo, Variables.alerta_aviso, Msg)

def actualizar_lista_etiquetas():
    # Posicionar la lista de etiquetas en una posición específica dentro del sub_frame3
    for i, etiqueta_perfil in enumerate(lista_etiquetas_perfiles):
        etiqueta_perfil.place(x=30, y=40 + (i * 30), width=400)

class SSHShellUI:
    def __init__(self, master, perfil, protocolo, puerto, host_ip, usuario, password):
        self.master = master
        self.perfil = perfil
        self.protocolo = protocolo
        self.puerto = puerto
        self.host_ip = host_ip
        self.usuario = usuario
        self.password = password

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20, bg="black", foreground="green")
        self.text_area.pack(expand=True, fill="both")
        self.etiqueta = tk.Label(master, text="Ingresar comando", foreground="white", background="black", font=("Arial", 10))
        self.etiqueta.pack(side="left", padx=5, pady=5)
        
        self.entry = tk.Entry(master, width=80, font=("Arial", 10), bg="white", foreground="black")
        self.entry.pack(side="left", padx=5, pady=5)

        self.clear_button = tk.Button(master, text="Limpiar OutPut", command=self.limpiar_texto, font=("Arial", 10))
        self.clear_button.pack(side="left", padx=5, pady=5)

        self.entry.bind("<Return>", self.enviar_comando)  # Asociar la tecla Enter a la función enviar_comando

        if protocolo == "Ssh":
            self.cliente = self.iniciar_sesion_ssh()
        elif protocolo == "Telnet":
            self.cliente = self.iniciar_sesion_telnet()
        else:
            self.cliente = None

    def iniciar_sesion_ssh(self):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(self.host_ip, port=22, username=self.usuario, password=self.password)
            self.text_area.insert(tk.END, "Conexión SSH establecida.\n", "output")
            return ssh_client
        except Exception as e:
            self.text_area.insert(tk.END, f"Error al establecer conexión SSH: {e}\n")
            return None

    def iniciar_sesion_telnet(self):
        try:
            telnet_client = telnetlib.Telnet(self.host_ip, self.puerto)
            self.text_area.insert(tk.END, f"Conexión Telnet establecida en el puerto {self.puerto}.\n", "output")
            return telnet_client
        except Exception as e:
            self.text_area.insert(tk.END, f"Error al establecer conexión Telnet: {e}\n")
            return None


    def ejecutar_comando(self, comando):
        if not self.cliente:
            self.text_area.insert(tk.END, f"No se pudo establecer conexión {self.protocolo}.\n", "error")
            return

        try:
            if self.protocolo == "SSH":
                stdin, stdout, stderr = self.cliente.exec_command(comando)
                output = stdout.read().decode()
                error = stderr.read().decode()
            elif self.protocolo == "Telnet":
                self.cliente.write(comando.encode('ascii') + b'\n')
                output = self.cliente.read_until(b'#', timeout=1).decode('ascii')
                error = ""

            if output:
                self.text_area.insert(tk.END, output)
            if error:
                self.text_area.insert(tk.END, error)

        except Exception as e:
            self.text_area.insert(tk.END, f"Error al ejecutar comando: {e}\n")

    def enviar_comando(self, event):
        comando_usuario = self.entry.get()
        if comando_usuario.lower() == 'exit':
            # Limpiar los widgets
            for widget in self.master.winfo_children():
                widget.destroy()
            return

        self.ejecutar_comando(comando_usuario)
        self.entry.delete(0, tk.END)

    def limpiar_texto(self):
        self.text_area.delete(1.0, tk.END)