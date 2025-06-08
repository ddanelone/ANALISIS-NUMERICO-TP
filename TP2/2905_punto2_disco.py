# Invertimos los signos en la parte real e imaginaria de la FFT de la imagen portadora
# Requiere más repeticiones para la votación mayoritaria y, por supuesto, más pixeles 
# en la imagen portadora vs la oculta.
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def cargar_grises(path):
    return np.array(Image.open(path).convert('L'))

def binarizar(imagen):
    return (imagen > 127).astype(np.uint8)

def obtener_posiciones_validas(shape, radio_exclusion=40, n=0):
    h, w = shape
    centro = (h // 2, w // 2)
    Y, X = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    dist = np.sqrt((Y - centro[0]) ** 2 + (X - centro[1]) ** 2)
    mask = dist > radio_exclusion
    indices = np.argwhere(mask)
    posiciones = []
    usados = set()
    for i, j in indices:
        ci, cj = (-i) % h, (-j) % w
        if (ci, cj) not in usados and (i, j) not in usados and (i, j) < (ci, cj):
            posiciones.append((i, j, ci, cj))
            usados.add((i, j))
            usados.add((ci, cj))
    np.random.shuffle(posiciones)
    return posiciones[:n]

def ocultar_fft(carrier, hidden, rep=3):
    carrier_f = np.fft.fft2(carrier)
    hidden_bin = binarizar(hidden).flatten()
    bits_rep = np.repeat(hidden_bin, rep)
    n_bits = len(bits_rep)
    posiciones = obtener_posiciones_validas(carrier.shape, radio_exclusion=40, n=n_bits)

    for idx in range(n_bits):
        i, j, ci, cj = posiciones[idx]
        bit = bits_rep[idx]
        val = carrier_f[i, j]

        if idx % 2 == 0:  # codificamos en parte real
            r = -abs(val.real) if bit == 1 else abs(val.real)
            carrier_f[i, j] = complex(r, val.imag)
            carrier_f[ci, cj] = complex(-r, val.imag)
        else:  # codificamos en parte imaginaria
            im = -abs(val.imag) if bit == 1 else abs(val.imag)
            carrier_f[i, j] = complex(val.real, im)
            carrier_f[ci, cj] = complex(val.real, -im)

    estego = np.real(np.fft.ifft2(carrier_f))
    estego = np.clip(estego, 0, 255).astype(np.uint8)
    return estego, posiciones

def extraer_fft(estego, shape_hidden, posiciones, rep=3):
    estego_f = np.fft.fft2(estego)
    n_bits_total = shape_hidden[0] * shape_hidden[1] * rep
    bits_extraidos = []

    for idx in range(n_bits_total):
        i, j, _, _ = posiciones[idx]
        val = estego_f[i, j]
        if idx % 2 == 0:  # leemos de parte real
            bit = 1 if val.real < 0 else 0
        else:  # leemos de parte imaginaria
            bit = 1 if val.imag < 0 else 0
        bits_extraidos.append(bit)

    bits = []
    for i in range(0, len(bits_extraidos), rep):
        votos = bits_extraidos[i:i+rep]
        bits.append(int(np.sum(votos) >= (rep / 2)))

    img_bits = np.array(bits[:shape_hidden[0]*shape_hidden[1]])
    img_oculta = (img_bits.reshape(shape_hidden) * 255).astype(np.uint8)
    return img_oculta

def comparar(img1, img2):
    diff = np.abs(img1.astype(int) - img2.astype(int))
    max_diff = np.max(diff)
    mean_diff = np.mean(diff)
    iguales = np.sum(img1 == img2)
    total = img1.size
    porcentaje = 100 * iguales / total
    return max_diff, mean_diff, porcentaje

# === MAIN ===
portadora = cargar_grises('imagen_portadora.png')  # a mayores pixeles, mejor queda la estego y más rep podemos agregar.  
oculta = cargar_grises('wp.png')        # 256x256

rep = 10 # Número de repeticiones para la codificación
estego, posiciones = ocultar_fft(portadora, oculta, rep=rep)

# Guardamos la imagen estego como .tiff para evitar compresión con pérdida
Image.fromarray(estego).save("imagen_estego.tiff", format='TIFF')

# Leemos la imagen estego desde disco (simulando una transmisión)
estego_cargada = cargar_grises("imagen_estego.tiff")

# Extraemos la imagen oculta desde la imagen leída
recuperada = extraer_fft(estego_cargada, oculta.shape, posiciones, rep=rep)

# === Estadísticas ===
print("=== Matriz Estego (vista 20x20) ===")
print(estego_cargada[:20, :20])
print("\n=== Matriz Recuperada (vista 20x20) ===")
print(recuperada[:20, :20])

print("\n=== Comparación Portadora vs Estego ===")
md, med, eq = comparar(portadora, estego_cargada)
print(f"Máxima diferencia absoluta: {md}")
print(f"Diferencia media: {med:.2f}")
print(f"Porcentaje de píxeles exactamente iguales: {eq:.2f}%")

print("\n=== Comparación Oculta original vs Recuperada ===")
md, med, eq = comparar(binarizar(oculta)*255, recuperada)
print(f"Máxima diferencia absoluta: {md}")
print(f"Diferencia media: {med:.2f}")
print(f"Porcentaje de píxeles exactamente iguales: {eq:.2f}%")

# === Visualización ===
fig, axs = plt.subplots(1, 4, figsize=(14, 4))
axs[0].imshow(portadora, cmap='gray'); axs[0].set_title("Portadora")
axs[1].imshow(estego_cargada, cmap='gray'); axs[1].set_title("Estego desde disco")
axs[2].imshow(oculta, cmap='gray'); axs[2].set_title("Oculta original")
axs[3].imshow(recuperada, cmap='gray'); axs[3].set_title("Recuperada")
for ax in axs: ax.axis('off')
plt.tight_layout()
plt.show()
