import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

# === Utilidades ===

def load_grayscale_image(path, size=None):
    img = Image.open(path).convert('L')
    if size:
        img = img.resize(size, Image.Resampling.LANCZOS)
    return np.array(img)

def binarize(img, threshold=128):
    return (img > threshold).astype(np.uint8)

# === Versión 1: EN MEMORIA ===

def embed_fft_memory(carrier, secret_bin, margin=20):
    F = np.fft.fft2(carrier)
    F_shifted = np.fft.fftshift(F)
    rows, cols = carrier.shape
    mask = np.ones_like(F_shifted, dtype=bool)
    mask[rows//2 - margin : rows//2 + margin, cols//2 - margin : cols//2 + margin] = False
    indices = np.argwhere(mask)
    bits = secret_bin.flatten()
    if len(bits) > len(indices):
        raise ValueError("La imagen secreta es demasiado grande.")
    for i, bit in enumerate(bits):
        r, c = indices[i]
        a, b = F_shifted[r, c].real, F_shifted[r, c].imag
        F_shifted[r, c] = complex(abs(a) if bit == 0 else -abs(a),
                                  abs(b) if bit == 0 else -abs(b))
    F_mod = np.fft.ifftshift(F_shifted)
    stego = np.fft.ifft2(F_mod).real
    stego = np.clip(stego, 0, 255).astype(np.uint8)
    return stego, F_shifted, mask

def extract_fft_memory(F_shifted, mask, shape_secret):
    indices = np.argwhere(mask)
    bits = []
    for i in range(np.prod(shape_secret)):
        r, c = indices[i]
        a, b = F_shifted[r, c].real, F_shifted[r, c].imag
        bits.append(1 if a < 0 or b < 0 else 0)
    return (np.array(bits).reshape(shape_secret) * 255).astype(np.uint8)

# === Versión 2: Guardando la FFT (en vez de guardar imagen) ===

def embed_fft_save(carrier, secret_bin, margin=20, fft_path='fft_guardada.npy'):
    stego, F_shifted, mask = embed_fft_memory(carrier, secret_bin, margin)
    np.save(fft_path, F_shifted)
    return stego, mask

def extract_fft_load(fft_path, mask, shape_secret):
    F_shifted = np.load(fft_path)
    return extract_fft_memory(F_shifted, mask, shape_secret)

# === Métricas ===

def compare_images(img1, img2, label=""):
    abs_diff = np.abs(img1.astype(int) - img2.astype(int))
    max_diff = np.max(abs_diff)
    mean_diff = np.mean(abs_diff)
    equal_pixels = np.sum(img1 == img2)
    total_pixels = img1.size
    perc_equal = 100 * equal_pixels / total_pixels

    fft1 = np.fft.fftshift(np.fft.fft2(img1))
    fft2 = np.fft.fftshift(np.fft.fft2(img2))
    fft_diff = np.mean(np.abs(fft1 - fft2))

    print(f"\n=== Comparación entre imágenes {label} ===")
    print(f"Máxima diferencia absoluta: {max_diff}")
    print(f"Diferencia media: {mean_diff:.2f}")
    print(f"Porcentaje de píxeles exactamente iguales: {perc_equal:.2f}%")
    print(f"Diferencia promedio en dominio de Fourier: {fft_diff:.2f}")

# === Main ===

# Cargar imágenes
carrier = load_grayscale_image("memaso.png")
secret = load_grayscale_image("wp.png", size=(256, 256))
secret_bin = binarize(secret)

# ---- Versión 1: Memoria ----
stego_mem, F_shifted_mem, mask = embed_fft_memory(carrier, secret_bin)
recovered_mem = extract_fft_memory(F_shifted_mem, mask, secret_bin.shape)

# ---- Versión 2: Guardado de FFT ----
stego_saved, _ = embed_fft_save(carrier, secret_bin, margin=20, fft_path="fft_guardada.npy")
recovered_saved = extract_fft_load("fft_guardada.npy", mask, secret_bin.shape)

# === Comparaciones ===
compare_images(stego_mem, stego_saved, "estego (memoria vs FFT guardado)")
compare_images(recovered_mem, recovered_saved, "recuperadas (memoria vs FFT guardado)")

# === Visualización ===
fig, axs = plt.subplots(3, 2, figsize=(12, 14))

axs[0, 0].imshow(carrier, cmap='gray')
axs[0, 0].set_title("Imagen Portadora")

axs[0, 1].imshow(secret, cmap='gray')
axs[0, 1].set_title("Imagen Oculta Original")

axs[1, 0].imshow(stego_mem, cmap='gray')
axs[1, 0].set_title("Estego (solo memoria)")

axs[1, 1].imshow(recovered_mem, cmap='gray')
axs[1, 1].set_title("Recuperada (memoria)")

axs[2, 0].imshow(stego_saved, cmap='gray')
axs[2, 0].set_title("Estego (desde FFT guardada)")

axs[2, 1].imshow(recovered_saved, cmap='gray')
axs[2, 1].set_title("Recuperada (desde FFT)")

for ax in axs.ravel():
    ax.axis('off')
plt.tight_layout()
plt.show()
