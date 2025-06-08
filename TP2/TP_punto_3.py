import numpy as np
import cv2
import matplotlib.pyplot as plt

# --- Parámetro de control ---
delta = 15000.0

# --- Funciones auxiliares ---
def asegurar_grises(imagen):
    if len(imagen.shape) == 3:
        return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    return imagen

def binarizar_imagen(imagen):
    return (imagen > 127).astype(np.uint8)

def ocultar_bit_en_paridad(a, bit, delta):
    signo = 1 if a >= 0 else -1
    q = abs(int(round(a / delta)))
    if q % 2 != bit:
        q += 1
    return signo * q * delta

def recuperar_bit_desde_paridad(a, delta):
    q = abs(int(round(a / delta)))
    return q % 2

# --- Cargar imágenes ---
portadora = asegurar_grises(cv2.imread("memaso.png", cv2.IMREAD_UNCHANGED))
oculta = asegurar_grises(cv2.imread("wp.png", cv2.IMREAD_UNCHANGED))
oculta_bin = binarizar_imagen(oculta)

# --- Transformada de Fourier 2D de la imagen portadora ---
F = np.fft.fft2(portadora.astype(np.float64))
F_real = F.real.copy()
F_imag = F.imag.copy()

# --- Codificación de la imagen oculta en F ---
m, n = oculta_bin.shape
for i in range(m):
    for j in range(n):
        bit = int(oculta_bin[i, j])
        F_real[i, j] = ocultar_bit_en_paridad(F_real[i, j], bit, delta)
        F_imag[i, j] = ocultar_bit_en_paridad(F_imag[i, j], bit, delta)

F_modificada = F_real + 1j * F_imag
imagen_estego = np.real(np.fft.ifft2(F_modificada))
imagen_estego = np.clip(imagen_estego, 0, 255).astype(np.uint8)
cv2.imwrite("imagen_estego2.png", imagen_estego)

# --- Decodificación desde imagen estego ---
F_estego = np.fft.fft2(imagen_estego.astype(np.float64))
F_estego_real = F_estego.real
F_estego_imag = F_estego.imag

recuperada = np.zeros_like(oculta_bin)
for i in range(m):
    for j in range(n):
        bit_r = recuperar_bit_desde_paridad(F_estego_real[i, j], delta)
        bit_i = recuperar_bit_desde_paridad(F_estego_imag[i, j], delta)
        # Promediar (redundancia) para mayor robustez
        bit = 1 if bit_r + bit_i >= 1 else 0
        recuperada[i, j] = bit * 255

# --- Guardar imagen recuperada ---
cv2.imwrite("imagen_recuperada.png", recuperada)

# --- Mostrar todas las imágenes ---
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.title("Imagen Portadora")
plt.imshow(portadora, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title("Imagen Estego")
plt.imshow(imagen_estego, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.title("Imagen Oculta (Original)")
plt.imshow(oculta, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.title("Imagen Oculta (Recuperada)")
plt.imshow(recuperada, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
