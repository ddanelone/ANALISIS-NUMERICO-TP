import numpy as np
import matplotlib.pyplot as plt

# Parámetros de muestreo
fs = 173.61  # Frecuencia de muestreo en Hz
fc = 40      # Frecuencia de corte en Hz

# Duración del filtro (en segundos), puede ajustarse
duracion_filtro = 1 / fc
tamano_filtro = int(fs * duracion_filtro)

# Ventana rectangular normalizada: promedio móvil
h = np.ones(tamano_filtro) / tamano_filtro

# Convolución (sin np.convolve)
def convolucion_discreta(x, h):
    N = len(x)
    M = len(h)
    y = np.zeros(N)
    for n in range(N):
        acc = 0.0
        for k in range(M):
            if n - k >= 0:
                acc += x[n - k] * h[k]
        y[n] = acc
    return y

# Función para cargar señal y aplicar filtrado
def procesar_y_graficar(nombre_archivo, titulo):
    x = np.loadtxt(nombre_archivo)
    t = np.arange(len(x)) / fs
    y = convolucion_discreta(x, h)

    plt.figure(figsize=(12, 5))
    plt.plot(t, x, label='Original', alpha=0.5, color='navy')
    plt.plot(t, y, label='Filtrada (convolución pasa bajos)', color='lightblue', linewidth=2)
    plt.title(titulo)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Procesar las 3 señales
procesar_y_graficar('Signal_1.txt', 'Signal 1: Señal original vs filtrada (convolución)')
procesar_y_graficar('Signal_2.txt', 'Signal 2: Señal original vs filtrada (convolución)')
procesar_y_graficar('Signal_3.txt', 'Signal 3: Señal original vs filtrada (convolución)')
