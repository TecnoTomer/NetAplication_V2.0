import ctypes 

def alerta_ok(titulo_ventana, titulo, texto): #esta alerta me muestra un boton de aceptar
	hwnd = ctypes.windll.user32.FindWindowW(None, titulo_ventana)
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 64)
	return resultado

def alerta_error(titulo_ventana, titulo, texto): #esta alerta me muestra 3 botones "anular, reintentar, omitir"
	hwnd = ctypes.windll.user32.FindWindowW(None, titulo_ventana)
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 18)
	return resultado

def alerta_aceptar(titulo_ventana, titulo, texto): #esta alerta muestra dos botones "aceptar, cancelar"
	hwnd = ctypes.windll.user32.FindWindowW(None, titulo_ventana)
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 33)
	return resultado

def alerta_cerrar(titulo_ventana, titulo, texto): #esta alerta muestra el icono amarillo con boton aceptar, cancelar
	hwnd = ctypes.windll.user32.FindWindowW(None, titulo_ventana)
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 52)
	return resultado

def alerta_Amarilla(titulo_ventana, titulo, texto): #esta alerta muestra el icono amarillo y un boton de aceptar
	hwnd = ctypes.windll.user32.FindWindowW(None, titulo_ventana)
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 48)
	return resultado
	
def alerta_si_no(titulo_ventana, titulo, texto):
	hwnd = ctypes.windll.user32.FindWindowW(None, titulo_ventana)
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 36)
	return resultado
