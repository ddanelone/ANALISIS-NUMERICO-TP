import numpy as np
import csv
import matplotlib.pyplot as plt

delta = 1.0
bandera = '&'

# 1. Leer CSV y reconstruir matriz compleja
with open("preguntas (1).csv", newline="") as archivo_csv:
    lector = csv.reader(archivo_csv)
    next(lector)  # saltar encabezado

    datos = [(int(f), int(c), float(r), float(im)) for f, c, r, im in lector]

max_fila = max(f for f, _, _, _ in datos)
max_col = max(c for _, c, _, _ in datos)
tf2d = np.zeros((max_fila + 1, max_col + 1), dtype=complex)

for f, c, r, im in datos:
    tf2d[f, c] = complex(r, im)

# 2. Función para extraer mensaje hasta bandera '&'
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
mensaje_recuperado = extraer_mensaje_hasta_bandera(tf2d, delta, bandera)
if mensaje_recuperado.endswith(bandera):
    mensaje_recuperado = mensaje_recuperado[:-1]

print("📥 Mensaje recuperado:")
print(mensaje_recuperado)

# 3. Reconstruir imagen con transformada inversa
imagen_reconstruida = np.fft.ifft2(tf2d).real

# 4. Mostrar la imagen reconstruida
plt.imshow(imagen_reconstruida, cmap='gray')
plt.title("Imagen reconstruida desde TF2D")
plt.axis('off')
plt.show()
