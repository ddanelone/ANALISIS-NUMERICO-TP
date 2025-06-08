import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Parámetros
IMAGE_CARRIER = "memaso.png"
IMAGE_SECRET = "wp.png"
IMAGE_OUT = "imagen_estego2.png"
REPETITIONS = 5
R_START, R_END = 50, 512
MAG_THRESHOLD = 50  # Umbral mínimo para |a + ib|

def load_grayscale_image(path, shape=None):
    img = Image.open(path).convert("L")
    if shape:
        img = img.resize(shape, Image.Resampling.LANCZOS)
    return np.array(img)

def embed_bits_sign_real_imag(carrier, secret_bits, reps=1):
    F = np.fft.fft2(carrier)
    F_shift = np.fft.fftshift(F)
    rows, cols = F_shift.shape
    cx, cy = rows // 2, cols // 2

    total_bits = len(secret_bits)
    embedded_bits = 0
    bit_idx = 0

    coords = []
    for r in range(R_START, R_END):
        for theta in np.linspace(0, 2 * np.pi, num=4 * r, endpoint=False):
            x = int(cx + r * np.cos(theta))
            y = int(cy + r * np.sin(theta))
            if 0 <= x < rows and 0 <= y < cols:
                if np.abs(F_shift[x, y]) >= MAG_THRESHOLD:
                    coords.append((x, y))
    coords = coords[: (total_bits * reps)]

    for i, (x, y) in enumerate(coords):
        if bit_idx >= total_bits:
            break
        bit = secret_bits[bit_idx // reps]
        val = F_shift[x, y]
        a, b = val.real, val.imag
        if bit == 0:
            a, b = np.abs(a), np.abs(b)
        else:
            a, b = -np.abs(a), -np.abs(b)
        F_shift[x, y] = a + 1j * b
        if (i + 1) % reps == 0:
            bit_idx += 1

    print(f"Bits embebidos realmente: {bit_idx}/{total_bits}")
    F_ishift = np.fft.ifftshift(F_shift)
    img_stego = np.fft.ifft2(F_ishift).real
    img_stego = np.clip(img_stego, 0, 255)
    return img_stego.astype(np.uint8)

def extract_bits_sign_real_imag(stego_img, total_bits, reps=1):
    F = np.fft.fft2(stego_img)
    F_shift = np.fft.fftshift(F)
    rows, cols = F_shift.shape
    cx, cy = rows // 2, cols // 2

    bits = []
    coords = []
    for r in range(R_START, R_END):
        for theta in np.linspace(0, 2 * np.pi, num=4 * r, endpoint=False):
            x = int(cx + r * np.cos(theta))
            y = int(cy + r * np.sin(theta))
            if 0 <= x < rows and 0 <= y < cols:
                if np.abs(F_shift[x, y]) >= MAG_THRESHOLD:
                    coords.append((x, y))
    coords = coords[: (total_bits * reps)]

    for i in range(0, len(coords), reps):
        votes = []
        for j in range(reps):
            if i + j >= len(coords):
                break
            x, y = coords[i + j]
            val = F_shift[x, y]
            a, b = val.real, val.imag
            bit = 0 if (a >= 0 and b >= 0) else 1
            votes.append(bit)
        if votes:
            bits.append(int(round(np.mean(votes))))
    return bits[:total_bits]

def bits_to_image(bits, shape):
    arr = np.array(bits, dtype=np.uint8) * 255
    return arr.reshape(shape)

def image_to_bits(img):
    return (img.flatten() > 127).astype(np.uint8).tolist()

# Carga de imágenes
carrier = load_grayscale_image(IMAGE_CARRIER)
secret = load_grayscale_image(IMAGE_SECRET, shape=(256, 256))
bits_secret = image_to_bits(secret)

# Codificación
stego = embed_bits_sign_real_imag(carrier, bits_secret, reps=REPETITIONS)
Image.fromarray(stego).save(IMAGE_OUT)

# Decodificación
stego_read = load_grayscale_image(IMAGE_OUT)
bits_rec = extract_bits_sign_real_imag(stego_read, len(bits_secret), reps=REPETITIONS)
secret_rec = bits_to_image(bits_rec, secret.shape)

# Visualización
fig, axs = plt.subplots(2, 2, figsize=(8, 8))
axs[0, 0].imshow(carrier, cmap='gray')
axs[0, 0].set_title("Imagen portadora")
axs[0, 1].imshow(stego, cmap='gray')
axs[0, 1].set_title("Imagen estego")
axs[1, 0].imshow(secret, cmap='gray')
axs[1, 0].set_title("Oculta original")
axs[1, 1].imshow(secret_rec, cmap='gray')
axs[1, 1].set_title("Oculta extraída")
for ax in axs.flat:
    ax.axis('off')
plt.tight_layout()
plt.show()
