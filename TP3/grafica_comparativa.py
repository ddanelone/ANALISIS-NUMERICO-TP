import numpy as np
import matplotlib.pyplot as plt

# Constantes físicas
R = 8.314  # J/(mol·K)

# Constantes de Van der Waals para el CO₂
a = 3.592  # L²·bar/mol²
b = 0.0427  # L/mol

# Conversión: 1 L·bar = 100 J
a = a * 100  # en J·L/mol²

# Temperaturas (K)
temperaturas = [150, 200, 250, 300]
colores = ['blue', 'green', 'orange', 'red']

# Rango de presiones en bar
P = np.linspace(0.1, 100, 500)  # bar
P_Pa = P * 1e5  # en Pascales

# Número de moles y volumen molar
n = 1  # mol
Vm = np.linspace(0.05, 5, 500)  # Volumen molar en L/mol

# Figura
fig, ax = plt.subplots(figsize=(10, 6))

# Graficar curvas de Van der Waals
for T, color in zip(temperaturas, colores):
    P_vdw = (n * R * T) / (Vm - b) - a / Vm**2  # presión en Pa
    Z_vdw = (P_vdw * Vm) / (n * R * T)  # factor de compresibilidad

    # Filtrar valores físicos
    mask = (Vm > b) & (P_vdw > 0) & (Z_vdw > 0)
    ax.plot(P_vdw[mask] / 1e5, Z_vdw[mask], label=f"T = {T} K", color=color)

# Línea horizontal para gas ideal
ax.axhline(1, color='black', linestyle='dashed', label='Gas Ideal (Z = 1)')

# Etiquetas
ax.set_xlabel("Presión (bar)")
ax.set_ylabel(r"$\frac{PV}{nRT}$")
ax.set_title("Comportamiento del CO₂: Gas Ideal vs Van der Waals")

# Leyenda
ax.legend(loc='upper right')

# Ajustes
plt.grid(True)
plt.tight_layout()
plt.show()
