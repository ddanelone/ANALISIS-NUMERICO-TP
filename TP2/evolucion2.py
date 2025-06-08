import numpy as np
import cv2
import matplotlib.pyplot as plt

def embed_image(portadora, oculta):
    if oculta.shape[0] > portadora.shape[0] or oculta.shape[1] > portadora.shape[1]:
        oculta = cv2.resize(oculta, (portadora.shape[1], portadora.shape[0]))

    dft = np.fft.fft2(portadora).astype(np.complex64)
    dft_shift = np.fft.fftshift(dft)

    # Codificamos alto, ancho y la imagen
    h, w = oculta.shape
    shape_bytes = np.array([h, w], dtype=np.uint16).tobytes()
    eof_marker = b'\x00\x00\xFF\xFF'
    data_to_embed = shape_bytes + oculta.tobytes() + eof_marker
    data_bits = np.unpackbits(np.frombuffer(data_to_embed, dtype=np.uint8))

    rows, cols = dft_shift.shape
    bit_idx = 0
    for i in range(rows):
        for j in range(cols):
            if bit_idx >= len(data_bits):
                break
            bit = data_bits[bit_idx]
            dft_shift[i, j] = complex(
                abs(dft_shift[i, j].real) * (-1 if bit else 1),
                dft_shift[i, j].imag
            )
            bit_idx += 1
            if bit_idx < len(data_bits):
                bit = data_bits[bit_idx]
                dft_shift[i, j] = complex(
                    dft_shift[i, j].real,
                    abs(dft_shift[i, j].imag) * (-1 if bit else 1)
                )
                bit_idx += 1
        if bit_idx >= len(data_bits):
            break

    idft = np.fft.ifftshift(dft_shift)
    imagen_estego = np.abs(np.fft.ifft2(idft)).astype(np.uint8)
    return imagen_estego

def extract_image(imagen_estego):
    dft = np.fft.fft2(imagen_estego).astype(np.complex64)
    dft_shift = np.fft.fftshift(dft)

    extracted_bits = []
    rows, cols = dft_shift.shape
    for i in range(rows):
        for j in range(cols):
            bit_real = 1 if dft_shift[i, j].real < 0 else 0
            extracted_bits.append(bit_real)
            bit_imag = 1 if dft_shift[i, j].imag < 0 else 0
            extracted_bits.append(bit_imag)

    bytes_array = np.packbits(extracted_bits)
    # Buscar marcador EOF
    for i in range(0, len(bytes_array) - 3):
        if bytes_array[i:i+4].tobytes() == b'\x00\x00\xFF\xFF':
            contenido = bytes_array[:i]
            break
    else:
        raise ValueError("Marcador EOF no encontrado.")

    # Leer las primeras 4 bytes como alto y ancho
    if len(contenido) < 4:
        raise ValueError("No hay suficientes datos para recuperar dimensiones.")
    h = int.from_bytes(contenido[:2].tobytes(), 'little')
    w = int.from_bytes(contenido[2:4].tobytes(), 'little')
    datos_imagen = contenido[4:]
    if len(datos_imagen) < h * w:
        raise ValueError("Datos insuficientes para reconstruir la imagen.")
    oculta_recovered = np.frombuffer(datos_imagen[:h * w], dtype=np.uint8).reshape((h, w))
    return oculta_recovered

def main():
    print("Cargando imágenes...")
    portadora = cv2.imread('imagen_portadora.png', cv2.IMREAD_GRAYSCALE)
    oculta = cv2.imread('imagen_oculta.png', cv2.IMREAD_GRAYSCALE)

    if portadora is None or oculta is None:
        raise ValueError("¡Error al cargar las imágenes!")

    print("Ocultando imagen...")
    imagen_estego = embed_image(portadora, oculta)
    cv2.imwrite('imagen_estego.png', imagen_estego)
    print("Imagen estego guardada como 'imagen_estego.png'")

    print("Recuperando imagen oculta...")
    oculta_recovered = extract_image(imagen_estego)
    cv2.imwrite('imagen_recuperada.png', oculta_recovered)
    print("Imagen recuperada guardada como 'imagen_recuperada.png'")

    # Mostrar resultados
    plt.figure(figsize=(12, 4))
    plt.subplot(131), plt.imshow(portadora, cmap='gray'), plt.title('Portadora')
    plt.subplot(132), plt.imshow(imagen_estego, cmap='gray'), plt.title('Estego')
    plt.subplot(133), plt.imshow(oculta_recovered, cmap='gray'), plt.title('Recuperada')
    plt.show()

if __name__ == "__main__":
    main()
