import Pantalla_p_funciones

#importar script con las varibles
import Variables
from Logs import agregar_log, configurar_logs
from Menus_funciones import crear_folders

if __name__ == "__main__":
    try:
        log_doc = "lib/Data/Logs/logs"
        crear_folders("Logs", "lib/Data")
        crear_folders("temp", "lib/Data")
        configurar_logs(log_doc)
        Msg = "Se inicializo la aplicacion"
        agregar_log(Msg)
        Pantalla_p_funciones.HoldingScreen()
        Pantalla_p_funciones.crear_windows_principal(Variables.titulo, Variables.icono_v)
    except Exception as e:
        Msg = f"Error: {e}"
        agregar_log(Msg)
        input(f"Error {e} presiona Enter para salir...") #quitar cuando se cree la app completamente
