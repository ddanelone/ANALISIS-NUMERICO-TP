import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Constantes físicas
R = 8.314  # J/(mol·K)
a = 3.592 * 100  # J·L/mol²
b = 0.0427  # L/mol
n = 1  # mol

# Presiones en MPa → las pasamos a Pa al usar en ecuaciones
P_MPa = np.linspace(0.1, 10, 300)  # de 0.1 a 10 MPa
P_Pa = P_MPa * 1e6  # en Pascales

# Temperaturas (en K)
temperaturas = [150, 200, 250, 300]
colores = ['blue', 'green', 'orange', 'red']

# Figura
fig, ax = plt.subplots(figsize=(10, 6))

# Función para resolver la ecuación de Van der Waals y obtener Vm
def resolver_vm(P, T):
    # Ecuación: P = RT / (Vm - b) - a / Vm^2
    # La pasamos a la forma f(Vm) = 0
    def f(Vm):
        return (R * T) / (Vm - b) - a / Vm**2 - P
    Vm_inicial = R * T / P  # estimación inicial desde gas ideal
    Vm_sol, = fsolve(f, Vm_inicial) # type: ignore
    return Vm_sol if Vm_sol > b else np.nan  # descartar resultados no físicos

# Graficar Z en función de P para cada T
for T, color in zip(temperaturas, colores):
    Z_list = []
    for P in P_Pa:
        try:
            Vm = resolver_vm(P, T)
            Z = (P * Vm) / (R * T)
        except:
            Z = np.nan
        Z_list.append(Z)
    ax.plot(P_Pa / 1e6, Z_list, label=f"T = {T} K", color=color)

# Línea horizontal Z = 1 (gas ideal)
ax.axhline(1, color='black', linestyle='dashed', label='Gas Ideal (Z = 1)')

# Línea vertical en 5 MPa
ax.axvline(5, color='red', linestyle='dotted', linewidth=1, label='P = 5 MPa')

# Etiquetas
ax.set_xlabel("Presión (MPa)")
ax.set_ylabel(r"$Z = \frac{PV}{nRT}$")
ax.set_title("Factor de Compresibilidad del CO₂ según Van der Waals")
ax.legend(loc='upper left')
ax.grid(True)
plt.tight_layout()
plt.show()
