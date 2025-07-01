import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

# Constantes CO2
R = 0.08314  # L·bar/mol·K
T = 300      # K
a = 3.592    # L²·bar/mol²
b = 0.04267  # L/mol

# Presión (bar)
P = 50



# Función Van der Waals
def f(V):
    return (P + a / V**2) * (V - b) - R * T

# Buscar intervalo para la raíz (típico para gases reales)
V_min, V_max = 0.05, 1.0

# Calcular raíz con método Brent
raiz = brentq(f, V_min, V_max)

# Valores para graficar
V_vals = np.linspace(V_min, V_max, 400)
f_vals = f(V_vals)

# Graficar
plt.figure(figsize=(8,5))
plt.plot(V_vals, f_vals, label=f'Van der Waals a P={P} bar')
plt.axhline(0, color='black', linewidth=0.6)
plt.scatter([raiz], [0], color='red', s=80, label=f'Raíz: V = {raiz:.6f} L/mol') #type: ignore
plt.xlabel('Volumen molar V (L/mol)')
plt.ylabel('f(V)')
plt.title('Volumen molar real de CO₂ usando Van der Waals')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
