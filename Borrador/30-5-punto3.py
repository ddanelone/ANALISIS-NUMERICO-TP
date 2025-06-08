import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Parámetros
DELTA = 1
REPETICIONES = 7
ZONA_EXCLUSION = 256  # Centro 256x256 a evitar
STEGO_FILENAME = 'imagen_estego3.tiff'

def cargar_imagen_grayscale(path, size=None):
    img = Image.open(path).convert('L')
    if size:
        img = img.resize(size)
    return np.array(img, dtype=np.uint8)

def obtener_matriz_bits(imagen):
    bits = np.unpackbits(imagen.flatten())
    return np.repeat(bits, REPETICIONES)

def reconstruir_imagen_bits(bits, forma):
    bits = bits.reshape(-1, REPETICIONES)
    votos = np.round(np.mean(bits, axis=1)).astype(np.uint8)
    votos = votos[:(votos.size // 8) * 8]  # Aseguramos múltiplo de 8
    bytes_recuperados = np.packbits(votos)
    return bytes_recuperados.reshape(forma)


def generar_coordenadas_validas(shape, excl):
    h, w = shape
    coords = []
    for i in range(h):
        for j in range(w):
            if (excl <= i < h - excl) and (excl <= j < w - excl):
                continue  # está en la zona central
            coords.append((i, j))
    return coords

def ajustar_valor(val, bit, delta):
    if val == 0:
        x = 1
    else:
        x = 1 if val > 0 else 0
    q = int(round(abs(val) / delta))
    # Ajustar paridad según bit
    if (q % 2) != bit:
        q += 1
    return x * q * delta

def codificar(memoria, mensaje_bits, delta=1):
    fft = np.fft.fft2(memoria.astype(np.float64))
    fft = np.fft.fftshift(fft)
    coords = generar_coordenadas_validas(fft.shape, ZONA_EXCLUSION)

    if len(mensaje_bits) > len(coords):
        raise ValueError("No hay suficientes coordenadas para ocultar el mensaje")

    for idx, bit in enumerate(mensaje_bits):
        i, j = coords[idx]
        real = fft[i, j].real
        imag = fft[i, j].imag
        new_real = ajustar_valor(real, bit, delta)
        fft[i, j] = complex(new_real, imag)

    fft = np.fft.ifftshift(fft)
    img_estego = np.fft.ifft2(fft).real
    img_estego = np.clip(img_estego, 0, 255).astype(np.uint8)
    return img_estego

def decodificar(imagen_estego, delta=1):
    fft = np.fft.fft2(imagen_estego.astype(np.float64))
    fft = np.fft.fftshift(fft)
    coords = generar_coordenadas_validas(fft.shape, ZONA_EXCLUSION)

    bits = []
    for i, j in coords[:128*128*REPETICIONES]:
        real = fft[i, j].real
        q = int(round(abs(real) / delta))
        bits.append(q % 2)

    imagen_recuperada = reconstruir_imagen_bits(np.array(bits, dtype=np.uint8), (128, 128))
    return imagen_recuperada

def main():
    # Cargar imágenes
    imagen_portadora = cargar_imagen_grayscale('globo.png')
    imagen_oculta = cargar_imagen_grayscale('wp - copia.png')

    # Obtener bits del mensaje
    bits_mensaje = obtener_matriz_bits(imagen_oculta)

    # Codificar
    imagen_estego = codificar(imagen_portadora, bits_mensaje, delta=DELTA)

    # Guardar imagen TIFF sin pérdida
    Image.fromarray(imagen_estego).save(STEGO_FILENAME, format='TIFF')

    # Recuperar desde archivo
    imagen_estego_leida = cargar_imagen_grayscale(STEGO_FILENAME)
    imagen_recuperada = decodificar(imagen_estego_leida, delta=DELTA)

    # Mostrar resultados
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    axs[0, 0].imshow(imagen_portadora, cmap='gray')
    axs[0, 0].set_title('Imagen original')
    axs[0, 1].imshow(imagen_estego, cmap='gray')
    axs[0, 1].set_title('Imagen con mensaje oculto')
    axs[1, 0].imshow(imagen_oculta, cmap='gray')
    axs[1, 0].set_title('Imagen a ocultar')
    axs[1, 1].imshow(imagen_recuperada, cmap='gray')
    axs[1, 1].set_title('Imagen recuperada')
    for ax in axs.flatten():
        ax.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
