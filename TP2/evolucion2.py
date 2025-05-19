import numpy as np
import cv2
import matplotlib.pyplot as plt

# === FUNCIONES AUXILIARES ===

def leer_imagen_gris(ruta):
    """Lee una imagen en escala de grises."""
    return cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

def calcular_max_shape_oculta(shape_portadora):
    """Calcula el tamaño máximo de la imagen oculta para que quepa en los bits disponibles."""
    total_bits = shape_portadora[0] * shape_portadora[1]
    total_pixeles = total_bits // 8
    lado = int(np.floor(np.sqrt(total_pixeles)))
    return (lado, lado)

def ajustar_imagen_oculta(oculta, shape_portadora):
    """Redimensiona la imagen oculta para que no exceda la capacidad de la portadora."""
    max_shape = calcular_max_shape_oculta(shape_portadora)
    if oculta.shape[0] > max_shape[0] or oculta.shape[1] > max_shape[1]:
        print("⚠️ Atención: la imagen oculta es muy grande. Se truncará para que entre en la portadora.")
        oculta_redim = cv2.resize(oculta, (max_shape[1], max_shape[0]))
    else:
        oculta_redim = oculta
    return oculta_redim

# === OCULTAMIENTO ===

def ocultar_por_signo(portadora, oculta):
    h, w = portadora.shape
    tf = np.fft.fft2(portadora)
    real = np.real(tf).flatten()
    imag = np.imag(tf).flatten()
    capacidad_bits = len(real)

    # Redimensionar la imagen oculta si es necesario
    oculta_redim = ajustar_imagen_oculta(oculta, (h, w))
    bits = np.unpackbits(oculta_redim.flatten())
    bits = bits[:capacidad_bits]  # Truncar si hay más bits que coeficientes

    # Cambiar signos según los bits
    signos = np.where(bits == 0, 1, -1)
    real_mod = np.abs(real[:len(bits)]) * signos
    imag_mod = np.abs(imag[:len(bits)]) * signos

    # Conservar el resto sin modificar
    real_final = np.concatenate([real_mod, real[len(bits):]])
    imag_final = np.concatenate([imag_mod, imag[len(bits):]])

    tf_mod = (real_final + 1j * imag_final).reshape(h, w)
    imagen_modificada = np.fft.ifft2(tf_mod)
    imagen_modificada = np.abs(imagen_modificada)
    imagen_modificada = np.clip(imagen_modificada, 0, 255).astype(np.uint8)

    return imagen_modificada, tf, tf_mod, bits, oculta_redim.shape

# === EXTRACCIÓN ===

def extraer_desde_signo(tf_mod, total_bits, shape_oculta):
    real = np.real(tf_mod).flatten()[:total_bits]
    imag = np.imag(tf_mod).flatten()[:total_bits]
    bits = np.where((real < 0) | (imag < 0), 1, 0)

    bits = bits[:(len(bits) // 8) * 8]
    pixeles = np.packbits(bits).flatten()
    total_pixeles = shape_oculta[0] * shape_oculta[1]
    return pixeles[:total_pixeles].reshape(shape_oculta)

# === MAIN ===

# Cargar imágenes
portadora = leer_imagen_gris("imagen_portadora.png")
oculta = leer_imagen_gris("imagen_oculta.png")

# Ocultar imagen
modificada, tf_original, tf_modificada, bits_ocultos, shape_oculta = ocultar_por_signo(portadora, oculta)

# Recuperar imagen
recuperada = extraer_desde_signo(tf_modificada, len(bits_ocultos), shape_oculta)

# Mostrar resultados
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.title("Imagen Portadora")
plt.imshow(portadora, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title("Imagen Modificada")
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
