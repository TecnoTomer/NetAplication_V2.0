import tkinter as tk
from  tkinter import ttk
import pandas as pd
import time

import Variables
from Logs import agregar_log

def Centro_principal(frame):
	Msg = "Centro principal cargado correctamente"
	agregar_log(Msg)
	global Centro_p
	Centro_p = tk.Frame(frame, bg="blue")
	Centro_p.pack(side="top", fill="both", expand=True)

	
	return frame