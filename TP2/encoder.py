import numpy as np
import cv2

def ocultar_texto(portadora, mensaje, delta=1):
    tf = np.fft.fft2(portadora)
    tf_flat = tf.flatten()

    bits = np.unpackbits(np.frombuffer(mensaje.encode('utf-8'), dtype=np.uint8))

    for i, bit in enumerate(bits):
        a = tf_flat[i].real
        b = tf_flat[i].imag

        signo_a = 1 if a >= 0 else -1
        q_a = int(np.round(abs(a) / delta))
        if (q_a % 2) != bit:
            q_a += 1
        nuevo_real = signo_a * q_a * delta

        signo_b = 1 if b >= 0 else -1
        q_b = int(np.round(abs(b) / delta))
        if (q_b % 2) != bit:
            q_b += 1
        nuevo_imag = signo_b * q_b * delta

        tf_flat[i] = complex(nuevo_real, nuevo_imag)

    tf_mod = tf_flat.reshape(tf.shape)
    imagen_estego = np.fft.ifft2(tf_mod).real
    imagen_estego = np.clip(imagen_estego, 0, 255).astype(np.uint8)

    return imagen_estego

if __name__ == "__main__":
    portadora = cv2.imread("imagen_portadora.png", cv2.IMREAD_GRAYSCALE)
    if portadora is None:
        print("ERROR: No se pudo cargar 'imagen_portadora.png'. Verifica que exista en el directorio.")
        exit(1)

    mensaje = "¿Cuál es tu nombre?-¿Qué estudias?-¿En qué año estás?-¿Qué te gusta de la materia?-¿Cuál es tu grupo?&"

    imagen_estego = ocultar_texto(portadora, mensaje, delta=1)

    cv2.imwrite("imagen_estego_preguntas.png", imagen_estego)
    print("Mensaje ocultado y guardado en 'imagen_estego_preguntas.png'")
