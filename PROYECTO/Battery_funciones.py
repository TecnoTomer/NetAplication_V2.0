import threading
import subprocess
import webbrowser
import http.server
import socketserver
import os

from Logs import agregar_log

ruta = "lib/data/Report.html"
server_thread = None

def generate_battery_report():
    subprocess.run(["powercfg", "/batteryreport", "/output", ruta], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    Msg = "Se genero un reporte de bateria"
    agregar_log(Msg)

def open_in_browser():
    # Generar el informe de la batería y limpiar el archivo HTML
    generate_battery_report()

    # Definir el manejador de solicitud HTTP
    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory="lib/data", **kwargs)

    global server_thread
    # Crear un servidor HTTP en el puerto 8000
    with socketserver.TCPServer(("", 8000), MyHttpRequestHandler) as httpd:
        print("Servidor web iniciado en el puerto 8000...")
        # Abrir el navegador web con la página generada
        webbrowser.open("http://localhost:8000/Report.html")
        # Escuchar las solicitudes entrantes hasta que se interrumpa
        httpd.serve_forever()

def start_server():
    global server_thread
    Msg = "Se abrio el reporte en el servidor puerto 8000"
    agregar_log(Msg)
    server_thread = threading.Thread(target=open_in_browser)
    server_thread.daemon = True
    server_thread.start()

def stop_server():
    global server_thread
    Msg = "Se detuvo el reporte en el servidor puerto 8000"
    agregar_log(Msg)
    if server_thread is not None:
        server_thread.join(timeout=1)  # Esperar a que el hilo del servidor termine
        server_thread = None