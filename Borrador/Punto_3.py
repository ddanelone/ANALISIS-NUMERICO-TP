import numpy as np
import cv2
import matplotlib.pyplot as plt

def leer_imagen_gris(ruta):
    return cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

def calcular_max_shape_oculta(shape):
    total_bits = shape[0] * shape[1]
    total_pixeles = total_bits // 8
    lado = int(np.floor(np.sqrt(total_pixeles)))
    return (lado, lado)

def ajustar_imagen_oculta(oculta, max_shape):
    if oculta.shape[0] > max_shape[0] or oculta.shape[1] > max_shape[1]:
        print("⚠️ Imagen oculta muy grande. Redimensionando.")
        oculta_redim = cv2.resize(oculta, (max_shape[1], max_shape[0]))
    else:
        oculta_redim = oculta
    return oculta_redim

def ocultar_por_cuantizacion_paridad(portadora, oculta, delta):
    h, w = portadora.shape
    tf = np.fft.fft2(portadora)
    tf_shifted = np.fft.fftshift(tf)

    real = np.real(tf_shifted).flatten()
    imag = np.imag(tf_shifted).flatten()

    capacidad_bits = len(real)
    max_shape_oculta = calcular_max_shape_oculta((h, w))
    oculta_redim = ajustar_imagen_oculta(oculta, max_shape_oculta)
    bits = np.unpackbits(oculta_redim.flatten())
    bits = bits[:capacidad_bits]

    real_mod = np.copy(real)
    imag_mod = np.copy(imag)

    for i in range(len(bits)):
        for componente, modificado in [(real, real_mod), (imag, imag_mod)]:
            a = componente[i]
            signo = 1 if a >= 0 else -1
            q = int(np.round(abs(a) / delta))
            bit = bits[i]

            # Forzar paridad
            if (q % 2) != bit:
                q += 1

            modificado[i] = signo * q * delta

    tf_mod_flat = real_mod + 1j * imag_mod
    tf_mod_shifted = tf_mod_flat.reshape(h, w)
    tf_mod = np.fft.ifftshift(tf_mod_shifted)
    imagen_modificada = np.fft.ifft2(tf_mod)
    imagen_modificada = np.abs(imagen_modificada)
    imagen_modificada = np.clip(imagen_modificada, 0, 255).astype(np.uint8)

    return imagen_modificada, tf, tf_mod, bits, oculta_redim.shape

def extraer_desde_paridad(tf_mod, total_bits, shape_oculta, delta):
    tf_shifted = np.fft.fftshift(tf_mod)
    real = np.real(tf_shifted).flatten()
    imag = np.imag(tf_shifted).flatten()

    bits = []
    for i in range(total_bits):
        a = real[i]
        b = imag[i]

        qa = int(np.round(abs(a) / delta))
        qb = int(np.round(abs(b) / delta))

        # Bit escondido en paridad
        bit_a = qa % 2
        bit_b = qb % 2

        bits.append(bit_a if i % 2 == 0 else bit_b)

    bits = np.array(bits[: (len(bits) // 8) * 8])
    pixeles = np.packbits(bits)
    total_pixeles = shape_oculta[0] * shape_oculta[1]
    return pixeles[:total_pixeles].reshape(shape_oculta)

# === MAIN ===

# Parámetro delta
delta = 200000.0  

# Cargar imágenes
portadora = leer_imagen_gris("imagen_portadora.png")
oculta = leer_imagen_gris("wp.png")

# Ocultamiento
imagen_estego, tf_original, tf_modificada, bits_ocultos, shape_oculta = ocultar_por_cuantizacion_paridad(portadora, oculta, delta)

# Guardar imagen estego
cv2.imwrite("imagen_estego_P3.png", imagen_estego)

# Extracción
recuperada = extraer_desde_paridad(tf_modificada, len(bits_ocultos), shape_oculta, delta)

# Mostrar resultados
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.title("Imagen Portadora")
plt.imshow(portadora, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title("Imagen Estego (δ = {})".format(delta))
plt.imshow(imagen_estego, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.title("Imagen Oculta Redimensionada")
plt.imshow(cv2.resize(oculta, shape_oculta[::-1]), cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.title("Imagen Oculta Recuperada")
plt.imshow(recuperada, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
