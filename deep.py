import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, fftfreq
from scipy.signal import butter, filtfilt, welch
from scipy.integrate import trapezoid
import seaborn as sns

# Configuración general
sns.set(style="darkgrid")
fs = 173.61  # Frecuencia de muestreo en Hz

# Función para cargar los datos desde archivo
def cargar_senal(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        return np.array([float(line.strip()) for line in f if line.strip()])

# Cargar las tres señales
senales = [cargar_senal(f'Signal_{i}.txt') for i in range(1, 4)]
t = np.arange(len(senales[0])) / fs

# Función para graficar múltiples señales
def graficar_senales(senales, titulos, xlabel, ylabel, tiempo=None):
    plt.figure(figsize=(15, 8))
    for i, senal in enumerate(senales):
        plt.subplot(3, 1, i + 1)
        x = tiempo if tiempo is not None else np.arange(len(senal))
        plt.plot(x, senal)
        plt.title(titulos[i])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()

# 1. Visualización en el dominio del tiempo
graficar_senales(
    senales,
    [
        'Señal 1 - Registro crudo en el dominio del tiempo',
        'Señal 2 - Registro crudo en el dominio del tiempo',
        'Señal 3 - Registro crudo en el dominio del tiempo'
    ],
    'Tiempo [s]',
    'Amplitud [u.a.]',
    t
)

# 2. Filtro pasa bajos
def filtro_pasa_bajos(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

cutoff = 40.0  # Hz
senales_filtradas = [filtro_pasa_bajos(s, cutoff, fs) for s in senales]

# Visualización de señales filtradas solamente
plt.figure(figsize=(15, 8))
for i in range(3):
    plt.subplot(3, 1, i + 1)
    plt.plot(t, senales_filtradas[i], color='tab:blue', linewidth=1.2)
    plt.title(f'Señal {i + 1} Filtrada (Low-pass 40 Hz)')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud [u.a.]')
plt.tight_layout()
plt.show()


# 3. FFT
def calcular_fft(senal, fs):
    n = len(senal)
    yf = fft(senal)
    xf = fftfreq(n, 1/fs)[:n//2]
    return xf, 2.0/n * np.abs(yf[0:n//2])

ffts = [calcular_fft(s, fs) for s in senales_filtradas]

# Visualización de FFT
plt.figure(figsize=(15, 8))
for i, (xf, yf) in enumerate(ffts):
    plt.subplot(3, 1, i + 1)
    plt.plot(xf, yf)
    plt.title(f'Señal {i + 1} - Espectro de Frecuencia (FFT)')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Magnitud [u.a.]')
    plt.xlim(0, 50)
plt.tight_layout()
plt.show()

# 4. Potencia espectral (Welch)
def calcular_potencia_espectral(senal, fs):
    f, Pxx = welch(senal, fs, nperseg=1024)
    return f, Pxx

potencias = [calcular_potencia_espectral(s, fs) for s in senales_filtradas]

# Visualización de potencia espectral
plt.figure(figsize=(15, 8))
for i, (f, Pxx) in enumerate(potencias):
    plt.subplot(3, 1, i + 1)
    plt.semilogy(f, Pxx)
    plt.title(f'Señal {i + 1} - Densidad Espectral de Potencia (Método de Welch)')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Potencia [V²/Hz]')
    plt.xlim(0, 50)
plt.tight_layout()
plt.show()

# 5. Autocorrelación
def calcular_autocorrelacion(senal):
    autocorr = np.correlate(senal, senal, mode='full')
    autocorr = autocorr[len(autocorr)//2:] / np.max(autocorr)
    return autocorr

autocorrelaciones = [calcular_autocorrelacion(s) for s in senales_filtradas]
t_autocorr = np.arange(len(autocorrelaciones[0])) / fs

# Visualización de autocorrelación
plt.figure(figsize=(15, 8))
for i, ac in enumerate(autocorrelaciones):
    plt.subplot(3, 1, i + 1)
    plt.plot(t_autocorr, ac)
    plt.title(f'Señal {i + 1} - Función de Autocorrelación Normalizada')
    plt.xlabel('Retardo [s]')
    plt.ylabel('Correlación normalizada')
    plt.xlim(0, 2)
plt.tight_layout()
plt.show()

# 6. Análisis de bandas de frecuencia
def analizar_bandas(f, Pxx, nombre_senal):
    bandas = {
        'Delta (0.5-4 Hz)': (0.5, 4),
        'Theta (4-8 Hz)': (4, 8),
        'Alpha (8-13 Hz)': (8, 13),
        'Beta (13-30 Hz)': (13, 30),
        'Gamma (30-50 Hz)': (30, 50)
    }
    print(f"\n🔍 Análisis de bandas para {nombre_senal}:")
    total = trapezoid(Pxx, f)
    for nombre, (low, high) in bandas.items():
        mask = (f >= low) & (f <= high)
        potencia = trapezoid(Pxx[mask], f[mask])
        porcentaje = (potencia / total) * 100
        print(f"{nombre}: {potencia:.4f} ({porcentaje:.2f} % de la potencia total)")
        
# Recolectar potencias por banda para graficar
bandas = {
    'Delta (0.5-4 Hz)': (0.5, 4),
    'Theta (4-8 Hz)': (4, 8),
    'Alpha (8-13 Hz)': (8, 13),
    'Beta (13-30 Hz)': (13, 30),
    'Gamma (30-50 Hz)': (30, 50)
}

nombres_bandas = list(bandas.keys())
potencias_bandas = []

for f, Pxx in potencias:
    total = trapezoid(Pxx, f)
    potencias_por_senal = []
    for low, high in bandas.values():
        mask = (f >= low) & (f <= high)
        potencia = trapezoid(Pxx[mask], f[mask])
        porcentaje = (potencia / total) * 100
        potencias_por_senal.append(porcentaje)
    potencias_bandas.append(potencias_por_senal)

# Convertir a numpy array para graficar fácilmente
potencias_bandas = np.array(potencias_bandas)

# Crear gráfico de bastones
x = np.arange(len(nombres_bandas))  # etiquetas
width = 0.25  # ancho de las barras

plt.figure(figsize=(12, 6))
plt.bar(x - width, potencias_bandas[0], width, label='Señal 1')
plt.bar(x, potencias_bandas[1], width, label='Señal 2')
plt.bar(x + width, potencias_bandas[2], width, label='Señal 3')
plt.xticks(x, nombres_bandas)
plt.ylabel('Potencia relativa [%]')
plt.title('Distribución de Potencia por Bandas de Frecuencia')
plt.legend()
plt.tight_layout()
plt.show()


for i, (f, Pxx) in enumerate(potencias):
    analizar_bandas(f, Pxx, f"Señal {i + 1}")
