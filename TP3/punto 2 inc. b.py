import numpy as np
import matplotlib.pyplot as plt
import time

# Constantes
R = 8.314
a = 0.364
b = 4.27e-5
T = 200
P = 5e5  # 0.5 MPa en Pa

def f(v):
    return (P + a / v**2) * (v - b) - R * T

def df(v):
    return -2 * a * (v - b) / v**3 + (P + a / v**2)

def newton(f, df, x0, tol=1e-10, max_iter=100):
    x = x0
    errores = []
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if abs(dfx) < 1e-14:  # evito división por cero o cerca
            raise ZeroDivisionError("Derivada nula o casi nula")
        dx = -fx / dfx
        x_new = x + dx
        errores.append(abs(dx))
        if abs(dx) < tol:
            return x_new, errores, i + 1
        x = x_new
    raise RuntimeError("No convergió en Newton")

def biseccion(f, a, b, tol=1e-10, max_iter=100):
    errores = []
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("No hay cambio de signo en el intervalo para bisección")
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        errores.append(abs(b - a))
        if abs(b - a) < tol or abs(fc) < tol:
            return c, errores, i + 1
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    raise RuntimeError("No convergió en bisección")

# Condiciones iniciales para Newton (que den volumen > b)
condiciones_newton = [
    ("Ideal", R * T / P),
    ("Cercana a b + 1e-4", b + 1e-4),
]

# Intervalos para bisección (debe haber cambio de signo)
intervalos_bis = [
    ("Intervalo 1", b + 1e-6, 1e-3),  # intervalo pequeño
    ("Intervalo 2", R*T/P/2, R*T/P*2),  # alrededor de ideal
]

# Ejecución y gráficas

plt.figure(figsize=(10,6))

for nombre, x0 in condiciones_newton:
    try:
        v, err_n, it = newton(f, df, x0)
        print(f"[Newton] Condición '{nombre}': Raíz en {v:.6e}, iter={it}, error final={err_n[-1]:.2e}")
        plt.semilogy(range(1,len(err_n)+1), err_n, label=f'Newton - {nombre}')
    except Exception as e:
        print(f"[Newton] Condición '{nombre}' falló: {e}")

for nombre, a_bis, b_bis in intervalos_bis:
    try:
        v, err_b, it = biseccion(f, a_bis, b_bis)
        print(f"[Bisección] {nombre}: Raíz en {v:.6e}, iter={it}, error final={err_b[-1]:.2e}")
        plt.semilogy(range(1,len(err_b)+1), err_b, label=f'Bisección - {nombre}')
    except Exception as e:
        print(f"[Bisección] {nombre} falló: {e}")

plt.title("Convergencia de métodos para resolver Van der Waals a P=0.5 MPa")
plt.xlabel("Iteración")
plt.ylabel("Error absoluto")
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
