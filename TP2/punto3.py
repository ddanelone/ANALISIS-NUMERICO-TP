import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import imageio.v3 as iio

def leer_imagen_gris_pil(ruta):
    img = Image.open(ruta).convert('L')
    return np.array(img, dtype=np.float64)

def guardar_tiff_float32(imagen, ruta):
    iio.imwrite(ruta, imagen.astype(np.float32))

def leer_tiff_float32(ruta):
    return iio.imread(ruta).astype(np.float64)

def calcular_max_shape_oculta(shape):
    total_bits = shape[0] * shape[1]
    total_pixeles = total_bits // 8
    lado = int(np.floor(np.sqrt(total_pixeles)))
    return (lado, lado)

def ajustar_imagen_oculta(oculta, max_shape):
    img = Image.fromarray(oculta.astype(np.uint8))
    redim = img.resize((max_shape[1], max_shape[0]), Image.LANCZOS)
    return np.array(redim, dtype=np.float64)

def ocultar_por_cuantizacion_paridad(portadora, oculta, delta):
    h, w = portadora.shape
    tf = np.fft.fft2(portadora)
    tf_shifted = np.fft.fftshift(tf)

    real = np.real(tf_shifted).flatten()
    imag = np.imag(tf_shifted).flatten()

    max_shape_oculta = calcular_max_shape_oculta((h, w))
    oculta_redim = ajustar_imagen_oculta(oculta, max_shape_oculta)

    bits = np.unpackbits(oculta_redim.astype(np.uint8).flatten())
    capacidad_bits = min(len(bits), len(real) + len(imag))
    bits = bits[:capacidad_bits]

    real_mod = real.copy()
    imag_mod = imag.copy()
    idx_real = 0
    idx_imag = 0

    for i, bit in enumerate(bits):
        if i % 2 == 0:
            a = real_mod[idx_real]
            signo = 1 if a >= 0 else -1
            q = int(np.round(abs(a) / delta))
            if (q % 2) != bit:
                q += 1
            real_mod[idx_real] = signo * q * delta
            idx_real += 1
        else:
            b = imag_mod[idx_imag]
            signo = 1 if b >= 0 else -1
            q = int(np.round(abs(b) / delta))
            if (q % 2) != bit:
                q += 1
            imag_mod[idx_imag] = signo * q * delta
            idx_imag += 1

    tf_mod_flat = real_mod + 1j * imag_mod
    tf_mod_shifted = tf_mod_flat.reshape(h, w)
    tf_mod = np.fft.ifftshift(tf_mod_shifted)
    imagen_estego = np.fft.ifft2(tf_mod)
    imagen_estego = np.real(imagen_estego)
    imagen_estego = np.clip(imagen_estego, 0, 255)

    return imagen_estego, bits, oculta_redim.shape

def extraer_desde_paridad(imagen_estego, shape_oculta, delta):
    tf = np.fft.fft2(imagen_estego)
    tf_shifted = np.fft.fftshift(tf)

    real = np.real(tf_shifted).flatten()
    imag = np.imag(tf_shifted).flatten()

    total_bits = shape_oculta[0] * shape_oculta[1] * 8
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
        bits.append(q % 2)

    bits = np.array(bits[: (len(bits) // 8) * 8])
    pixeles = np.packbits(bits)
    total_pixeles = shape_oculta[0] * shape_oculta[1]
    return pixeles[:total_pixeles].reshape(shape_oculta)

# === MAIN ===

ruta_portadora = "globo.png"   # mientras más pixeles tenga, mejor la recuperación, terrible el tiempo de espera.
ruta_oculta = "wp.png"

portadora = leer_imagen_gris_pil(ruta_portadora)
oculta = leer_imagen_gris_pil(ruta_oculta)

valores_delta = [1, 10, 100, 1000, 10000,50000,100000]

for delta in valores_delta:
    print(f"\n🔍 Procesando con delta = {delta}")
    
    imagen_estego, bits_ocultos, shape_oculta = ocultar_por_cuantizacion_paridad(portadora, oculta, delta)

    archivo_estego = f"imagen_estego_delta_{delta}.tiff"
    guardar_tiff_float32(imagen_estego, archivo_estego)
    print(f"✅ Imagen estego guardada como: {archivo_estego}")

    imagen_estego_leida = leer_tiff_float32(archivo_estego)
    shape_oculta = ajustar_imagen_oculta(oculta, calcular_max_shape_oculta(imagen_estego.shape)).shape
    recuperada = extraer_desde_paridad(imagen_estego_leida, shape_oculta, delta)

    plt.figure(figsize=(10, 8))
    plt.suptitle(f"Comparativa para δ = {delta}", fontsize=14)

    plt.subplot(2, 2, 1)
    plt.title("Imagen Portadora")
    plt.imshow(portadora, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.title("Imagen Estego")
    plt.imshow(imagen_estego, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.title("Oculta Redimensionada")
    plt.imshow(ajustar_imagen_oculta(oculta, shape_oculta), cmap='gray', vmin=0, vmax=255)
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.title("Oculta Recuperada")
    plt.imshow(recuperada, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
