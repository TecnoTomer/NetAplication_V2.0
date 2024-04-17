import threading
import subprocess
import webbrowser
import http.server
import socketserver

ruta = "lib/data/battery_monitor.html"

def generate_battery_report():
    subprocess.run(["powercfg", "/batteryreport", "/output", ruta], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def open_in_browser():
    # Generar el informe de la batería y limpiar el archivo HTML
    generate_battery_report()

    # Definir el manejador de solicitud HTTP
    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory="lib/data", **kwargs)

    # Crear un servidor HTTP en el puerto 8000
    with socketserver.TCPServer(("", 8000), MyHttpRequestHandler) as httpd:
        print("Servidor web iniciado en el puerto 8000...")
        # Abrir el navegador web con la página generada
        webbrowser.open("http://localhost:8000/battery_monitor.html")
        # Escuchar las solicitudes entrantes hasta que se interrumpa
        httpd.serve_forever()

def open_in_browser_thread():
    thread = threading.Thread(target=open_in_browser)
    thread.start()

# Llamar a la función open_in_browser en un hilo separado
open_in_browser_thread()

# El programa principal puede continuar su ejecución aquí sin bloquearse
# ...

