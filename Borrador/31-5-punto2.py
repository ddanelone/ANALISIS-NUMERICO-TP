import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from scipy.stats import mode

# --- Parámetros ---
R_MIN = 50           # Mínimo radio para alta frecuencia
REPETICION = 3       # Bits repetidos para robustez (votación mayoritaria)
PORTADORA_PATH = "globo.png"
OCULTA_PATH = "wp.png"
SALIDA_PATH = "imagen_estego2.tiff"

# --- Utilidades ---
def imagen_a_bits(img):
    return np.unpackbits(img.flatten())

def bits_a_imagen(bits, shape):
    total_bits = np.prod(shape) * 8
    bits = bits[:total_bits]
    bytes_ = np.packbits(bits)
    return bytes_.reshape(shape)

def obtener_posiciones_alta_frecuencia(shape, r_min):
    M, N = shape
    cx, cy = M // 2, N // 2
    Y, X = np.ogrid[:M, :N]
    R = np.sqrt((X - cx)**2 + (Y - cy)**2)
    mask = R > r_min
    coords = np.column_stack(np.where(mask))
    posiciones = []
    vistos = set()
    for y, x in coords:
        y_sym = (-y) % M
        x_sym = (-x) % N
        clave = tuple(sorted([(y, x), (y_sym, x_sym)]))
        if clave not in vistos:
            posiciones.append((y, x))
            vistos.add(clave)
    return posiciones

def codificar_en_fft(F, bits, posiciones, repeticion):
    F_mod = F.copy()
    M, N = F.shape
    bits_rep = np.repeat(bits, repeticion)
    for k, (i, j) in enumerate(posiciones[:len(bits_rep)]):
        bit = bits_rep[k]
        a, b = F[i, j].real, F[i, j].imag
        b = abs(b) if bit == 0 else -abs(b)
        F_mod[i, j] = complex(a, b)
        i_sym, j_sym = (-i) % M, (-j) % N
        F_mod[i_sym, j_sym] = complex(a, -b)
    return F_mod

def decodificar_desde_fft(F, posiciones, cantidad_bits, repeticion):
    bits = []
    for k in range(cantidad_bits):
        votos = []
        for r in range(repeticion):
            idx = k * repeticion + r
            if idx >= len(posiciones):
                break
            i, j = posiciones[idx]
            b = F[i, j].imag
            votos.append(1 if b < 0 else 0)
        if votos:
            m = mode(votos, keepdims=True)
            bits.append(int(m.mode[0]) if hasattr(m.mode, '__getitem__') else int(m.mode))
        else:
            bits.append(0)  # Relleno por si falta alguno
    return np.array(bits, dtype=np.uint8)

# --- Carga de imágenes ---
img_portadora = imageio.imread(PORTADORA_PATH).astype(np.float64)
if img_portadora.ndim == 3:
    img_portadora = np.mean(img_portadora, axis=2)

img_oculta = imageio.imread(OCULTA_PATH).astype(np.uint8)
if img_oculta.ndim == 3:
    img_oculta = np.mean(img_oculta, axis=2).astype(np.uint8)

bits_oculta = imagen_a_bits(img_oculta)

print(f"[INFO] Imagen oculta: {img_oculta.shape}, bits a ocultar: {len(bits_oculta)}")

# --- FFT ---
F = fftshift(fft2(img_portadora))

# --- Posiciones válidas ---
posiciones = obtener_posiciones_alta_frecuencia(F.shape, R_MIN)
print(f"[INFO] Posiciones disponibles: {len(posiciones)}")

if len(posiciones) < len(bits_oculta) * REPETICION:
    raise ValueError("No hay suficientes posiciones en alta frecuencia para ocultar la imagen.")

# --- Codificación ---
F_mod = codificar_en_fft(F, bits_oculta, posiciones, REPETICION)
img_estego = np.real(ifft2(ifftshift(F_mod)))

imageio.imwrite(SALIDA_PATH, np.clip(img_estego, 0, 255).astype(np.uint8))
print(f"[INFO] Imagen estego guardada en: {SALIDA_PATH}")

# --- Visualización: Portadora vs Estego ---
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.imshow(img_portadora, cmap='gray')
plt.title("Portadora")
plt.axis('off')
plt.subplot(1, 2, 2)
plt.imshow(img_estego, cmap='gray')
plt.title("Imagen Estego")
plt.axis('off')
plt.tight_layout()
plt.show()

# --- Decodificación ---
img_estego_leida = imageio.imread(SALIDA_PATH).astype(np.float64)
F_leida = fftshift(fft2(img_estego_leida))
bits_recuperados = decodificar_desde_fft(F_leida, posiciones, len(bits_oculta), REPETICION)
print(f"[INFO] Bits recuperados: {len(bits_recuperados)}")

img_recuperada = bits_a_imagen(bits_recuperados, img_oculta.shape)

# --- Visualización: Oculta vs Recuperada ---
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.imshow(img_oculta, cmap='gray')
plt.title("Oculta Original")
plt.axis('off')
plt.subplot(1, 2, 2)
plt.imshow(img_recuperada, cmap='gray')
plt.title("Recuperada")
plt.axis('off')
plt.tight_layout()
plt.show()

# --- Diferencias ---
diferencia = np.abs(img_oculta.astype(int) - img_recuperada.astype(int))
plt.figure(figsize=(5, 4))
plt.imshow(diferencia, cmap='hot')
plt.title("Diferencia Absoluta")
plt.axis('off')
plt.colorbar()
plt.show()
