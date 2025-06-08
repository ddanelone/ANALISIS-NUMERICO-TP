import numpy as np
from PIL import Image

delta = 1.0
bandera = '&'

# 1. Cargar imagen TIFF reconstruida
imagen = Image.open("imagen_portadora_mensaje.tiff").convert("L")
matriz = np.array(imagen, dtype=np.float32)

# 2. Aplicar TF2D para obtener matriz compleja
tf2d = np.fft.fft2(matriz)

# 3. Extraer mensaje oculto con misma función que antes
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

mensaje_recuperado = extraer_mensaje_hasta_bandera(tf2d, delta, bandera)
print("📥 Mensaje recuperado desde imagen TIFF:")
print(mensaje_recuperado)
