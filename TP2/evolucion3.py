import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm

def imagen_a_bits(imagen):
    """Convierte imagen a cadena de bits (8 bits por píxel)"""
    datos = np.array(imagen).flatten()
    bits = ''.join([format(pixel, '08b') for pixel in datos])
    return bits, imagen.size

def bits_a_imagen(bits, size):
    """Reconstruye imagen desde cadena de bits"""
    pixels = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)]
    array = np.array(pixels, dtype=np.uint8).reshape(size[::-1])
    return Image.fromarray(array)

def calcular_capacidad_maxima(portadora_path):
    """Calcula y muestra la capacidad máxima de ocultación"""
    portadora = Image.open(portadora_path)
    width, height = portadora.size
    
    # Cálculo teórico
    total_coef = width * height
    coef_utilizables = (total_coef - 1) // 2  # -1 por DC, //2 por simetría
    max_bits = coef_utilizables * 2           # 2 bits por coeficiente (real+imag)
    max_pixels = max_bits // 8                # 8 bits por píxel
    
    # Considerando que necesitamos almacenar también el tamaño (4 bytes = 32 bits)
    max_pixels_util = (max_bits - 32) // 8
    
    print("\n=== CÁLCULO DE CAPACIDAD ===")
    print(f"Dimensión imagen portadora: {width} x {height} = {width*height} píxeles")
    print(f"Coeficientes TF2D totales: {total_coef}")
    print(f"Coeficientes utilizables (considerando simetría): {coef_utilizables}")
    print(f"Bits almacenables (2 por coeficiente): {max_bits} bits")
    print(f"Píxeles máximos ocultables (8 bits/píxel): {max_pixels}")
    print(f"Píxeles útiles (reservando 32 bits para tamaño): {max_pixels_util}")
    print(f"Tamaño máximo imagen oculta: {int(np.sqrt(max_pixels_util))} x {int(np.sqrt(max_pixels_util))} (aprox)")
    
    return max_pixels_util

def codificar_con_fourier(portadora_path, oculta_path, salida_path):
    """Oculta imagen en otra modificando signos de la TF2D"""
    # Calcular capacidad primero
    max_pixels = calcular_capacidad_maxima(portadora_path)
    
    # Cargar imágenes
    portadora = Image.open(portadora_path).convert('L')
    oculta = Image.open(oculta_path).convert('L')
    
    # Verificar tamaño
    oculta_pixels = oculta.size[0] * oculta.size[1]
    if oculta_pixels > max_pixels:
        raise ValueError(f"Imagen oculta demasiado grande. Máx: {max_pixels} píxeles ({int(np.sqrt(max_pixels))}x{int(np.sqrt(max_pixels))} aprox)")
    
    # Resto del código de codificación...
    # ... [el mismo código de codificación que antes]
    """
    Oculta imagen en otra modificando signos de la TF2D
    """
    # Cargar imágenes
    portadora = Image.open(portadora_path).convert('L')
    oculta = Image.open(oculta_path).convert('L')
    
    # Convertir imagen oculta a bits
    bits_ocultos, size_oculta = imagen_a_bits(oculta)
    portadora_array = np.array(portadora, dtype=np.float32)
    
    # Calcular TF2D
    tf = np.fft.fft2(portadora_array)
    tf_shifted = np.fft.fftshift(tf)
    
    # Obtener dimensiones
    filas, cols = tf_shifted.shape
    total_coef = filas * cols
    necesarios = len(bits_ocultos) // 2
    
    if necesarios > total_coef:
        raise ValueError(f"Imagen oculta demasiado grande. Máx: {total_coef*2//8} bytes")
    
    # Codificar bits en los coeficientes
    bit_idx = 0
    for f in tqdm(range(filas), desc="Codificando"):
        for c in range(cols):
            if bit_idx >= len(bits_ocultos):
                break
                
            coef = tf_shifted[f, c]
            real = np.abs(coef.real)
            imag = np.abs(coef.imag)
            
            # Modificar signos según bits
            if bit_idx < len(bits_ocultos):
                real = real if bits_ocultos[bit_idx] == '0' else -real
                bit_idx += 1
            if bit_idx < len(bits_ocultos):
                imag = imag if bits_ocultos[bit_idx] == '0' else -imag
                bit_idx += 1
                
            tf_shifted[f, c] = complex(real, imag)
    
    # Transformada inversa
    tf_modificada = np.fft.ifftshift(tf_shifted)
    imagen_estego = np.fft.ifft2(tf_modificada)
    imagen_estego = np.clip(np.real(imagen_estego), 0, 255).astype(np.uint8)
    
    # Guardar y mostrar resultados
    Image.fromarray(imagen_estego).save(salida_path)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.imshow(portadora, cmap='gray')
    plt.title('Portadora Original')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(oculta, cmap='gray')
    plt.title('Imagen Oculta')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(imagen_estego, cmap='gray')
    plt.title('Imagen Estego')
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    return size_oculta

def decodificar_con_fourier(estego_path, size_oculta):
    """Recupera imagen oculta leyendo signos de coeficientes TF2D"""
    estego = Image.open(estego_path).convert('L')
    estego_array = np.array(estego, dtype=np.float32)
    
    # Calcular TF2D
    tf = np.fft.fft2(estego_array)
    tf_shifted = np.fft.fftshift(tf)
    
    # Obtener dimensiones
    filas, cols = tf_shifted.shape
    cantidad_bits = size_oculta[0] * size_oculta[1] * 8
    bits = []
    
    # Decodificar bits desde los coeficientes
    for f in tqdm(range(filas), desc="Decodificando"):
        for c in range(cols):
            if len(bits) >= cantidad_bits:
                break
                
            coef = tf_shifted[f, c]
            bits.append('1' if coef.real < 0 else '0')
            if len(bits) < cantidad_bits:
                bits.append('1' if coef.imag < 0 else '0')
    
    # Reconstruir imagen
    bits = ''.join(bits[:cantidad_bits])
    return bits_a_imagen(bits, size_oculta)

# --- BLOQUE PRINCIPAL ---
if __name__ == "__main__":
    imagen_portadora = "imagen_portadora.png"
    imagen_oculta = "imagen_oculta.png"
    imagen_estego = "imagen_estego_fourier.png"
    
    try:
        print("=== Codificación ===")
        size_oculta = codificar_con_fourier(imagen_portadora, imagen_oculta, imagen_estego)
        
        print("\n=== Decodificación ===")
        imagen_recuperada = decodificar_con_fourier(imagen_estego, size_oculta)
        
        # Mostrar resultados
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.imshow(Image.open(imagen_oculta), cmap='gray')
        plt.title("Imagen Oculta Original")
        plt.axis('off')
        
        plt.subplot(1, 2, 2)
        plt.imshow(imagen_recuperada, cmap='gray')
        plt.title("Imagen Recuperada")
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Error: {str(e)}")