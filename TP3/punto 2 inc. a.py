import numpy as np
import matplotlib.pyplot as plt
import time

# ---------- Constantes ----------
R = 8.314  # J/(mol·K)
a = 0.364  # Pa·m^6/mol^2
b = 4.27e-5  # m^3/mol
T = 200  # K
P = 5e6  # Pa

# ---------- Ecuación de Van der Waals ----------
# (P + a / v^2)(v - b) - R*T = 0

def f(v):
    return (P + a / v**2) * (v - b) - R * T

def df(v):
    # Derivada de la función respecto a v
    return (-2 * a * (v - b) / v**3) + (P + a / v**2)

# ---------- Método de Newton-Raphson ----------
def newton_vdw(f, df, x0, tol=1e-10, max_iter=50):
    x = x0
    errores = []
    start = time.perf_counter()
    
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if dfx == 0:
            raise ZeroDivisionError("Derivada nula, método fallido.")
        dx = -fx / dfx
        x += dx
        errores.append(abs(dx))
        if abs(dx) < tol:
            break
    end = time.perf_counter()
    return x, errores, i+1, end - start

# ---------- Estimación inicial ----------
v_ideal = R * T / P  # Volumen molar ideal
v0 = v_ideal  # buen punto de partida

# ---------- Ejecutar método ----------
v_real, errores, iteraciones, tiempo = newton_vdw(f, df, v0)

# ---------- Resultados ----------
print("=== Cálculo del Volumen Molar Real (Van der Waals) ===")
print(f"Presión: {P/1e6} MPa")
print(f"Temperatura: {T} K")
print(f"Volumen molar ideal: {v_ideal:.6e} m³/mol")
print(f"Volumen molar real: {v_real:.6e} m³/mol")
print(f"Iteraciones: {iteraciones}")
print(f"Error final: {errores[-1]:.2e}")
print(f"Tiempo de ejecución: {tiempo:.6f} segundos")

# ---------- Gráfico de convergencia ----------
plt.figure(figsize=(8, 5))
plt.semilogy(range(1, len(errores)+1), errores, marker='o', label="Error |Δv|")
plt.xlabel("Iteración")
plt.ylabel("Error absoluto")
plt.title("Convergencia del Método de Newton-Raphson (Van der Waals)")
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
