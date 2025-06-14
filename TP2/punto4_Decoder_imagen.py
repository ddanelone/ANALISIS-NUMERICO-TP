import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

delta = 1.0
bandera = '&'

# 1. Cargar imagen TIFF
imagen_estego = Image.open("imagen_estego.tiff").convert("L")
matriz_estego = np.array(imagen_estego, dtype=np.float32)

# Mostrar imagen estego (espacial)
print("\n🔹 Imagen estego (primeros 5x4 píxeles):")
print(matriz_estego[:5, :4])

# 2. Aplicar transformada de Fourier a la imagen estego
tf2d_recuperada = np.fft.fft2(matriz_estego)

# Mostrar matriz transformada recuperada
print("\n🔹 TF2D recuperada (primeros 5x4 elementos - parte real):")
print(tf2d_recuperada[:5, :4].real)
print("\n🔹 TF2D recuperada (primeros 5x4 elementos - parte imaginaria):")
print(tf2d_recuperada[:5, :4].imag)

# 3. Función para extraer mensaje (sin cambios)
def extraer_mensaje_hasta_bandera(tf2d, delta, bandera='&'):
    bits = ""
    mensaje = ""
    filas, columnas = tf2d.shape
    k = 0

    for i in range(filas):
        for j in range(columnas):
            if k % 8 == 0 and k != 0:
                caracter = chr(int(bits[-8:], 2))
                mensaje += caracter
                if caracter == bandera:
                    return mensaje

            a, b = tf2d[i, j].real, tf2d[i, j].imag

            q_real = abs(round(a / delta))
            bits += str(q_real % 2)
            k += 1

            if k % 8 == 0:
                caracter = chr(int(bits[-8:], 2))
                mensaje += caracter
                if caracter == bandera:
                    return mensaje

            q_imag = abs(round(b / delta))
            bits += str(q_imag % 2)
            k += 1

    return mensaje

# Extraer mensaje
mensaje_recuperado = extraer_mensaje_hasta_bandera(tf2d_recuperada, delta, bandera)
if mensaje_recuperado.endswith(bandera):
    mensaje_recuperado = mensaje_recuperado[:-1]

print("\n📥 Mensaje recuperado:")
print(mensaje_recuperado)

# 4. Mostrar la imagen estego
plt.figure(figsize=(12, 6))
plt.imshow(matriz_estego, cmap='gray')
plt.title("Imagen estego (TIFF)")
plt.axis('off')

plt.tight_layout()
plt.show()