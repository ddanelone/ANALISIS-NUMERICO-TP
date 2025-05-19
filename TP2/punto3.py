import numpy as np
import cv2
import matplotlib.pyplot as plt

def leer_imagen_gris(ruta):
    img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"❌ No se pudo leer la imagen: {ruta}")
    return img.astype(np.float64)

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

    max_shape_oculta = calcular_max_shape_oculta((h, w))
    oculta_redim = ajustar_imagen_oculta(oculta, max_shape_oculta)

    bits = np.unpackbits(oculta_redim.astype(np.uint8).flatten())
    
    capacidad_bits = min(len(bits), len(real) + len(imag))  # uso total bits posibles
    bits = bits[:capacidad_bits]

    real_mod = real.copy()
    imag_mod = imag.copy()

    # Vamos a recorrer bits y asignar alternadamente a real_mod e imag_mod:
    idx_real = 0
    idx_imag = 0

    for i, bit in enumerate(bits):
        if i % 2 == 0:
            # Modifico real
            a = real_mod[idx_real]
            signo = 1 if a >= 0 else -1
            q = int(np.round(abs(a) / delta))
            # Ajustar paridad de q según bit
            if (q % 2) != bit:
                q += 1
            real_mod[idx_real] = signo * q * delta
            idx_real += 1
        else:
            # Modifico imag
            b = imag_mod[idx_imag]
            signo = 1 if b >= 0 else -1
            q = int(np.round(abs(b) / delta))
            if (q % 2) != bit:
                q += 1
            imag_mod[idx_imag] = signo * q * delta
            idx_imag += 1

    # Reconstruir TF modificada
    tf_mod_flat = real_mod + 1j * imag_mod
    tf_mod_shifted = tf_mod_flat.reshape(h, w)
    tf_mod = np.fft.ifftshift(tf_mod_shifted)
    imagen_modificada = np.fft.ifft2(tf_mod)
    imagen_modificada = np.abs(imagen_modificada)
    imagen_modificada = np.clip(imagen_modificada, 0, 255).astype(np.uint8)

    return imagen_modificada, bits, oculta_redim.shape

def extraer_desde_paridad(tf_mod, total_bits, shape_oculta, delta):
    tf_shifted = np.fft.fftshift(tf_mod)
    real = np.real(tf_shifted).flatten()
    imag = np.imag(tf_shifted).flatten()

    bits = []
    idx_real = 0
    idx_imag = 0
    for i in range(total_bits):
        if i % 2 == 0:
            a = real[idx_real]
            idx_real += 1
        else:
            a = imag[idx_imag]
            idx_imag += 1
        q = int(np.round(abs(a) / delta))
        bit = q % 2
        bits.append(bit)

    bits = np.array(bits[: (len(bits) // 8) * 8])
    pixeles = np.packbits(bits)
    total_pixeles = shape_oculta[0] * shape_oculta[1]
    return pixeles[:total_pixeles].reshape(shape_oculta)

# === MAIN ===

delta = 25000   # Ajustá este parámetro para balancear calidad y recuperabilidad

# Cargar imágenes
portadora = leer_imagen_gris("imagen_portadora.png")
oculta = leer_imagen_gris("imagen_oculta.png")

# Ocultamiento
imagen_estego, bits_ocultos, shape_oculta = ocultar_por_cuantizacion_paridad(portadora, oculta, delta)

# Guardar imagen estego
archivo_estego = "imagen_estego_P3.png"
cv2.imwrite(archivo_estego, imagen_estego)
print(f"✅ Imagen estego guardada como: {archivo_estego}")

# Leer imagen estego desde disco y calcular su TF2D
estego_leida = leer_imagen_gris(archivo_estego)
tf_modificada = np.fft.fft2(estego_leida)

# Extracción
recuperada = extraer_desde_paridad(tf_modificada, len(bits_ocultos), shape_oculta, delta)

# Mostrar resultados
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.title("Imagen Portadora")
plt.imshow(portadora, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title(f"Imagen Estego (δ = {delta})")
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
