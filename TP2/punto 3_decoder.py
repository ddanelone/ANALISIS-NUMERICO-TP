import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def extraer_bits_fft(img, num_bits, delta):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    real = fshift.real.flatten()
    imag = fshift.imag.flatten()

    bits = []
    for i in range(num_bits):
        coef = real if i % 2 == 0 else imag
        val = coef[i // 2]
        q = abs(int(round(val / delta)))
        bits.append(q % 2)
    return bits

def bits_a_imagen(bits, alto, ancho, delimitador="&"):
    bytes_recuperados = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        b = int("".join(str(bit) for bit in byte), 2)
        bytes_recuperados.append(b)
        if bytes(bytes_recuperados[-len(delimitador):]) == delimitador.encode():
            bytes_recuperados = bytes_recuperados[:-len(delimitador)]
            break

    if len(bytes_recuperados) < alto * ancho:
        print("⚠️ Imagen recuperada incompleta, se completará con ceros.")
        bytes_recuperados += [0] * (alto * ancho - len(bytes_recuperados))
    elif len(bytes_recuperados) > alto * ancho:
        print("⚠️ Imagen recuperada excede el tamaño, se truncará.")
        bytes_recuperados = bytes_recuperados[:alto * ancho]

    return np.array(bytes_recuperados, dtype=np.uint8).reshape((alto, ancho))

def main():
    alto, ancho = 256, 256
    for delta in [1, 10, 100, 1000, 10000, 100000]:
        print(f"[Decoder] Procesando estego_delta{delta}.tiff con delta = {delta}")
        estego = np.array(Image.open(f"estego_delta{delta}.tiff").convert("L"))
        num_bits_estimado = estego.size * 2  # real + imag

        bits = extraer_bits_fft(estego, num_bits_estimado, delta)
        img_recuperada = bits_a_imagen(bits, alto, ancho)

        plt.imshow(img_recuperada, cmap="gray")
        plt.title(f"Imagen Recuperada (delta={delta})")
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    main()
