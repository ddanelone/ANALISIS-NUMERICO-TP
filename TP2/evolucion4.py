import numpy as np
import cv2
import matplotlib.pyplot as plt

def leer_imagen_gris(ruta):
    return cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

def calcular_max_shape_oculta(mask):
    total_bits = np.sum(mask)
    total_pixeles = total_bits // 8
    lado = int(np.floor(np.sqrt(total_pixeles)))
    return (lado, lado)

def ajustar_imagen_oculta(oculta, max_shape):
    if oculta.shape[0] > max_shape[0] or oculta.shape[1] > max_shape[1]:
        print("⚠️ Atención: la imagen oculta es muy grande. Se truncará.")
        oculta_redim = cv2.resize(oculta, (max_shape[1], max_shape[0]))
    else:
        oculta_redim = oculta
    return oculta_redim

def crear_mascara_alta_frecuencia(shape, radio_interno=50):
    """Crea una máscara circular que selecciona solo las frecuencias altas."""
    h, w = shape
    cx, cy = w // 2, h // 2
    y, x = np.ogrid[:h, :w]
    distancia = np.sqrt((x - cx)**2 + (y - cy)**2)
    return distancia >= radio_interno

def ocultar_por_signo_alta_frecuencia_masked(portadora, oculta, radio=50):
    h, w = portadora.shape
    tf = np.fft.fft2(portadora)
    tf_shifted = np.fft.fftshift(tf)

    # Crear máscara de alta frecuencia
    mask = crear_mascara_alta_frecuencia((h, w), radio_interno=radio)
    total_bits = int(np.sum(mask))

    max_shape_oculta = calcular_max_shape_oculta(mask)
    oculta_redim = ajustar_imagen_oculta(oculta, max_shape_oculta)
    bits = np.unpackbits(oculta_redim.flatten())
    bits = bits[:total_bits]

    # Aplicar signos en alta frecuencia
    real = np.real(tf_shifted)
    imag = np.imag(tf_shifted)

    idxs = np.argwhere(mask)
    for i, (y, x) in enumerate(idxs[:len(bits)]):
        signo = -1 if bits[i] == 1 else 1
        real[y, x] = np.abs(real[y, x]) * signo
        imag[y, x] = np.abs(imag[y, x]) * signo

        # Aplicar conjugación hermítica
        y_sym = h - y if y != 0 else 0
        x_sym = w - x if x != 0 else 0
        real[y_sym, x_sym] = real[y, x]
        imag[y_sym, x_sym] = -imag[y, x]  # conjugar parte imaginaria

    tf_mod_shifted = real + 1j * imag
    tf_mod = np.fft.ifftshift(tf_mod_shifted)
    imagen_modificada = np.fft.ifft2(tf_mod)
    imagen_modificada = np.abs(imagen_modificada)
    imagen_modificada = np.clip(imagen_modificada, 0, 255).astype(np.uint8)

    return imagen_modificada, tf, tf_mod, bits, oculta_redim.shape, mask

def extraer_desde_signo_masked(tf_mod, total_bits, shape_oculta, mask):
    tf_shifted = np.fft.fftshift(tf_mod)
    real = np.real(tf_shifted)
    imag = np.imag(tf_shifted)

    idxs = np.argwhere(mask)
    bits = []
    for (y, x) in idxs[:total_bits]:
        if real[y, x] < 0 or imag[y, x] < 0:
            bits.append(1)
        else:
            bits.append(0)

    bits = np.array(bits[: (len(bits) // 8) * 8])
    pixeles = np.packbits(bits)
    total_pixeles = shape_oculta[0] * shape_oculta[1]
    return pixeles[:total_pixeles].reshape(shape_oculta)

# === MAIN ===

# Cargar imágenes
portadora = leer_imagen_gris("imagen_portadora.jpg")
oculta = leer_imagen_gris("imagen_oculta.jpg")

# Ocultar imagen (radio define qué tan lejos del centro empieza la codificación)
modificada, tf_original, tf_modificada, bits_ocultos, shape_oculta, mask = ocultar_por_signo_alta_frecuencia_masked(portadora, oculta, radio=50)

# Recuperar imagen
recuperada = extraer_desde_signo_masked(tf_modificada, len(bits_ocultos), shape_oculta, mask)

# Mostrar resultados
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.title("Imagen Portadora")
plt.imshow(portadora, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title("Imagen Estego (Modificada)")
plt.imshow(modificada, cmap='gray')
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
