import numpy as np
from PIL import Image
import csv

delta = 1.0

# 1. Cargar imagen
imagen = Image.open("memaso.png").convert("L")
matriz = np.array(imagen, dtype=np.float32)

# 2. Transformada de Fourier
tf2d = np.fft.fft2(matriz)

# 3. Codificar mensaje
mensaje = "(1) En LSB, además de codificar más de 1 bit por pixel, podrían hallar otra manera de aumentar la capacidad de codificación en una imagen? (2) Por qué eligieron el método del umbral en 127 y cómo funciona? (3) Qué pasó con la imagen estego cuando usaron deltas muy altos (del orden de 100.000 o más) y qué efecto tuvieron en la imagen recuperada? *** FIN ***&"
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
