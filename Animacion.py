import numpy as np
import cv2
import funciones as fn

import os
import tkinter as tk
from  tkinter import filedialog 

color = (0, 0, 0)
grosor = 2

# Controlar capturas
n_capturas = 0
grabando = False

imagen_referencia = None
transparencia = 0.4  
referencia_activa = False

camara = cv2.VideoCapture(0) #1 = webcam, 0 = droidcam
numero_fotograma = 0

def actualizar_grosor(val):
    global grosor
    if val < 1:
        val = 1
    grosor = val

def pinta(event,x,y,flags,param):

    global x_prev,y_prev, color

    if event == cv2.EVENT_LBUTTONDOWN:
        x_prev,y_prev = x,y

    if event == cv2.EVENT_RBUTTONDOWN:
        x_prev,y_prev = x,y

    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        cv2.line(img,(x_prev,y_prev),(x,y),fn.color_actual, grosor)
        x_prev,y_prev = x,y

    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_RBUTTON:
       cv2.line(img,(x_prev,y_prev),(x,y),(255,255,255),grosor)
       x_prev,y_prev = x,y

    if referencia_activa:
        mostrar_pizarra_calco(img)
    else:
        cv2.imshow('Pizarra', img)

def mostrar_pizarra_calco(pizarra):
    """
    Muestra la pizarra con la imagen de referencia.
    """
    global imagen_referencia, transparencia, referencia_activa

    if not referencia_activa or imagen_referencia is None:
        cv2.imshow("Pizarra", pizarra)
        return

    ref_redim = cv2.resize(imagen_referencia, (pizarra.shape[1], pizarra.shape[0])) # Ajuste con la pizarra

    calco = cv2.addWeighted(ref_redim, transparencia, pizarra, 1 - transparencia, 0)

    cv2.imshow("Pizarra", calco)

def pegar_imagen (ruta, temporal):
    """Carga una imagen para pegarla a la pizarra"""

    global imagen_referencia, referencia_activa

    imag_calcar = cv2.imread(ruta)
    if imag_calcar is None:
        print("⚠️ No se pudo cargar la imagen de referencia.")
        return None
   
    # --- Borrar si es una imagen temporal ---
    if temporal:  # o cualquier otra regla que uses
        try:
            os.remove(ruta)
        except Exception as e:
            print(f"⚠️ No se pudo eliminar {ruta}: {e}")


    imagen_referencia = imag_calcar
    referencia_activa = True
    return imag_calcar

def seleccionar_captura (ruta_proyecto):
    raiz = tk.Tk()
    raiz.withdraw()

    ruta_imagen = filedialog.askopenfilename(
        file = "Seleccione una imagen",
        initialdir=ruta_proyecto,
        filetypes = [("Archivos de imagen", "*.jpg *.jpeg *.png")]
    )

    if ruta_imagen:
        img = cv2.imread(ruta_imagen)

        resultado = fn.editar_imagen(img)

        if isinstance(resultado, str):
            temp = False
            pegar_imagen (resultado, temp)
        elif resultado is not None:
            temp_path = "temp_editada.jpg"
            cv2.imwrite(temp_path, resultado)
            temp = True
            pegar_imagen(temp_path, temp)
        else:
            print("Error al seleccionar la imagen")
    else:
        print("No se ha seleccionado la imagen")

    raiz.destroy()
        
def guardar_captura (ruta):
    global numero_fotograma

    cv2.namedWindow('camara')

    if not camara.isOpened():
        print("No es posible abrir la cámara")
        exit()

    while True:
        key = cv2.waitKey(100)

        ret, frame = camara.read()
        if not ret:
            print("No es posible obtener la imagen")
            break

        cv2.imshow('camara', frame)

        if key == ord(' '):
            print('Grabando '+'/fotograma'+str(numero_fotograma)+'.jpg')
            cv2.imwrite(ruta+'/Capturas'+'/fotograma'+str(numero_fotograma)+'.jpg', frame)
            numero_fotograma +=1
            print("Ruta actual:", os.getcwd())
            break 
        elif key == ord('q'):
            break

    camara.release()
    cv2.destroyWindow('camara')

def click_menu (event, x, y, flags, param):
    global color_actual
        
    if event == cv2.EVENT_LBUTTONDOWN:
       #--- Para seleccionar captura ---
        if hasattr(fn, 'boton'):
            x1, y1, x2, y2 = fn.boton
            if (x1 <= x <= x2 and y1 <= y <= y2):
                seleccionar_captura(ruta)
                return 
        #--- Para seleccionar colores ---
        x_inicial = 350
        y_inicial = 70
        for c, nombre in fn.colores:
            if x_inicial <= x <= x_inicial + 40 and y_inicial <= y <= y_inicial + 40:
                fn.color_actual = c
                print(f"🎨 Color cambiado a: {nombre} ({c})")
                break
            y_inicial += 50  

