import numpy as np
from PIL import Image

delta = 1.0

# 1. Cargar imagen
imagen = Image.open("memaso.png").convert("L")
matriz = np.array(imagen, dtype=np.float32)
print("🔹 Matriz original (primeros 5x4 elementos):")
print(matriz[:5, :4])  # Mostrar subconjunto representativo

# 2. Transformada de Fourier
tf2d = np.fft.fft2(matriz)
print("\n🔹 TF2D original (primeros 5x4 elementos - parte real):")
print(tf2d[:5, :4].real)

# 3. Codificar mensaje
mensaje = "(1) En LSB, además de codificar más de 1 bit por pixel, podrían hallar otra manera de aumentar la capacidad de codificación en una imagen? (2) Por qué eligieron el método del umbral en 127 y cómo funciona? (3) Qué pasó con la imagen estego cuando usaron deltas muy altos (del orden de 100.000 o más) y qué efecto tuvieron en la imagen recuperada? *** FIN ***&"
mensaje_ascii = mensaje.encode("latin1")
mensaje_binario = ''.join(format(byte, '08b') for byte in mensaje_ascii)

# 4. Ocultar mensaje (función sin cambios)
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

# Mostrar matriz transformada modificada
print("\n🔹 TF2D codificada (primeros 5x4 elementos - parte real):")
print(tf2d_codificada[:5, :4].real)
print("\n🔹 TF2D codificada (primeros 5x4 elementos - parte imaginaria):")
print(tf2d_codificada[:5, :4].imag)

# 5. Aplicar transformada inversa y guardar como TIFF
imagen_estego = np.fft.ifft2(tf2d_codificada).real
imagen_estego = np.clip(imagen_estego, 0, 255)
imagen_estego = Image.fromarray(np.fft.ifft2(tf2d_codificada).real.astype(np.float32))
imagen_estego.save("imagen_estego.tiff", format="TIFF")

print("\n✅ Codificación finalizada. Guardado como imagen_estego.tiff")