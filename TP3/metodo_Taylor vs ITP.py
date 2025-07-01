import numpy as np
import matplotlib.pyplot as plt

# === Función ===
def f(x):
    return np.sin(5 * x) * np.exp(-x / 10) - 0.1

def f1(x):
    return (5 * np.cos(5 * x) * np.exp(-x / 10)) - (0.1 * np.sin(5 * x) * np.exp(-x / 10))

def f2(x):
    e = np.exp(-x / 10)
    sin = np.sin(5 * x)
    cos = np.cos(5 * x)
    term1 = -25 * sin * e / 10
    term2 = -10 * cos * e / 10
    term3 = -0.5 * sin * e / 10
    return -25 * sin * e / 10 - 10 * cos * e / 10 - 0.5 * sin * e / 10

FUNCION_STR = "f(x) = sin(5x) * exp(-x/10) - 0.1"

# === Método de Taylor 2° orden ===
def taylor_segundo_orden(f, f1, f2, x0, tol=1e-10, max_iter=100):
    iteraciones = [x0]
    errores = []

    for n in range(max_iter):
        fx = f(x0)
        fx1 = f1(x0)
        fx2 = f2(x0)

        denom = fx1**2 - fx * fx2
        if denom == 0:
            print("Denominador cero. Deteniendo.")
            break

        x1 = x0 - (fx * fx1) / denom
        iteraciones.append(x1)
        errores.append(abs(f(x1)))

        if abs(f(x1)) < tol:
            break

        x0 = x1

    return x1, iteraciones, errores # type: ignore

# === Estimación orden de convergencia ===
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

# === Gráfico ===
def graficar_iteraciones(f, iteraciones, raiz_aprox, funcion_str):
    x_vals = np.linspace(min(iteraciones) - 1, max(iteraciones) + 1, 1000)
    y_vals = f(x_vals)

    plt.figure(figsize=(12, 6))
    plt.plot(x_vals, y_vals, label=funcion_str, color='blue')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.scatter(iteraciones, [f(x) for x in iteraciones], color='orange', label='Iteraciones')
    plt.scatter([raiz_aprox], [f(raiz_aprox)], color='green', s=80, label='Raíz final')
    for i, x in enumerate(iteraciones):
        plt.annotate(f'{i+1}', (x, f(x)), textcoords="offset points", xytext=(0, 6), ha='center', fontsize=8)
    plt.title('Taylor 2° Orden - Evolución hacia la raíz')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Configuración ===
x0 = 1.5       # valor inicial
tol = 1e-10    # tolerancia

# === Ejecución ===
raiz, iteraciones, errores = taylor_segundo_orden(f, f1, f2, x0, tol=tol)

# === Resultados ===
ordenes = estimar_orden_convergencia(errores)

print(f"\nRaíz aproximada: {raiz:.10f}")
print(f"Cantidad de iteraciones: {len(iteraciones)-1}")
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
