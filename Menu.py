import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from PIL import Image, ImageTk
import os

import Animacion as animacion

# Carpeta donde se guardarán los proyectos
PROJECTS_DIR = "proyectos"

# Crear carpeta base si no existe
os.makedirs(PROJECTS_DIR, exist_ok=True)


def iniciar_proyecto_nuevo():
    """Crea un nuevo proyecto con un nombre dado por el usuario."""
    nombre = simpledialog.askstring("Nuevo proyecto", "Introduce el nombre del proyecto:")
    if not nombre:
        return

    ruta = os.path.join(PROJECTS_DIR, nombre)
    if os.path.exists(ruta):
        messagebox.showerror("Error", "Ya existe un proyecto con ese nombre.")
        return

    os.makedirs(ruta)
    
    os.makedirs(os.path.join(ruta, "Capturas"), exist_ok=True)
    os.makedirs(os.path.join(ruta, "Capturas_editadas"), exist_ok=True)
    messagebox.showinfo("Proyecto creado", f"Proyecto '{nombre}' creado en:\n{ruta}")
    abrir_proyecto(ruta)

    
def abrir_proyecto_existente():
    """Permite seleccionar una carpeta de proyecto existente."""
    carpeta = filedialog.askdirectory(initialdir=PROJECTS_DIR, title="Seleccionar proyecto existente")
    if carpeta:
        abrir_proyecto(carpeta)

def abrir_proyecto(ruta):
    """Aquí puedes definir qué pasa cuando se abre un proyecto."""
    ventana.destroy()  # Cerrar la ventana del menú
    animacion.pizarraPrincipal(ruta)  #abrir la pizarra con la ruta del proyecto
    #interfaz_pizarra.interfaz_pizarra()  #abrir la interfaz de pizarra

# === Interfaz principal ===
ventana = tk.Tk()
ventana.title("Pizarra de Animación - Menú Principal")
ventana.geometry("600x296")
ventana.resizable(False, False)

#== Fondo de ventana ==
ruta_fondo = 'MenuImagenes/fondo_menu.jpg'
imagen_fondo = Image.open(ruta_fondo)

fondo = ImageTk.PhotoImage(imagen_fondo)
label_fondo = tk.Label(ventana, image=fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(ventana, text="🎨 Pizarra de Animación", font=("Arial", 18, "bold")).pack(pady=30)

btn_nuevo = tk.Button(ventana, text="➕ Iniciar proyecto nuevo", font=("Arial", 12), width=25, command=iniciar_proyecto_nuevo)
btn_nuevo.pack(pady=10)

btn_abrir = tk.Button(ventana, text="📂 Abrir proyecto existente", font=("Arial", 12), width=25, command=abrir_proyecto_existente)
btn_abrir.pack(pady=10)

ventana.mainloop()
