import numpy as np
import matplotlib.pyplot as plt

# Función loca
def f(x):
    return np.sin(5 * x) * np.exp(-x / 10) - 0.1

FUNCION_STR = "f(x) = sin(5x) * exp(-x/10) - 0.1"

# Método ITP
def itp_method(f, a, b, tol=1e-10, max_iter=100, k=0.2):
    if f(a) * f(b) >= 0:
        raise ValueError("El intervalo no cumple f(a) * f(b) < 0")

    iteraciones = []
    errores = []

    fa = f(a)
    fb = f(b)

    for n in range(max_iter):
        c = (a + b) / 2
        r = b - a
        d = k * r**2
        x_lin = (fb * a - fa * b) / (fb - fa)

        if abs(x_lin - c) <= d:
            x_itp = x_lin
        else:
            x_itp = c - np.sign(x_lin - c) * d

        fx = f(x_itp)
        iteraciones.append(x_itp)
        errores.append(abs(fx))

        if abs(fx) < tol or (b - a) / 2 < tol:
            break

        if fa * fx < 0:
            b = x_itp
            fb = fx
        else:
            a = x_itp
            fa = fx

    return x_itp, iteraciones, errores # type: ignore

# Orden de convergencia
def estimar_orden_convergencia(errores):
    p_values = []
    for i in range(2, len(errores)):
        if errores[i-1] == 0 or errores[i-2] == 0:
            continue
        num = np.log(errores[i] / errores[i-1])
        den = np.log(errores[i-1] / errores[i-2])
        if den != 0:
            p = num / den
            p_values.append(p)
    return p_values

# Gráfico
def graficar_iteraciones(f, iteraciones, raiz_aprox, funcion_str):
    x_vals = np.linspace(min(iteraciones) - 1, max(iteraciones) + 1, 1000)
    y_vals = f(x_vals)

    plt.figure(figsize=(12, 6))
    plt.plot(x_vals, y_vals, label=funcion_str, color='blue')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.scatter(iteraciones, [f(x) for x in iteraciones], color='red', label='Iteraciones')
    plt.scatter([raiz_aprox], [f(raiz_aprox)], color='green', s=80, label='Raíz final')
    for i, x in enumerate(iteraciones):
        plt.annotate(f'{i+1}', (x, f(x)), textcoords="offset points", xytext=(0, 6), ha='center', fontsize=8)
    plt.title('Evolución de las iteraciones hacia la raíz')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Configuración ===
a, b = 1.5, 2   # Intervalo grande
tol = 1e-10       # Tolerancia estricta

# === Ejecución ===
try:
    raiz, iteraciones, errores = itp_method(f, a, b, tol=tol, max_iter=100)
except ValueError as e:
    print(f"Error: {e}")
    exit()

# === Resultados ===
ordenes = estimar_orden_convergencia(errores)

print(f"\nRaíz aproximada: {raiz:.10f}")
print(f"Cantidad de iteraciones: {len(iteraciones)}")
print("Errores estimados:")
for i, e in enumerate(errores):
    print(f"Iteración {i+1}: error = {e:.2e}")

if ordenes:
    orden_promedio = np.mean(ordenes)
    print(f"Orden de convergencia estimado: {orden_promedio:.4f}")
else:
    print("No se pudo estimar el orden de convergencia.")

# === Gráfico ===
graficar_iteraciones(f, iteraciones, raiz, FUNCION_STR)
