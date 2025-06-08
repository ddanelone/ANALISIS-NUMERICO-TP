import numpy as np
import cv2
from numpy.fft import fft2, ifft2
from PIL import Image

# Funciones auxiliares
def imagen_a_bits(imagen):
    plano = imagen.flatten()
    bits = ''.join([format(pix, '08b') for pix in plano])
    bits += format(ord('&'), '08b')  # delimitador
    return list(bits)

def bits_a_imagen(bits):
    bytes_img = []
    for i in range(0, len(bits), 8):
        byte = ''.join(bits[i:i + 8])
        if byte == format(ord('&'), '08b'):
            break
        bytes_img.append(int(byte, 2))
    arr = np.array(bytes_img, dtype=np.uint8)
    return arr

def modificar_signo_por_bit(valor, bit):
    if bit == '0':
        return np.abs(valor)
    else:
        return -np.abs(valor)

def ocultar_bits_en_tf2d(tf2d, bits):
    tf2d_mod = np.copy(tf2d)
    h, w = tf2d.shape
    idx = 0
    for i in range(h):
        for j in range(w):
            if idx >= len(bits):
                return tf2d_mod
            real = tf2d_mod[i, j].real
            imag = tf2d_mod[i, j].imag
            real = modificar_signo_por_bit(real, bits[idx])
            idx += 1
            if idx >= len(bits):
                imag = tf2d_mod[i, j].imag  # no modificar si no hay más bits
            else:
                imag = modificar_signo_por_bit(imag, bits[idx])
                idx += 1
            tf2d_mod[i, j] = complex(real, imag)
    return tf2d_mod

def extraer_bits_de_tf2d(tf2d):
    bits = []
    h, w = tf2d.shape
    for i in range(h):
        for j in range(w):
            real = tf2d[i, j].real
            imag = tf2d[i, j].imag
            bits.append('0' if real >= 0 else '1')
            bits.append('0' if imag >= 0 else '1')
            if len(bits) >= 8:
                ultimo_byte = ''.join(bits[-8:])
                if ultimo_byte == format(ord('&'), '08b'):
                    return bits
    return bits

# Función principal
def main():
    print("Leyendo imagen portadora...")
    portadora = cv2.imread("imagen_portadora.png", cv2.IMREAD_GRAYSCALE)
    print("Leyendo imagen a ocultar...")
    oculta = cv2.imread("imagen_oculta.png", cv2.IMREAD_GRAYSCALE)

    if portadora is None or oculta is None:
        print("ERROR: No se pudo leer una o ambas imágenes.")
        return

    if len(portadora.shape) != 2 or len(oculta.shape) != 2:
        print("ERROR: Ambas imágenes deben ser en escala de grises.")
        return

    print("Aplicando TF2D a imagen portadora...")
    tf2d = fft2(portadora)

    print("Codificando imagen oculta...")
    bits = imagen_a_bits(oculta)
    print(f"Cantidad total de bits a ocultar (incluyendo delimitador): {len(bits)}")

    capacidad = portadora.shape[0] * portadora.shape[1] * 2
    if len(bits) > capacidad:
        print("ERROR: La imagen portadora no tiene suficiente capacidad.")
        return

    print("Modificando signos en dominio de frecuencia...")
    tf2d_mod = ocultar_bits_en_tf2d(tf2d, bits)

    print("Aplicando transformada inversa para generar imagen estego...")
    estego = np.real(ifft2(tf2d_mod))
    estego = np.clip(estego, 0, 255).astype(np.uint8)

    print("Guardando imagen estego como 'imagen_estego.png'...")
    Image.fromarray(estego).save("imagen_estego.png")

    print("Leyendo imagen estego desde disco...")
    estego_leida = cv2.imread("imagen_estego.png", cv2.IMREAD_GRAYSCALE)

    print("Aplicando TF2D para recuperar datos...")
    tf2d_leida = fft2(estego_leida)

    print("Extrayendo bits de la transformada...")
    bits_extraidos = extraer_bits_de_tf2d(tf2d_leida)

    print("Reconstruyendo imagen oculta...")
    imagen_recuperada_arr = bits_a_imagen(bits_extraidos)

    lado = int(np.sqrt(len(imagen_recuperada_arr)))
    if lado * lado > len(imagen_recuperada_arr):
        lado -= 1
    imagen_recuperada = np.reshape(imagen_recuperada_arr[:lado * lado], (lado, lado))

    print("Guardando imagen recuperada como 'imagen_recuperada.png'...")
    Image.fromarray(imagen_recuperada).save("imagen_recuperada.png")
    print("Proceso completado con éxito.")

if __name__ == "__main__":
    main()
