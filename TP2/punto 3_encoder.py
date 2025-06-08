import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def imagen_a_bits(img, delimitador="&"):
    img_bytes = img.tobytes() + delimitador.encode()
    bits = [int(b) for byte in img_bytes for b in format(byte, '08b')]
    return bits

def codificar_fft(img, bits, delta):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    real = fshift.real
    imag = fshift.imag

    altura, ancho = img.shape
    total_coef = altura * ancho
    if len(bits) > total_coef * 2:
        raise ValueError("Demasiados bits para codificar en esta imagen.")

    flat_real = real.flatten()
    flat_imag = imag.flatten()
    idx = 0

    for i in range(len(bits)):
        coef = flat_real if i % 2 == 0 else flat_imag
        val = coef[i // 2]
        signo = 1 if val >= 0 else -1
        q = abs(int(round(val / delta)))
        if (q % 2) != bits[i]:
            q += 1
        coef[i // 2] = signo * q * delta

    f_mod = np.fft.ifftshift(flat_real.reshape((altura, ancho)) + 1j * flat_imag.reshape((altura, ancho)))
    img_mod = np.fft.ifft2(f_mod).real
    img_mod = np.clip(img_mod, 0, 255).astype(np.uint8)
    return img_mod

def main():
    portadora = np.array(Image.open("memaso.png").convert("L"))
    oculta = np.array(Image.open("wp.png").resize((256, 256)).convert("L"))
    bits = imagen_a_bits(oculta)

    for delta in [1, 10, 100, 1000, 10000, 100000]:
        print(f"[Encoder] Procesando con delta = {delta}")
        estego = codificar_fft(portadora, bits, delta)
        Image.fromarray(estego).save(f"estego_delta{delta}.tiff")

        plt.imshow(estego, cmap="gray")
        plt.title(f"Imagen Estego (delta={delta})")
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    main()
