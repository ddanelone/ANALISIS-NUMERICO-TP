import numpy as np
import cv2
import matplotlib.pyplot as plt

def leer_imagen_gris(ruta):
    img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    return img.astype(np.float64)

def calcular_max_shape_oculta(mask):
    total_bits = np.sum(mask)
    total_pixeles = total_bits // 8
    lado = int(np.floor(np.sqrt(total_pixeles)))
    return (lado, lado)

def ajustar_imagen_oculta(oculta, max_shape):
    if oculta.shape[0] > max_shape[0] or oculta.shape[1] > max_shape[1]:
        oculta_redim = cv2.resize(oculta, (max_shape[1], max_shape[0]))
    else:
        oculta_redim = oculta
    return oculta_redim

def crear_mascara_alta_frecuencia(shape, radio_interno=50):
    h, w = shape
    cx, cy = w // 2, h // 2
    y, x = np.ogrid[:h, :w]
    distancia = np.sqrt((x - cx)**2 + (y - cy)**2)
    return distancia >= radio_interno

def ocultar_por_signo_alta_frecuencia_simple(portadora, oculta, radio=50):
    h, w = portadora.shape
    tf = np.fft.fft2(portadora)
    tf_shifted = np.fft.fftshift(tf)

    mask = crear_mascara_alta_frecuencia((h, w), radio_interno=radio)
    total_bits = int(np.sum(mask))

    max_shape_oculta = calcular_max_shape_oculta(mask)
    oculta_redim = ajustar_imagen_oculta(oculta, max_shape_oculta)

    bits = np.unpackbits(oculta_redim.astype(np.uint8).flatten())
    bits = bits[:total_bits]

    real = np.real(tf_shifted).copy()
    imag = np.imag(tf_shifted).copy()

    idxs = np.argwhere(mask)
    for i, (y, x) in enumerate(idxs[:len(bits)]):
        signo = -1 if bits[i] == 1 else 1

        real[y, x] = np.abs(real[y, x]) * signo
        imag[y, x] = np.abs(imag[y, x]) * signo

        # Simetría conjugada para que el resultado sea real
        y_sym = (h - y) % h
        x_sym = (w - x) % w
        real[y_sym, x_sym] = np.abs(real[y_sym, x_sym]) * signo
        imag[y_sym, x_sym] = -np.abs(imag[y_sym, x_sym]) * signo

    tf_mod_shifted = real + 1j * imag
    tf_mod = np.fft.ifftshift(tf_mod_shifted)
    imagen_modificada = np.fft.ifft2(tf_mod)
    imagen_modificada = np.real(imagen_modificada)
    imagen_modificada = np.clip(imagen_modificada, 0, 255).astype(np.uint8)

    return imagen_modificada, mask, len(bits), oculta_redim.shape

def extraer_desde_signo_simple(tf_mod, total_bits, shape_oculta, mask):
    tf_shifted = np.fft.fftshift(tf_mod)
    real = np.real(tf_shifted)
    imag = np.imag(tf_shifted)

    idxs = np.argwhere(mask)
    bits = []
    for (y, x) in idxs[:total_bits]:
        bit = 1 if real[y, x] < 0 or imag[y, x] < 0 else 0
        bits.append(bit)

    bits = np.array(bits[: (len(bits) // 8) * 8])  # múltiplos de 8
    pixeles = np.packbits(bits)
    total_pixeles = shape_oculta[0] * shape_oculta[1]
    return pixeles[:total_pixeles].reshape(shape_oculta)

# === MAIN ===

archivo_portadora = "imagen_portadora.png"
archivo_oculta = "imagen_oculta.png"
archivo_estego = "imagen_estego.png"

portadora = leer_imagen_gris(archivo_portadora)
oculta = leer_imagen_gris(archivo_oculta)

modificada, mask, total_bits, shape_oculta = ocultar_por_signo_alta_frecuencia_simple(
    portadora, oculta, radio=50
)

cv2.imwrite(archivo_estego, modificada)
print(f"✅ Imagen estego guardada como: {archivo_estego}")

estego_leida = leer_imagen_gris(archivo_estego)
tf_modificada = np.fft.fft2(estego_leida)
recuperada = extraer_desde_signo_simple(tf_modificada, total_bits, shape_oculta, mask)

plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.title("Portadora")
plt.imshow(portadora, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title("Estego (guardada)")
plt.imshow(estego_leida, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.title("Oculta original (redimensionada)")
plt.imshow(cv2.resize(oculta, shape_oculta[::-1]), cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.title("Oculta recuperada")
plt.imshow(recuperada, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
