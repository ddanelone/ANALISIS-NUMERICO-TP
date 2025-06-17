import numpy as np
import matplotlib.pyplot as plt

def regula_falsi(f, a, b, tol=1e-6, max_iter=100, graficar=True):
    """
    Método de Regula Falsi con visualización gráfica en cada iteración.
    """
    if f(a) * f(b) >= 0:
        print("Error: f(a) y f(b) deben tener signos opuestos.")
        return None

    puntos = []  # Para almacenar los puntos (a, f(a)), (b, f(b)), (c, f(c))

    for i in range(max_iter):
        fa, fb = f(a), f(b)
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        puntos.append((a, b, c, fa, fb, fc))

        if abs(fc) < tol:
            break

        if fa * fc < 0:
            b = c
        else:
            a = c

    if graficar:
        x_vals = np.linspace(a - 1, b + 1, 500)
        y_vals = f(x_vals)

        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, label='f(x)', color='black')
        plt.axhline(0, color='gray', linestyle='--')

        for j, (a, b, c, fa, fb, fc) in enumerate(puntos):
            # Recta entre (a, f(a)) y (b, f(b))
            plt.plot([a, b], [fa, fb], color='orange', linestyle='--', alpha=0.6)
            # Punto de intersección c
            plt.plot(c, fc, 'o', color='red', label='Aproximación' if j == 0 else "")
        
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title("Método de Regula Falsi")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return c #type: ignore

# Función de prueba
def mi_funcion(x):
    return x**3 - x - 2

# Parámetros
a, b = 1, 2
raiz = regula_falsi(mi_funcion, a, b, tol=1e-6, max_iter=30)

if raiz is not None:
    print("Raíz aproximada:", raiz)
