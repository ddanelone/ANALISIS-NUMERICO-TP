import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def load_grayscale_image(path, size=None):
    img = Image.open(path).convert('L')
    if size:
        img = img.resize(size, Image.Resampling.LANCZOS)
    return np.array(img)

def binarize(img, threshold=128):
    return (img > threshold).astype(np.uint8)

def embed_using_fft_sign(carrier, secret_bin):
    F = np.fft.fft2(carrier)
    F_shifted = np.fft.fftshift(F)  # centramos las frecuencias para trabajar más fácilmente

    rows, cols = F_shifted.shape

    # Definimos una máscara para modificar solo altas frecuencias (bordes del espectro)
    # Por ejemplo, un "anillo" alrededor de la frecuencia central que no modifica el DC ni bajas frecuencias
    margin = 20  # margen alrededor centro que no modificamos
    mask = np.ones_like(F_shifted, dtype=bool)
    center_row, center_col = rows // 2, cols // 2
    mask[center_row - margin:center_row + margin, center_col - margin:center_col + margin] = False

    # Extraemos los coeficientes a modificar (donde mask es True)
    indices = np.argwhere(mask)

    bits = secret_bin.flatten()
    if bits.size > len(indices):
        raise ValueError(f"Imagen secreta demasiado grande para ocultar en portadora. Max bits: {len(indices)}")

    # Modificamos el signo según bit solo en esos coeficientes seleccionados
    for i, bit in enumerate(bits):
        r, c = indices[i]
        real_part = F_shifted[r, c].real
        imag_part = F_shifted[r, c].imag
        # Si bit=0, signo positivo; si bit=1, signo negativo
        F_shifted[r, c] = complex(abs(real_part) * (1 if bit == 0 else -1),
                                  abs(imag_part) * (1 if bit == 0 else -1))

    # Reconstruimos la imagen inversa
    F_mod = np.fft.ifftshift(F_shifted)
    stego = np.fft.ifft2(F_mod).real
    stego = np.clip(stego, 0, 255).astype(np.uint8)

    return stego, F_shifted, mask

def extract_from_fft_sign(F_shifted, mask, shape_secret):
    indices = np.argwhere(mask)
    bits = []
    for i in range(np.prod(shape_secret)):
        r, c = indices[i]
        real_part = F_shifted[r, c].real
        imag_part = F_shifted[r, c].imag
        bit = 1 if (real_part < 0 or imag_part < 0) else 0
        bits.append(bit)
    extracted_bin = np.array(bits, dtype=np.uint8).reshape(shape_secret)
    return (extracted_bin * 255).astype(np.uint8)

# === Main ===
carrier = load_grayscale_image("memaso.png")
secret = load_grayscale_image("wp.png")
secret_bin = binarize(secret)

# Ajustamos tamaño secreto para que quepa en la cantidad de coeficientes disponibles
rows, cols = carrier.shape
margin = 20
mask_size = np.sum(np.ones((rows, cols), dtype=bool)) - (2 * margin)**2  # aproximado área modificable

if secret_bin.size > mask_size:
    raise ValueError(f"Imagen secreta muy grande para ocultar en portadora: {secret_bin.size} bits > {mask_size}")

stego, F_shifted, mask = embed_using_fft_sign(carrier, secret_bin)
recovered = extract_from_fft_sign(F_shifted, mask, secret_bin.shape)

# === Visualización ===
fig, axs = plt.subplots(2, 2, figsize=(12, 12))
axs[0, 0].imshow(carrier, cmap='gray')
axs[0, 0].set_title("Imagen portadora")
axs[0, 1].imshow(stego, cmap='gray')
axs[0, 1].set_title("Imagen estego")
axs[1, 0].imshow(secret, cmap='gray')
axs[1, 0].set_title("Oculta original")
axs[1, 1].imshow(recovered, cmap='gray')
axs[1, 1].set_title("Oculta extraída")

for ax in axs.ravel():
    ax.axis('off')

plt.tight_layout()
plt.show()
