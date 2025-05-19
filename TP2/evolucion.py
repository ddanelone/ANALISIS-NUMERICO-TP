import numpy as np
import cv2
import matplotlib.pyplot as plt

def leer_imagen_gris(ruta):
    return cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

def ocultar_imagen(portadora, oculta, escala=0.1):
    # Asegurar tamaños iguales
    oculta = cv2.resize(oculta, (portadora.shape[1], portadora.shape[0]))

    # TF2D de ambas imágenes
    f_portadora = np.fft.fft2(portadora)
    f_oculta = np.fft.fft2(oculta)

    # Insertar parte de la imagen oculta en la portadora (frecuencias altas)
    f_portadora_mod = f_portadora + escala * f_oculta

    # Volver al dominio espacial
    portadora_con_oculta = np.fft.ifft2(f_portadora_mod)
    portadora_con_oculta = np.abs(portadora_con_oculta)
    portadora_con_oculta = np.clip(portadora_con_oculta, 0, 255).astype(np.uint8)

    return portadora_con_oculta, f_portadora_mod

def extraer_imagen(f_portadora_mod, f_portadora, escala=0.1):
    # Diferencia de frecuencias
    f_oculta_extraida = (f_portadora_mod - f_portadora) / escala

    # Volver al dominio espacial
    imagen_extraida = np.fft.ifft2(f_oculta_extraida)
    imagen_extraida = np.abs(imagen_extraida)
    imagen_extraida = np.clip(imagen_extraida, 0, 255).astype(np.uint8)

    return imagen_extraida

# Cargar imágenes
portadora = leer_imagen_gris('imagen_portadora.png')
oculta = leer_imagen_gris('imagen_oculta.png')

# Ocultar imagen
portadora_oculta, f_modificada = ocultar_imagen(portadora, oculta)

# Extraer imagen
f_original = np.fft.fft2(portadora)
oculta_extraida = extraer_imagen(f_modificada, f_original)

# Mostrar resultados
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.title("Imagen Portadora Original")
plt.imshow(portadora, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title("Imagen con Imagen Oculta")
plt.imshow(portadora_oculta, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.title("Imagen Oculta Original")
plt.imshow(oculta, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.title("Imagen Extraída")
plt.imshow(oculta_extraida, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
