import tkinter as tk
from PIL import Image, ImageTk

#script con variables
import Variables


#Perzonalizacion selecionar boton
def selecion_boton(self): #efecto al selecionar boton
    self.bind("<Enter>", lambda event: self.config(bg=Variables.c_s_b))
    self.bind("<Leave>", lambda event: self.config(bg=Variables.c_barras))

#Botones informativos
def boton_ayuda(color, selft, texto_tooltip, coord_x, coord_y):#boton ayuda informativo derecha
    imagen = Image.open(Variables.icono_help) # reemplaza esto con la ruta a tu imagen
    imagen = imagen.resize((15, 15), Image.LANCZOS) # Ajustar el tamaño de la imagen
    imagen_tk = ImageTk.PhotoImage(imagen) # Convertir la imagen a un formato que Tkinter pueda usar
    boton_help = tk.Label(selft, image=imagen_tk, bg=color) # Crear el botón con la imagen ajustada
    boton_help.image = imagen_tk # mantener una referencia a la imagen
    boton_help.place(x=coord_x, y=coord_y) # ajusta las coordenadas x e y
    ToolTip(boton_help, texto_tooltip) # Crear el tooltip para el botón

class ToolTip(object): #tooltip del boton_ayuda informativo derecha
    def __init__(self, widget, text='Widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tw, text=self.text, background="#ffffff", relief='solid', borderwidth=1, wraplength = 180)
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()

def boton_ayuda_izquierda(color, selft, texto_tooltip, coord_x, coord_y): #boton ayuda informativo izquierda
    imagen = Image.open(Variables.icono_help) # reemplaza esto con la ruta a tu imagen
    imagen = imagen.resize((15, 15), Image.LANCZOS) # Ajustar el tamaño de la imagen
    imagen_tk = ImageTk.PhotoImage(imagen) # Convertir la imagen a un formato que Tkinter pueda usar
    boton_help = tk.Label(selft, image=imagen_tk, bg=color) # Crear el botón con la imagen ajustada
    boton_help.image = imagen_tk # mantener una referencia a la imagen
    boton_help.place(x=coord_x, y=coord_y) # ajusta las coordenadas x e y
    ToolTipIzquierda(boton_help, texto_tooltip) # Crear el tooltip para el botón

class ToolTipIzquierda(object):
    def __init__(self, widget, text='Widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        # Colocar la ventana del tooltip a la izquierda del botón
        self.tw.wm_geometry(f"+{x - 200}+{y}") #ajustar '200' según el tamaño de tu tooltip
        label = tk.Label(self.tw, text=self.text, background="#ffffff", relief='solid', borderwidth=1, wraplength = 180)
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()
