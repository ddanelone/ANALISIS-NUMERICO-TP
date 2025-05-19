import numpy as np
import matplotlib.pyplot as plt
import math
import time  

# DFT manual
def dft_manual(x):
    N = len(x)
    X = []
    for k in range(N):
        real = 0.0
        imag = 0.0
        for n in range(N):
            angle = 2 * math.pi * k * n / N
            real += x[n] * math.cos(-angle)
            imag += x[n] * math.sin(-angle)
        X.append(complex(real, imag))
    return X

# Frecuencia de muestreo
fs = 173.61

# Función para graficar la magnitud de la DFT
def graficar_dft(nombre_archivo, titulo):
    print(f"\nProcesando {titulo}...")
    inicio = time.time()  # Comenzar tiempo

    x = np.loadtxt(nombre_archivo)
    X = dft_manual(x)
    N = len(X)
    freqs = [fs * k / N for k in range(N)]
    magnitudes = [abs(Xk) for Xk in X]

    fin = time.time()  # Finalizar tiempo
    duracion = fin - inicio
    print(f"Tiempo de procesamiento para {titulo}: {duracion:.2f} segundos")

    # Graficamos solo hasta la mitad (frecuencias positivas)
    mitad = N // 2
    plt.figure(figsize=(12, 5))
    plt.plot(freqs[:mitad], magnitudes[:mitad])
    plt.title(f"Espectro de {titulo} (DFT manual)")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Magnitud")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Aplicar a cada señal
graficar_dft("Signal_1.txt", "Signal 1")
graficar_dft("Signal_2.txt", "Signal 2")
graficar_dft("Signal_3.txt", "Signal 3")
