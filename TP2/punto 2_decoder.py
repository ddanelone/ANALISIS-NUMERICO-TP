import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def extraer_bits_fft_signo(img_estego, cantidad_bits):
    fft = np.fft.fft2(img_estego)
    fft_shifted = np.fft.fftshift(fft)
    flat_fft = fft_shifted.flatten()

    bits = []
    for i in range(min(cantidad_bits, len(flat_fft))):
        real = flat_fft[i].real
        imag = flat_fft[i].imag
        bit = 1 if real < 0 or imag < 0 else 0
        bits.append(bit)
    return np.array(bits, dtype=np.uint8)

def bits_a_imagen(bits, alto, ancho):
    bits = bits[:len(bits) - (len(bits) % 8)]
    bytes_img = np.packbits(bits)
    if bytes_img.size < alto * ancho:
        bytes_img = np.concatenate([bytes_img, np.zeros(alto*ancho - bytes_img.size, dtype=np.uint8)])
        print("⚠️ Imagen recuperada incompleta, se completará con ceros.")
    bytes_img = bytes_img[:alto*ancho]
    img = bytes_img.reshape((alto, ancho))
    return (img > 128).astype(np.uint8) * 255

def main():
    estego_path = "imagen_estego.npy"
    oculta_original_path = "wp.png"

    estego = np.load(estego_path)
    print(f"[Decoder] Imagen estego cargada. Tamaño: {estego.shape}")

    img_oculta_original = Image.open(oculta_original_path).convert('L')
    alto, ancho = img_oculta_original.size[1], img_oculta_original.size[0]

    total_bits = alto * ancho * 8 + 8
    bits_extraidos = extraer_bits_fft_signo(estego, total_bits)

    delim = [0, 0, 1, 0, 0, 1, 1, 0]  # ASCII '&'
    bits_bytes = np.split(bits_extraidos, len(bits_extraidos) // 8)
    mensaje_bits = []
    for b in bits_bytes:
        mensaje_bits.extend(b)
        if np.array_equal(b, delim):
            break

    mensaje_bits = np.array(mensaje_bits[:-8], dtype=np.uint8)
    oculta_recuperada = bits_a_imagen(mensaje_bits, alto, ancho)

    # Visualización
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.title("Imagen Oculta Original")
    plt.imshow(np.array(img_oculta_original), cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title("Imagen Recuperada")
    plt.imshow(oculta_recuperada, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title("Imagen Estego")
    plt.imshow(estego, cmap='gray')
    plt.axis('off')
    plt.show()

    print("✅ Decodificación finalizada.")

if __name__ == "__main__":
    main()
