import numpy as np
import cv2

def extraer_texto(imagen_estego, delta=1):
    tf_mod = np.fft.fft2(imagen_estego)
    tf_flat = tf_mod.flatten()
    bits = []

    for z in tf_flat:
        a = z.real
        q = int(np.round(abs(a) / delta))
        bits.append(q % 2)

    bits = np.array(bits[: (len(bits) // 8) * 8])
    bytes_extraidos = np.packbits(bits)

    try:
        texto = bytes_extraidos.tobytes().decode('utf-8', errors='ignore')
        mensaje_final = texto.split('&')[0] + '&'
    except UnicodeDecodeError:
        mensaje_final = "[Error de decodificación]"

    return mensaje_final

if __name__ == "__main__":
    imagen_estego = cv2.imread("imagen_estego_preguntas.png", cv2.IMREAD_GRAYSCALE)
    if imagen_estego is None:
        print("ERROR: No se pudo cargar 'imagen_estego_preguntas.png'. Verifica que exista en el directorio.")
        exit(1)

    mensaje_extraido = extraer_texto(imagen_estego, delta=1)

    print("Mensaje extraído:", mensaje_extraido)