def pizarraPrincipal(ruta_proyecto):
    """
    Abre la pizarra principal de animación. 
    Permite dibujar, guardar imágenes y crear una animación GIF.
    """
    # --- Variables globales ---
    global img, imagenes, indice_actual, pizarra_blanca, menu
    global referencia_activa
    global ruta
    
    ruta = ruta_proyecto

    print("Abriendo pizarra de animación para el proyecto en:", ruta_proyecto)    #Mensaje de prueba
    imagenes = []               #Almacena las imagenes guardadas de la pizarra
    indice_actual = -1
    pizarra_blanca = True
        
    img = fn.setPizarraBlanca()        #Crear una pizarra blanca
    menu = fn.dibujar_menu(ruta_proyecto)

    #--- Inicializar elementos necesarios ---
    cv2.namedWindow('Pizarra')
    cv2.setMouseCallback('Pizarra', pinta)
    cv2.createTrackbar('Grosor', 'Pizarra', grosor, 20, actualizar_grosor)
    cv2.imshow('Pizarra',img)

    cv2.namedWindow("Menu")
    cv2.setMouseCallback("Menu", click_menu)
    cv2.imshow('Menu', menu)

    #--- Imprimir los controles básicos --
    print("Controles:")
    print(" - M: Mostrar/Ocultar menú")
    print(" - C: Abrir cámara")
    print(" - Enter: Guardar dibujo actual")
    print(" - Q: Salir")
    print(" - D: Siguiente imagen")
    print(" - A: Imagen anterior")
    print(" - N: Nueva pizarra en blanco")
    print(" - Supr: Borrar imagen actual")

    #--- Bucle principal ---
    while True:
        key = cv2.waitKey(100)

        #Tecla ENTER
        if key == 13:
            if pizarra_blanca:
                imagenes.append(img.copy())
                print("Imagen guardada. Total de imagenes:", len(imagenes))
                indice_actual = len(imagenes)

                #Poner la pizarra en blanco
                img = fn.setPizarraBlanca()
                if referencia_activa:
                    mostrar_pizarra_calco(img)
                else:
                    cv2.imshow('Pizarra', img)

                pizarra_blanca = True
            else:
                imagenes[indice_actual] = img.copy()
                print("Imagen ", indice_actual, " editada")

        #Tecla derecha o 'd' (pasar a la siguiente imagen)
        elif key == ord('d'):
            indice_actual += 1
            if indice_actual == len(imagenes):
                #Poner la pizarra en blanco
                pizarra_blanca = True
                img = fn.setPizarraBlanca()
                if referencia_activa:
                    mostrar_pizarra_calco(img)
                else:
                    cv2.imshow('Pizarra', img)

            elif indice_actual > len(imagenes) - 1:
                print("No hay mas imagenes")
                indice_actual = len(imagenes) - 1

            else:
                pizarra_blanca = False
                print("Mostrando la siguiente imagen, numero:", indice_actual)
                img = imagenes[indice_actual].copy()
                if referencia_activa:
                    mostrar_pizarra_calco(img)
                else:
                    cv2.imshow('Pizarra', img)

        #Tecla izquierda o 'a' (volver a la imagen anterior)
        elif key == ord('a'):
            # Pizarra blanca justo después de guardar
            if pizarra_blanca and indice_actual == len(imagenes):
                if len(imagenes) > 0:
                    indice_actual = len(imagenes) - 1
                    pizarra_blanca = False
                    print("Volviendo a la última imagen:", indice_actual)
                    img = imagenes[indice_actual].copy()
                    if referencia_activa:
                        mostrar_pizarra_calco(img)
                    else:
                        cv2.imshow('Pizarra', img)
                else:
                    print("No hay imágenes guardadas aún")
            else:
                indice_actual -= 1
                if indice_actual < 0:
                    print("No hay imagen anterior")
                    indice_actual = 0
                else:
                    pizarra_blanca = False
                    print("Mostrando la imagen anterior, número:", indice_actual)
                    img = imagenes[indice_actual].copy()
                    if referencia_activa:
                        mostrar_pizarra_calco(img)
                    else:
                        cv2.imshow('Pizarra', img)
            
        #Tecla Borrar (Borrar una imagen)
        elif key == 8:
            print("Borrando imagen...")
            if len(imagenes) > 0 and not pizarra_blanca:
                imagenes.pop(indice_actual)
                print("Imagen borrada. Total de imagenes:", len(imagenes))
                if len(imagenes) == 0:
                    #Poner la pizarra en blanco
                    pizarra_blanca = True
                    img = fn.setPizarraBlanca()
                    if referencia_activa:
                        mostrar_pizarra_calco(img)
                    else:
                        cv2.imshow('Pizarra', img)
                    indice_actual = -1
                else:
                    if indice_actual >= len(imagenes):
                        indice_actual = len(imagenes) - 1
                    img = imagenes[indice_actual].copy()
                    if referencia_activa:
                        mostrar_pizarra_calco(img)
                    else:
                        cv2.imshow('Pizarra', img)
            else:
                print("No hay imagen para borrar o estas en una pizarra en blanco")

        #Tecla 'n' (Poner en blanco la pizarra)
        elif key == ord('n'):
            print("Poniendo la pizarra en blanco...")
            pizarra_blanca = True
            img = fn.setPizarraBlanca()
            if referencia_activa:
                mostrar_pizarra_calco(img)
            else:
                cv2.imshow('Pizarra', img)
            
        #Tecla ESC ó 'q'
        elif key == 27 or key == ord('q'): 
            
            ruta_video = os.path.join(ruta_proyecto, "output.mp4")
            if len(imagenes) == 0:
                print("⚠️ No hay imágenes para exportar.")
                break

            alto, ancho, _ = imagenes[0].shape
            fps = 5 

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(ruta_video, fourcc, fps, (ancho, alto))

            # --- Escribir los frames ---
            for i, frame in enumerate(imagenes):
                out.write(frame)
                print(f"🎞️ Frame {i} agregado al video")

            out.release()
            print(f"✅ Video guardado correctamente en: {ruta_video}")
            break

        #Tecla 'x' (Alternar referencia)
        elif key == ord('x'):
            if referencia_activa:
                referencia_activa = False
            else:
                referencia_activa = True

        #Tecla 'c' (Tomar captura)
        elif key == ord('c'):
            guardar_captura(ruta_proyecto)

    cv2.destroyAllWindows()