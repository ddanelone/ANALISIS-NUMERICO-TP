import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import imageio.v3 as iio

def cargar_grises(path):
    return np.array(Image.open(path).convert("L"), dtype=np.float64)

def ajustar_oculta(oculta, portadora_shape, rep):
    max_bits = portadora_shape[0] * portadora_shape[1]
    max_bits_usables = max_bits // rep
    max_pixeles = max_bits_usables // 8
    lado = int(np.floor(np.sqrt(max_pixeles)))
    if oculta.shape[0] > lado or oculta.shape[1] > lado:
        print("⚠️ Redimensionando imagen oculta a:", lado, "x", lado)
        oculta = np.array(Image.fromarray(oculta.astype(np.uint8)).resize((lado, lado)))
    return oculta

def ocultar(portadora, oculta, delta, rep):
    tf = np.fft.fftshift(np.fft.fft2(portadora))
    real = np.real(tf).flatten()
    imag = np.imag(tf).flatten()

    oculta = ajustar_oculta(oculta, portadora.shape, rep)
    bits = np.unpackbits(oculta.astype(np.uint8).flatten())
    bits_rep = np.repeat(bits, rep)

    capacidad = min(len(bits_rep), len(real) + len(imag))
    bits_rep = bits_rep[:capacidad]

    real_mod = real.copy()
    imag_mod = imag.copy()
    idx_real = idx_imag = 0

    for i, bit in enumerate(bits_rep):
        if i % 2 == 0:
            a = real_mod[idx_real]
            signo = 1 if a >= 0 else -1
            q = int(np.round(abs(a) / delta))
            if q % 2 != bit:
                q += 1
            real_mod[idx_real] = signo * q * delta
            idx_real += 1
        else:
            b = imag_mod[idx_imag]
            signo = 1 if b >= 0 else -1
            q = int(np.round(abs(b) / delta))
            if q % 2 != bit:
                q += 1
            imag_mod[idx_imag] = signo * q * delta
            idx_imag += 1

    tf_mod = (real_mod + 1j * imag_mod).reshape(portadora.shape)
    tf_mod = np.fft.ifftshift(tf_mod)
    estego = np.fft.ifft2(tf_mod)
    estego = np.real(estego)
    estego = np.clip(estego, 0, 255)

    return estego.astype(np.float32), oculta.shape

def extraer(estego, delta, shape_oculta, rep):
    tf = np.fft.fftshift(np.fft.fft2(estego))
    real = np.real(tf).flatten()
    imag = np.imag(tf).flatten()

    total_bits = shape_oculta[0] * shape_oculta[1] * 8
    total_bits_rep = total_bits * rep

    bits_extraidos = []
    idx_real = idx_imag = 0

    for i in range(total_bits_rep):
        if i % 2 == 0:
            a = real[idx_real]
            idx_real += 1
        else:
            a = imag[idx_imag]
            idx_imag += 1
        q = int(np.round(abs(a) / delta))
        bits_extraidos.append(q % 2)

    bits_finales = []
    for i in range(0, len(bits_extraidos), rep):
        bloque = bits_extraidos[i:i+rep]
        if len(bloque) < rep:
            break
        bit = int(np.sum(bloque) >= (rep // 2 + 1))
        bits_finales.append(bit)

    bits_finales = np.array(bits_finales[: (len(bits_finales) // 8) * 8])
    pixeles = np.packbits(bits_finales)
    return pixeles[:shape_oculta[0] * shape_oculta[1]].reshape(shape_oculta)

# === MAIN ===
delta = 100000     # fuerza de cuantización
rep = 1          # repeticiones por bit para votación

# === ENCODER ===
portadora = cargar_grises("imagen_oculta.png")
oculta = cargar_grises("wp.png")
estego, shape_oculta = ocultar(portadora, oculta, delta=delta, rep=rep)
iio.imwrite("imagen_estego.tiff", estego.astype(np.float32))
print("✅ Imagen estego guardada como imagen_estego.tiff")

# === DECODER ===
estego_leida = iio.imread("imagen_estego.tiff").astype(np.float64)
recuperada = extraer(estego_leida, delta=delta, shape_oculta=shape_oculta, rep=rep)

# === VISUALIZACIÓN ===
fig, axs = plt.subplots(1, 4, figsize=(16, 5))
axs[0].imshow(portadora, cmap='gray', vmin=0, vmax=255)
axs[0].set_title("Portadora")
axs[1].imshow(estego_leida, cmap='gray', vmin=0, vmax=255)
axs[1].set_title(f"Estego (δ={delta}, rep={rep})")
axs[2].imshow(oculta, cmap='gray', vmin=0, vmax=255)
axs[2].set_title("Oculta ajustada")
axs[3].imshow(recuperada, cmap='gray', vmin=0, vmax=255)
axs[3].set_title("Recuperada (votación)")
for ax in axs:
    ax.axis('off')
plt.tight_layout()
plt.show()
