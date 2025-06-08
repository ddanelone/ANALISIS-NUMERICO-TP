import numpy as np
import cv2
import matplotlib.pyplot as plt

def leer_imagen_gris(ruta):
    return cv2.imread(ruta, cv2.IMREAD_GRAYSCALE).astype(np.float64)

def crear_mascara_alta_frecuencia(shape, radio_interno=50):
    h, w = shape
    cy, cx = h // 2, w // 2
    y, x = np.ogrid[:h, :w]
    distancia = np.sqrt((x - cx)**2 + (y - cy)**2)
    return distancia >= radio_interno

def ocultar_imagen(portadora, oculta, radio=50, epsilon=5):
    h, w = portadora.shape
    tf = np.fft.fft2(portadora)
    tf_shifted = np.fft.fftshift(tf)

    mask = crear_mascara_alta_frecuencia((h, w), radio_interno=radio)
    indices = np.argwhere(mask)

    bits_oculta = np.unpackbits(oculta.astype(np.uint8).flatten())
    if len(indices) < len(bits_oculta):
        raise ValueError("La imagen oculta es demasiado grande para esta portadora")

    real = np.real(tf_shifted)
    imag = np.imag(tf_shifted)

    usados = 0
    for i, (y, x) in enumerate(indices):
        if usados >= len(bits_oculta):
            break
        magn = np.hypot(real[y, x], imag[y, x])
        if magn < epsilon:
            continue  # muy poco significativos

        bit = bits_oculta[usados]
        sgn = -1 if bit == 1 else 1
        real[y, x] = sgn * np.abs(real[y, x])
        imag[y, x] = sgn * np.abs(imag[y, x])

        # simetría hermítica
        ys, xs = h - y if y != 0 else 0, w - x if x != 0 else 0
        real[ys, xs] = real[y, x]
        imag[ys, xs] = -imag[y, x]

        usados += 1

    tf_mod = np.fft.ifftshift(real + 1j * imag)
    img_estego = np.fft.ifft2(tf_mod).real
    img_estego = np.clip(img_estego, 0, 255).astype(np.uint8)

    # Guardar
    cv2.imwrite("imagen_estego.png", img_estego)
    np.savez("datos_estego.npz", tf_mod_real=np.real(tf_mod), tf_mod_imag=np.imag(tf_mod),
             total_bits=usados, shape_oculta=oculta.shape, mask=mask)

    return img_estego

def extraer_desde_archivos():
    datos = np.load("datos_estego.npz")
    real = datos["tf_mod_real"]
    imag = datos["tf_mod_imag"]
    tf_mod = real + 1j * imag
    total_bits = int(datos["total_bits"])
    shape_oculta = tuple(datos["shape_oculta"])
    mask = datos["mask"]

    tf_shifted = np.fft.fftshift(tf_mod)
    real = np.real(tf_shifted)
    imag = np.imag(tf_shifted)

    indices = np.argwhere(mask)
    bits = []
    for y, x in indices:
        if len(bits) >= total_bits:
            break
        bit = 1 if (real[y, x] < 0 or imag[y, x] < 0) else 0
        bits.append(bit)

    bits = np.array(bits[: (len(bits) // 8) * 8])
    pixeles = np.packbits(bits)
    total_pixeles = shape_oculta[0] * shape_oculta[1]
    return pixeles[:total_pixeles].reshape(shape_oculta)

# === MAIN ===

# Cargar imágenes
portadora = leer_imagen_gris("imagen_portadora.png")
oculta = leer_imagen_gris("imagen_oculta.png")

# Redimensionar imagen oculta (opcional)
if oculta.shape[0] > portadora.shape[0] or oculta.shape[1] > portadora.shape[1]:
    print("⚠️ Redimensionando imagen oculta para que quepa en la portadora.")
    nuevo_lado = min(portadora.shape)
    oculta = cv2.resize(oculta, (nuevo_lado, nuevo_lado), interpolation=cv2.INTER_AREA)

# Ocultar
estego = ocultar_imagen(portadora, oculta)

# Extraer
recuperada = extraer_desde_archivos()

# === Mostrar resultados ===
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.title("Imagen Portadora")
plt.imshow(portadora, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title("Imagen Estego")
plt.imshow(estego, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.title("Imagen Oculta Original")
plt.imshow(oculta, cmap='gray')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.title("Imagen Oculta Recuperada")
plt.imshow(recuperada, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
