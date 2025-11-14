import tkinter as tk
from tkinter import colorchooser, ttk
from PIL import Image, ImageTk
import os


# --- Variables globales ---
color = (0, 0, 0)
grosor = 3


# --- Funciones de utilidad ---
def actualizar_grosor(val):
    """Actualiza el grosor (solo visual)."""
    global grosor
    grosor = int(val)
    lbl_grosor.config(text=f"Grosor: {grosor}")


def seleccionar_color():
    """Selecciona un color (solo visual)."""
    global color
    nuevo_color = colorchooser.askcolor(title="Selecciona un color")[0]  # (R,G,B)
    if nuevo_color:
        color = tuple(map(int, nuevo_color))
        btn_color.config(bg=f"#{int(color[0]):02x}{int(color[1]):02x}{int(color[2]):02x}")


def abrir_camara():
    """Solo muestra mensaje de cámara (no funcional)."""
    print("📸 Cámara (función no implementada aún).")


def abrir_pizarra():
    """Simula abrir la pizarra (solo mensaje)."""
    print("🖌️ Simulando apertura de la pizarra OpenCV...")


# --- Interfaz principal ---
def interfaz_pizarra():
    ventana = tk.Tk()
    ventana.title("Pizarra de Animación (Control)")
    ventana.geometry("1000x600")
    ventana.configure(bg="#ececec")

    global lbl_grosor, btn_color

    # === Marco superior (controles) ===
    frame_top = tk.Frame(ventana, bg="#dddddd", height=60)
    frame_top.pack(fill="x")

    lbl_grosor = tk.Label(frame_top, text=f"Grosor: {grosor}", bg="#dddddd", font=("Arial", 11))
    lbl_grosor.pack(side="left", padx=10)

    slider_grosor = ttk.Scale(frame_top, from_=1, to=20, orient="horizontal", command=actualizar_grosor)
    slider_grosor.set(grosor)
    slider_grosor.pack(side="left", padx=10)

    btn_color = tk.Button(frame_top, text="🎨 Color", command=seleccionar_color, width=10)
    btn_color.pack(side="left", padx=10)

    try:
        icono_camara = Image.open("MenuImagenes/camara_icono.png")
        icono_camara = icono_camara.resize((35, 35))
        icono_camara_tk = ImageTk.PhotoImage(icono_camara)
        btn_camara = tk.Button(frame_top, image=icono_camara_tk, command=abrir_camara, bd=0, bg="#dddddd", cursor="hand2")
        btn_camara.image = icono_camara_tk  # prevenir que se borre de memoria
    except Exception as e:
        print("⚠️ No se encontró el ícono de cámara:", e)
        btn_camara = tk.Button(frame_top, text="📸 Cámara", command=abrir_camara, bg="#dddddd", cursor="hand2")

    btn_camara.pack(side="right", padx=15)

    # === Marco izquierdo (miniaturas de capturas) ===
    frame_izq = tk.Frame(ventana, bg="#f0f0f0", width=150)
    frame_izq.pack(side="left", fill="y")

    tk.Label(frame_izq, text="📁 Capturas", bg="#f0f0f0", font=("Arial", 11, "bold")).pack(pady=10)

    for i in range(3):
        lbl = tk.Label(frame_izq, text=f"Imagen {i+1}", bg="#fafafa", relief="groove", width=15, height=2)
        lbl.pack(pady=5, padx=10)

    # === Marco central ===
    frame_centro = tk.Frame(ventana, bg="#cccccc")
    frame_centro.pack(side="left", expand=True, fill="both")

    lbl_info = tk.Label(frame_centro, text="Interfaz de control de pizarra", bg="#cccccc", font=("Arial", 12))
    lbl_info.pack(pady=20)

    btn_abrir = tk.Button(frame_centro, text="🖌️ Abrir Pizarra (demo)", font=("Arial", 13, "bold"), command=abrir_pizarra)
    btn_abrir.pack(pady=10)

    ventana.mainloop()

