import json
from flask import Flask, render_template

# Inicializar la aplicación Flask
app = Flask(__name__)

# Ruta para renderizar el template de Flask
@app.route('/')
def index():
    # Cargar los datos desde el archivo JSON
    with open('datos.json', 'r') as file:
        data = json.load(file)
    
    # Obtener los datos de los campos NOMBRE y SEÑAL del JSON
    nombres = data.get("NOMBRE", [])
    bssid = data.get("BSSID", [])
    senal = data.get("SEÑAL", [])
    canal = data.get("CANAL", [])
    frecuencia = data.get("FRECUENCIA (GHz)", [])
    banda = data.get("BANDA", [])
    seguridad = data.get("SEGURIDAD", [])

    # Renderizar el template y pasar los datos
    return render_template('index.html', nombres=nombres, bssid=bssid, senal=senal, canal=canal, frecuencia=frecuencia, banda=banda, seguridad=seguridad)

# Configurar la carpeta para archivos estáticos (por ejemplo, imágenes)
app.static_folder = 'static'
app.static_url_path = '/static'

if __name__ == '__main__':
    app.run(debug=True)
