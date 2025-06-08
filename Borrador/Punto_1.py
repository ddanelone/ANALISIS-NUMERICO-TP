from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def mensaje_a_binario(mensaje):
    mensaje += "&"  # Marcador de fin
    return ''.join([format(ord(c), '08b') for c in mensaje])

def binario_a_mensaje(bin_str):
    chars = [bin_str[i:i+8] for i in range(0, len(bin_str), 8)]
    mensaje = ''
    for byte in chars:
        char = chr(int(byte, 2))
        if char == '&':
            break
        mensaje += char
    return mensaje

def ocultar_mensaje(imagen_path, mensaje, salida_path):
    try:
        imagen = Image.open(imagen_path).convert('L')  # Escala de grises
        datos = np.array(imagen).flatten()
        bin_mensaje = mensaje_a_binario(mensaje)
        
        if len(bin_mensaje) > len(datos):
            max_chars = len(datos) // 8  # Cada carácter necesita 8 bits
            raise ValueError(f"El mensaje es muy largo para esta imagen. Máximo: {max_chars} caracteres")
        
        for i, bit in enumerate(bin_mensaje):
            datos[i] = (datos[i] & 0b11111110) | int(bit)

        nueva_imagen = Image.fromarray(np.reshape(datos, imagen.size[::-1]).astype(np.uint8))
        nueva_imagen.save(salida_path)
        print(f"Mensaje ocultado y guardado en {salida_path}")
        
        # Mostrar comparación de imágenes
        plt.figure(figsize=(10, 5))
        plt.suptitle("Comparación de imágenes", fontsize=14)

        plt.subplot(1, 2, 1)
        plt.imshow(imagen, cmap='gray')
        plt.title('Imagen Original')
        plt.axis('off')
        
        plt.subplot(1, 2, 2)
        plt.imshow(nueva_imagen, cmap='gray')
        plt.title('Imagen con Mensaje Oculto')
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        return nueva_imagen
        
    except Exception as e:
        print(f"Error al ocultar mensaje: {str(e)}")
        return None

def extraer_mensaje(imagen_path):
    try:
        imagen = Image.open(imagen_path).convert('L')
        datos = np.array(imagen).flatten()
        bits = ''.join([str(pixel & 1) for pixel in datos])
        return binario_a_mensaje(bits)
    except Exception as e:
        print(f"Error al extraer mensaje: {str(e)}")
        return None

# === MAIN ===
if __name__ == "__main__":
    imagen_original = "imagen_portadora.jpg"
    imagen_estego = "imagen_estego.png"
    mensaje = "Hola, Análisis Numérico 2025"
    
    imagen = Image.open(imagen_original).convert('L')
    capacidad = (imagen.size[0] * imagen.size[1]) // 8
    print(f"\nInformación de la imagen: {imagen.size[0]}x{imagen.size[1]} píxeles")
    print(f"Capacidad máxima de mensaje: {capacidad} caracteres")
    print(f"Longitud del mensaje actual: {len(mensaje)} caracteres\n")
    
    print(f"Ocultando mensaje: '{mensaje}'")
    imagen_modificada = ocultar_mensaje(imagen_original, mensaje, imagen_estego)
    
    if imagen_modificada:
        mensaje_recuperado = extraer_mensaje(imagen_estego)
        print("\nMensaje recuperado:", mensaje_recuperado)
        
        # Verificación
        if mensaje == mensaje_recuperado:
            print("¡El mensaje se recuperó correctamente!")
        else:
            print("Hubo un error en la recuperación del mensaje")

        # Mostrar ventana con los mensajes
        plt.figure(figsize=(10, 3))
        plt.suptitle("Comparación de mensajes", fontsize=14)
        plt.text(0.05, 0.6, f"Mensaje original:\n{mensaje}", fontsize=12, wrap=True)
        plt.text(0.55, 0.6, f"Mensaje recuperado:\n{mensaje_recuperado}", fontsize=12, wrap=True)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
