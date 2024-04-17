import sys
from cx_Freeze import setup, Executable

base = None

build_exe_options = {
    "packages": ["tkinter"],
    "includes": [
        "tkinter", "ctypes", "datetime", "os", "getpass",
        "time", "random", "socket", "psutil", "speedtest",
        "keyboard", "subprocess", "re", "PIL", "pandas", "pyperclip", "pywifi", "openpyxl",
        "shutil", "openpyxl.styles", "base64", "json", "paramiko", "telnetlib3", "telnetlib", "sys",
        "cryptography", "matplotlib", "numpy", "webbrowser", "socketserver", "http", "threading"
    ],
    "include_files": [
        ("lib/data", "lib/data"),
        ("lib/Emulator", "lib/Emulator"),
        ("lib/Screen_Holdin.exe", "lib/Screen_Holdin.exe")
    ]
}

executables = [
    Executable("NetAplicationV2.py", base=None, icon="lib/data/icono.ico")
]

setup(
    name="NetAplication_v2",
    version="2.0",
    description="Bienvenido a tu herramienta todo en uno para ingeniería de sistemas y redes. Diseñada pensando en los profesionales de las telecomunicaciones, esta herramienta proporciona un conjunto integral de funciones para facilitar la gestión eficiente de tus sistemas y redes.",
    options={"build_exe": build_exe_options},
    executables=executables
)


"""
PARA EJECUTAR Y CREAR EL .EXE DEL PROGRAMA EDITAR EL NOMBRE DEL .PY,
Y CORRER EN CMD ESTE COMANDO, cxfreeze script_aparte.py --target-dir dist --no-console

"""
