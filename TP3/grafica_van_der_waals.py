import numpy as np
import matplotlib.pyplot as plt

# Constantes de Van der Waals para CO₂
R = 8.314
T = 200.0
a = 0.364
b = 4.267e-5

# Presiones a comparar
presiones = {
    "P = 5.0 MPa": 5e6,
    "P = 0.5 MPa": 0.5e6
}

# Dominio de volumen molar restringido
v_vals = np.linspace(b * 1.01, 0.005, 1000)

# Función de Van der Waals
def f_vdw(v, P):
    return (P + a / v**2) * (v - b) - R * T

# Crear gráfico
plt.figure(figsize=(10, 6))

for etiqueta, P in presiones.items():
    f_vals = []
    for v in v_vals:
        try:
            f = f_vdw(v, P)
            f_vals.append(f)
        except:
            f_vals.append(np.nan)
    
    color = 'blue' if P > 1e6 else 'red'
    plt.plot(v_vals, f_vals, label=etiqueta, color=color)

# Estética del gráfico
plt.axhline(0, color="gray", linestyle="--")
plt.axvline(b, color="black", linestyle=":", label=f"b = {b:.2e} m³/mol")
plt.xlim([b * 1.01, 0.005])
plt.title("f(v) de Van der Waals (CO₂) - Comparación de presiones")
plt.xlabel("Volumen molar v (m³/mol)")
plt.ylabel("f(v)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
