import numpy as np
import cv2
import matplotlib.pyplot as plt
import imageio.v3 as iio

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
        print("⚠️ Atención: la imagen oculta es muy grande. Se truncará.")
        oculta_redim = cv2.resize(oculta, (max_shape[1], max_shape[0]), interpolation=cv2.INTER_AREA)
    else:
        oculta_redim = oculta
    return oculta_redim

def crear_mascara_alta_frecuencia(shape, radio_interno=50):
    h, w = shape
    cx, cy = w // 2, h // 2
    y, x = np.ogrid[:h, :w]
    distancia = np.sqrt((x - cx)**2 + (y - cy)**2)
    return distancia >= radio_interno

def ocultar_por_signo_alta_frecuencia_masked(portadora, oculta, radio=50, epsilon=1.0):
    h, w = portadora.shape
    tf = np.fft.fft2(portadora)
    tf_shifted = np.fft.fftshift(tf)

    mask = crear_mascara_alta_frecuencia((h, w), radio_interno=radio)
    total_bits = int(np.sum(mask))

    max_shape_oculta = calcular_max_shape_oculta(mask)
    oculta_redim = ajustar_imagen_oculta(oculta, max_shape_oculta)
    bits = np.unpackbits(oculta_redim.astype(np.uint8).flatten())
    bits = bits[:total_bits]

    real = np.real(tf_shifted)
    imag = np.imag(tf_shifted)

    idxs = np.argwhere(mask)
    for i, (y, x) in enumerate(idxs[:len(bits)]):
        r, im = real[y, x], imag[y, x]
        mag = np.hypot(r, im)

        # Si la magnitud es demasiado baja, saltar (para evitar distorsión)
        if mag < epsilon:
            continue

        signo = -1 if bits[i] == 1 else 1
        real[y, x] = signo * abs(r)
        imag[y, x] = signo * abs(im)

        # Aplicar simetría conjugada estricta
        y_sym = (-y) % h
        x_sym = (-x) % w
        real[y_sym, x_sym] = real[y, x]
        imag[y_sym, x_sym] = -imag[y, x]

    tf_mod_shifted = real + 1j * imag
    tf_mod = np.fft.ifftshift(tf_mod_shifted)
    imagen_modificada = np.fft.ifft2(tf_mod).real

    # Clipping antes de guardar
    imagen_modificada = np.clip(imagen_modificada, 0, 255)

    return imagen_modificada, tf, tf_mod, bits, oculta_redim.shape, mask

def extraer_desde_signo_masked(tf_mod, total_bits, shape_oculta, mask):
    tf_shifted = np.fft.fftshift(tf_mod)
    real = np.real(tf_shifted)
    imag = np.imag(tf_shifted)

    idxs = np.argwhere(mask)
    bits = []
    for (y, x) in idxs[:total_bits]:
        b = int(real[y, x] < 0 or imag[y, x] < 0)
        bits.append(b)

    bits = np.array(bits[: (len(bits) // 8) * 8])
    pixeles = np.packbits(bits)
    total_pixeles = shape_oculta[0] * shape_oculta[1]
    return pixeles[:total_pixeles].reshape(shape_oculta)

# === MAIN ===

# Cargar imágenes
portadora = leer_imagen_gris("memaso.png")
oculta = leer_imagen_gris("wp.png")

# Ocultar imagen
modificada, tf_original, tf_modificada, bits_ocultos, shape_oculta, mask = ocultar_por_signo_alta_frecuencia_masked(
    portadora, oculta, radio=50, epsilon=1.0
)

# Guardar imagen estego en TIFF 32-bit float
iio.imwrite("imagen_estego.tiff", (modificada / 255).astype(np.float32))

# Leer la imagen estego desde TIFF
estego_leida = iio.imread("imagen_estego.tiff").astype(np.float64) * 255

# Transformada y extracción
tf_estego_leida = np.fft.fft2(estego_leida)
recuperada = extraer_desde_signo_masked(tf_estego_leida, len(bits_ocultos), shape_oculta, mask)

# === Mostrar resultados ===

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.title("Imagen Portadora")
plt.imshow(portadora, cmap='gray', vmin=0, vmax=255)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Imagen Estego (TIFF)")
plt.imshow(estego_leida, cmap='gray', vmin=0, vmax=255)
plt.axis('off')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.title("Imagen Oculta Original")
plt.imshow(cv2.resize(oculta, shape_oculta[::-1]), cmap='gray', vmin=0, vmax=255)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Imagen Oculta Recuperada")
plt.imshow(recuperada, cmap='gray', vmin=0, vmax=255)
plt.axis('off')
plt.tight_layout()
plt.show()
