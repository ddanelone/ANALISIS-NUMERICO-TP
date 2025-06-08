import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def imagen_a_bits(img_binaria):
    bits = np.unpackbits(img_binaria.flatten())
    bits_delimitador = np.unpackbits(np.array([38], dtype=np.uint8))  # ASCII '&'
    return np.concatenate([bits, bits_delimitador])

def ocultar_bits_fft_signo(img_portadora, bits):
    fft = np.fft.fft2(img_portadora)
    fft_shifted = np.fft.fftshift(fft)
    flat_fft = fft_shifted.flatten()

    if len(bits) > len(flat_fft):
        raise ValueError("No hay suficientes coeficientes FFT para ocultar la imagen.")

    for i, bit in enumerate(bits):
        real = flat_fft[i].real
        imag = flat_fft[i].imag
        if bit == 1:
            real = -abs(real)
            imag = -abs(imag)
        else:
            real = abs(real)
            imag = abs(imag)
        flat_fft[i] = complex(real, imag)

    fft_mod = flat_fft.reshape(fft_shifted.shape)
    imagen_estego = np.fft.ifft2(np.fft.ifftshift(fft_mod))
    return np.clip(np.real(imagen_estego), 0, 255).astype(np.uint8)

def main():
    portadora_path = "memaso.png"
    oculta_path = "wp.png"
    salida_path = "imagen_estego.npy"

    img_portadora = Image.open(portadora_path).convert('L')
    datos_portadora = np.array(img_portadora)

    img_oculta = Image.open(oculta_path).convert('L')
    datos_oculta = (np.array(img_oculta) > 128).astype(np.uint8) * 255

    bits_oculta = imagen_a_bits(datos_oculta)
    print(f"[Encoder] Bits a ocultar: {len(bits_oculta)}")

    estego = ocultar_bits_fft_signo(datos_portadora, bits_oculta)

    np.save(salida_path, estego)
    print(f"[Encoder] Imagen estego guardada en {salida_path}")

    # Visualización
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title("Portadora Original")
    plt.imshow(datos_portadora, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title("Imagen Estego")
    plt.imshow(estego, cmap='gray')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
