import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image


def leer_gris(ruta):
    return np.asarray(Image.open(ruta).convert("L"))


def crear_mascara_alta_frecuencia(shape, radio_interno=50):
    h, w = shape
    cx, cy = w // 2, h // 2
    y, x = np.ogrid[:h, :w]
    dist = np.sqrt((x - cx)**2 + (y - cy)**2)
    return dist >= radio_interno


def int_a_bits16(n):
    return np.unpackbits(np.array([n], dtype=">u2").view(np.uint8))


def bits16_a_int(bits):
    bits = bits[:16]
    byte_array = np.packbits(bits)
    return int.from_bytes(byte_array, byteorder="big")


def ocultar(portadora, oculta, radio=50, salida="imagen_estego.png"):
    h, w = portadora.shape
    tf = np.fft.fft2(portadora)
    tf_shifted = np.fft.fftshift(tf)

    mask = crear_mascara_alta_frecuencia((h, w), radio)
    idxs = np.argwhere(mask)

    max_bits = len(idxs) * 2
    alto, ancho = oculta.shape

    header = np.concatenate([int_a_bits16(alto), int_a_bits16(ancho)])
    bits_data = np.unpackbits(oculta.flatten())
    total_bits = np.concatenate([header, bits_data])

    if len(total_bits) > max_bits:
        print("⚠️ Imagen oculta demasiado grande. Redimensionando.")
        max_pix = (max_bits - 32) // 8
        lado = int(np.floor(np.sqrt(max_pix)))
        oculta = cv2.resize(oculta, (lado, lado), interpolation=cv2.INTER_AREA)
        alto, ancho = oculta.shape
        header = np.concatenate([int_a_bits16(alto), int_a_bits16(ancho)])
        bits_data = np.unpackbits(oculta.flatten())
        total_bits = np.concatenate([header, bits_data])

    print(f"[INFO] Bits ocultados: {len(total_bits)}")
    print(f"[INFO] Imagen oculta: {alto}x{ancho}")

    real = np.real(tf_shifted)
    imag = np.imag(tf_shifted)

    for i, (y, x) in enumerate(idxs[:len(total_bits) // 2]):
        bit_r = total_bits[2 * i]
        bit_i = total_bits[2 * i + 1]
        real[y, x] = abs(real[y, x]) * (-1 if bit_r else 1)
        imag[y, x] = abs(imag[y, x]) * (-1 if bit_i else 1)

    tf_mod = np.fft.ifftshift(real + 1j * imag)
    img_mod = np.fft.ifft2(tf_mod)
    img_mod = np.abs(img_mod)
    img_mod = np.clip(img_mod, 0, 255).astype(np.uint8)

    Image.fromarray(img_mod).save(salida)
    print(f"[INFO] Imagen estego guardada como {salida}")


def extraer(ruta_estego, radio=50):
    img = np.asarray(Image.open(ruta_estego).convert("L"))
    h, w = img.shape
    tf = np.fft.fft2(img)
    tf_shifted = np.fft.fftshift(tf)

    mask = crear_mascara_alta_frecuencia((h, w), radio)
    idxs = np.argwhere(mask)

    bits = []
    for (y, x) in idxs:
        bits.append(0 if tf_shifted[y, x].real >= 0 else 1)
        bits.append(0 if tf_shifted[y, x].imag >= 0 else 1)

    bits = np.array(bits, dtype=np.uint8)

    if len(bits) < 32:
        print("❌ Encabezado insuficiente.")
        return np.zeros((10, 10), dtype=np.uint8)

    alto = bits16_a_int(bits[:16])
    ancho = bits16_a_int(bits[16:32])
    bits_esperados = alto * ancho * 8

    print(f"[INFO] Bits extraídos: {len(bits)}")
    print(f"[INFO] Dimensiones recuperadas: {alto}x{ancho}")
    print(f"[INFO] Bits necesarios: {bits_esperados}")

    if len(bits[32:]) < bits_esperados:
        print("⚠️ Datos incompletos. Recuperación parcial.")
        bits_extra = np.zeros(bits_esperados, dtype=np.uint8)
        bits_extra[:len(bits[32:])] = bits[32:]
        datos = bits_extra
    else:
        datos = bits[32:32 + bits_esperados]

    try:
        img_oculta = np.packbits(datos).reshape((alto, ancho))
    except Exception as e:
        print(f"❌ Error al reconstruir la imagen: {e}")
        return np.zeros((10, 10), dtype=np.uint8)

    return img_oculta


if __name__ == "__main__":
    # Leer imágenes
    portadora = leer_gris("memaso.png")
    oculta = leer_gris("wp.png")

    # Ocultamiento
    ocultar(portadora, oculta, radio=50, salida="imagen_estego.png")

    # Recuperación desde disco
    recuperada = extraer("imagen_estego.png", radio=50)

    # Guardar imagen recuperada
    Image.fromarray(recuperada).save("imagen_recuperada.png")

    # Mostrar resultados
    estego = leer_gris("imagen_estego.png")

    plt.figure(figsize=(10, 8))

    plt.subplot(2, 2, 1)
    plt.title("Imagen Portadora")
    plt.imshow(portadora, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.title("Imagen Estego")
    plt.imshow(estego, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.title("Imagen Oculta Original")
    plt.imshow(oculta, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.title("Imagen Oculta Recuperada")
    plt.imshow(recuperada, cmap='gray')
    plt.axis('off')

    plt.tight_layout()
    plt.show()
