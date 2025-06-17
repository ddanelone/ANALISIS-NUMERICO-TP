import numpy as np
import matplotlib.pyplot as plt

def biseccion(f, a, b, maxit=50, tol=1e-6):
    """
    Método de bisección que guarda el error y puntos evaluados en cada iteración.
    
    Retorna:
    - m: raíz aproximada
    - err: error final
    - errores: lista de errores en x
    - puntos: lista de tuplas (m, f(m))
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La función no cambia de signo en el intervalo dado.")

    errores = []
    puntos = []

    for _ in range(maxit):
        m = (a + b) / 2
        fm = f(m)
        err = (b - a) / 2
        errores.append(err)
        puntos.append((m, fm))

        if abs(fm) < tol or err < tol:
            return m, err, errores, puntos

        if f(a) * fm < 0:
            b = m
        else:
            a = m

    return m, err, errores, puntos #type: ignore

# Función de ejemplo
def f(x):
    return np.exp(-x) - x

# Llamada al método
a, b = 0, 1
raiz, err_final, errores, puntos = biseccion(f, a, b, maxit=100, tol=1e-8)

print(f"Raíz aproximada: {raiz:.8f}")
print(f"Error final: {err_final:.2e}")
print(f"Iteraciones: {len(errores)}")

# Gráfico del error en escala logarítmica
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(errores) + 1), errores, marker='o')
plt.yscale('log')
plt.xlabel("Iteración")
plt.ylabel("Error en x")
plt.title("Convergencia del método de bisección")
plt.grid(True, which='both', linestyle='--')
plt.tight_layout()
plt.show()

# Gráfico de los puntos evaluados según el signo
x_vals = [m for m, _ in puntos]
y_vals = [fval for _, fval in puntos]

colors = ['red' if fval < 0 else 'blue' for fval in y_vals]

plt.figure(figsize=(8, 5))
plt.scatter(x_vals, y_vals, c=colors, s=60, edgecolors='k')
plt.axhline(0, color='gray', linestyle='--')
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Puntos evaluados durante la bisección")
plt.grid(True)
plt.tight_layout()
plt.show()
