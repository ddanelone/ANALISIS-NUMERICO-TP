import numpy as np
import cv2

def ocultar_texto(portadora, mensaje, delta=1):
    tf = np.fft.fft2(portadora)
    tf_flat = tf.flatten()

    # Codificar mensaje a UTF-8 y obtener bits
    bits = np.unpackbits(np.frombuffer(mensaje.encode('utf-8'), dtype=np.uint8))

    for i, bit in enumerate(bits):
        a = tf_flat[i].real
        b = tf_flat[i].imag

        # Parte real
        signo_a = 1 if a >= 0 else -1
        q_a = int(np.round(abs(a) / delta))
        if (q_a % 2) != bit:
            q_a += 1
        nuevo_real = signo_a * q_a * delta

        # Parte imaginaria (se modifica igual que la real, aunque no se use en extracción)
        signo_b = 1 if b >= 0 else -1
        q_b = int(np.round(abs(b) / delta))
        if (q_b % 2) != bit:
            q_b += 1
        nuevo_imag = signo_b * q_b * delta

        tf_flat[i] = complex(nuevo_real, nuevo_imag)

    tf_mod = tf_flat.reshape(tf.shape)
    imagen_estego = np.fft.ifft2(tf_mod).real
    imagen_estego = np.clip(imagen_estego, 0, 255).astype(np.uint8)
    return imagen_estego, tf_mod

def extraer_texto(tf_mod, delta=1):
    tf_flat = tf_mod.flatten()
    bits = []

    for z in tf_flat:
        a = z.real
        q = int(np.round(abs(a) / delta))
        bits.append(q % 2)

    # Agrupar en bytes
    bits = np.array(bits[: (len(bits) // 8) * 8])
    bytes_extraidos = np.packbits(bits)

    try:
        texto = bytes_extraidos.tobytes().decode('utf-8', errors='ignore')
        mensaje_final = texto.split('&')[0] + '&'
    except UnicodeDecodeError:
        mensaje_final = "[Error de decodificación]"

    return mensaje_final

# === MAIN ===

# Cargar portadora
portadora = cv2.imread("imagen_portadora.png", cv2.IMREAD_GRAYSCALE)

# Mensaje a ocultar
mensaje = "¿Cuál es tu nombre?-¿Qué estudias?-¿En qué año estás?-¿Qué te gusta de la materia?-¿Cuál es tu grupo?&"

# Ocultar mensaje
imagen_estego, tf_mod = ocultar_texto(portadora, mensaje, delta=1)

# Guardar imagen estego si lo necesitás (opcional)
# cv2.imwrite("imagen_estego_preguntas.png", imagen_estego)

# Extraer mensaje
mensaje_extraido = extraer_texto(tf_mod, delta=1)

# Mostrar resultado
print("Mensaje extraído:", mensaje_extraido)
