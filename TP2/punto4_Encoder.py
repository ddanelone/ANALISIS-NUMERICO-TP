import numpy as np
from PIL import Image
import csv

delta = 1.0

# 1. Cargar imagen
imagen = Image.open("imagen_portadora.png").convert("L")
matriz = np.array(imagen, dtype=np.float32)

# 2. Transformada de Fourier
tf2d = np.fft.fft2(matriz)

# 3. Codificar mensaje
mensaje = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.&"
mensaje_ascii = mensaje.encode("latin1")
mensaje_binario = ''.join(format(byte, '08b') for byte in mensaje_ascii)

# 4. Ocultar mensaje
def ocultar_mensaje_en_tf2d(tf2d, bits, delta):
    tf2d_mod = tf2d.copy()
    k = 0
    filas, columnas = tf2d.shape

    for i in range(filas):
        for j in range(columnas):
            if k >= len(bits):
                break

            a, b = tf2d_mod[i, j].real, tf2d_mod[i, j].imag

            if k < len(bits):
                q = abs(round(a / delta))
                bit = int(bits[k])
                if q % 2 != bit:
                    q += 1
                signo = 1 if a >= 0 else -1
                a_cod = signo * q * delta
                k += 1
            else:
                a_cod = a

            if k < len(bits):
                q = abs(round(b / delta))
                bit = int(bits[k])
                if q % 2 != bit:
                    q += 1
                signo = 1 if b >= 0 else -1
                b_cod = signo * q * delta
                k += 1
            else:
                b_cod = b

            tf2d_mod[i, j] = complex(a_cod, b_cod)

        if k >= len(bits):
            break

    return tf2d_mod

tf2d_codificada = ocultar_mensaje_en_tf2d(tf2d, mensaje_binario, delta)

# 5. Guardar en CSV
with open("tf2d_codificada.csv", "w", newline="") as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerow(["fila", "columna", "real", "imag"])

    for i in range(tf2d_codificada.shape[0]):
        for j in range(tf2d_codificada.shape[1]):
            valor = tf2d_codificada[i, j]
            escritor.writerow([i, j, valor.real, valor.imag])

print("✅ Codificación finalizada. Guardado como tf2d_codificada.csv")
