import cv2
import numpy as np

import os
import tkinter as tk
from  tkinter import filedialog 
from tkinter import messagebox

# --- Variables globales ---
colores = [
        ((0,0,255), "Rojo"),
        ((0,222,0), "Verde"),
        ((255,0,0), "Azul"),
        ((0,0,0), "Negro"),
        ((255,255,255), "Blanco"),
        ((255,255,0), "Cian"),
        ((255,0,255), "Magenta"),
        ((0,255,255), "Amarillo"),
        ((128,128,128), "Gris"),
        ((255, 0, 157), "Morado"),
        ((26, 127, 239), "Naranja")
    ] 

color_actual = (0, 0, 0)  # Color inicial por defecto (negro)

incremento_brillo = 0

bloque = 3 
constante = 0 
img_original = None

def setPizarraBlanca ():
    """Crea y devuelve una imagen blanca para usar como pizarra."""
    img = np.zeros((500, 700, 3), np.uint8)   #Crear pizarra blanca 
    img[:] = (255, 255, 255)

    return img

def modificar_brillo (img):
    """Incrementa el brillo de la imagen."""
    global incremento_brillo

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    limite = 255 - incremento_brillo
    v[v > limite] = 255
    v[v <= limite] += incremento_brillo

    hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return img

def incrementar_brillo (valor):
    """Actualiza el valor de la variable incremento_brillo """
    global incremento_brillo
    incremento_brillo = valor

def actualizar_bloque(blq):
    global bloque, img_original, constante
    bloque = blq

    if bloque < 3 : bloque = 3

    elif bloque%2 == 0 : bloque += 1

    img_umbral = cv2.adaptiveThreshold(img_original,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,bloque,constante)

    #ADAPTIVE_THRESH_MEAN_C::
    cv2.imshow('Imagen filtrada', img_umbral)

def actualizar_constante (cte): #Ajusta el umbral calculado
    global constante, img_original, bloque
    constante = cte

    img_umbral = cv2.adaptiveThreshold(img_original,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,bloque,constante)

    cv2.imshow('Imagen filtrada', img_umbral)

def filtro_adaptativo (imagen):
    global constante, img_original, bloque

    img_original = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    cv2.namedWindow('Filtrar Imagen')
    #cv2.namedWindow('Imagen Filtrada')

    cv2.createTrackbar('Bloque', 'Filtrar Imagen', bloque, 500, actualizar_bloque)
    cv2.createTrackbar('Constante', 'Filtrar Imagen', constante, 255, actualizar_constante)

    img_umbral = cv2.adaptiveThreshold(
        img_original, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
        bloque, constante
    )
    cv2.imshow('Filtrar Imagen', img_umbral)

    while True:
        key = cv2.waitKey(100)

        if key == 27 or key == ord('q'):
            cv2.destroyWindow('Filtrar Imagen')
            return None

        elif key == ord('s'):
            cv2.destroyWindow('Filtrar Imagen')
            return img_umbral

def editar_imagen (imagen):
    """Selecciona una imagen guardada y permite editarla. Devuelve la ruta de donde se ha guardado la imagen"""

    if imagen is None:
        print("No se pudo cargar la imagen.")
        return

    cv2.namedWindow('Imagen Seleccionada')
    cv2.createTrackbar('Brillo', 'Imagen Seleccionada', 0, 255, incrementar_brillo)

    #--- Bucle para la edición ---
    while True:
        key = cv2.waitKey(100)
        img_modificada = modificar_brillo(imagen.copy())      

        cv2.imshow('Imagen Seleccionada', img_modificada)

        #Tecla ESC o 'q'
        if key == 27 or key == ord('q'): 
            cv2.destroyWindow('Imagen Seleccionada')
            return img_modificada
        
        #tecla S
        elif key == ord('s'):
            cv2.destroyWindow('Imagen Seleccionada')
            
            #--- Preguntar si desea aplicar filtro adaptativo ---
            raiz = tk.Tk()
            raiz.withdraw() 

            respuesta = messagebox.askyesno("Filtro adaptativo", "¿Desea aplicar filtro adaptativo?")
            raiz.destroy()

            if respuesta:
                img_guardar = filtro_adaptativo(img_modificada)
            else:
                img_guardar = img_modificada

            # --- Elegir ruta y nombre para guardar ---
            raiz = tk.Tk()
            raiz.withdraw()

            Capturas_editadas = os.path.join(os.getcwd(), "Capturas_editadas")
            ruta_guardado = filedialog.asksaveasfilename(
                initialdir=Capturas_editadas,
                title="Guardar imagen editada",
                defaultextension=".jpg",
                filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
            )
            raiz.destroy()

            if ruta_guardado:
                cv2.imwrite(ruta_guardado, img_guardar)
                return ruta_guardado
            else:
                print("⚠️ No se guardó la imagen (cancelado por el usuario).")
                return img_modificada


def dibujar_menu (ruta):
    """
    Dibuja la ventana menú. Muestra a la izquierda las capturas hechas y a la derecha los colores
    """
    menu = np.zeros((600, 600, 3), np.uint8)
    menu[:] = (220, 220, 220)

    global boton 
    boton = (20, 50, 250, 90)
    cv2.putText(menu, "Colores:", (350, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)

    #--- Dibujar los colores disponibles ---
    x, y = 350, 70
    for c, nombre in colores:
        cv2.rectangle(menu, (x, y), (x+20, y+20), c, -1)
        cv2.rectangle(menu, (x, y), (x+20, y+20), (0, 0, 0), 1)
        cv2.putText(menu, nombre, (x+30, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (40, 40, 40), 1)
        y += 50

    # --- Mostrar los nombres de las capturas hechas ---
    cv2.putText(menu, "Capturas:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)

    # --- Dibujar botón para seleccionar captura ---
    cv2.rectangle(menu, (20, 50), (250, 90), (180, 180, 180), -1)   # fondo
    cv2.rectangle(menu, (20, 50), (250, 90), (50, 50, 50), 2)       # borde
    cv2.putText(menu, "Seleccionar captura", (30, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)

    # --- Mostrar la opción de captura ---
    cv2.putText(menu, "C: Tomar  fotografia", (30, 590), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)    
    return menu 

