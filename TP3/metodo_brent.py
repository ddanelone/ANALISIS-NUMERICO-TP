import numpy as np
import matplotlib.pyplot as plt

def brent(f, a=0.0, b=1.0, tol=1e-12, max_iter=100):
    fa = f(a)
    fb = f(b)
    if fa * fb >= 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo.")

    if abs(fa) < abs(fb):
        a, b = b, a
        fa, fb = fb, fa

    c = a
    fc = fa
    d = b  # Inicializar d como numérico
    mflag = True

    for i in range(max_iter):
        if fa != fc and fb != fc:
            # Interpolación cuadrática inversa
            s = a * fb * fc / ((fa - fb) * (fa - fc)) + \
                b * fa * fc / ((fb - fa) * (fb - fc)) + \
                c * fa * fb / ((fc - fa) * (fc - fb))
        elif fa != fb:
            # Método de la secante
            s = b - fb * (b - a) / (fb - fa)
        else:
            # Bisección directa si todos son iguales
            s = (a + b) / 2

        # Criterios para rechazar s y usar bisección
        conditions = [
            not (min(a, b) < s < max(a, b)),
            mflag and abs(s - b) >= abs(b - c) / 2,
            not mflag and abs(s - b) >= abs(c - d) / 2,
            mflag and abs(b - c) < tol,
            not mflag and abs(c - d) < tol
        ]

        if any(conditions):
            s = (a + b) / 2
            mflag = True
        else:
            mflag = False

        fs = f(s)
        d, c = c, b
        fc, fb_old = fb, fb  # Guardar por seguridad

        if fa * fs < 0:
            b = s
            fb = fs
        else:
            a = s
            fa = fs

        if abs(fa) < abs(fb):
            a, b = b, a
            fa, fb = fb, fa

        if abs(fb) < tol or abs(b - a) < tol:
            return b

    raise RuntimeError("El método de Brent no converge")

# Definición de la función
def f(x):
    return np.cos(x) - x

# Intervalo conocido que encierra la raíz
a, b = 0, 1

# Guardamos los puntos evaluados manualmente
puntos_evaluados = []

# Envolvemos f para guardar puntos
def f_tracking(x):
    fx = f(x)
    puntos_evaluados.append((x, fx))
    return fx

# Ejecutamos el método de Brent
raiz = brent(f_tracking, a, b, tol=1e-10, max_iter=100)

print(f"Raíz aproximada: {raiz:.10f}")
print(f"f(raíz) = {f(raiz):.2e}")
print(f"Cantidad de evaluaciones: {len(puntos_evaluados)}")

# Gráfico
x_vals = np.linspace(a, b, 500)
y_vals = f(x_vals)

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label='f(x)', color='black')
plt.axhline(0, color='gray', linestyle='--')

# Puntos evaluados
for x, fx in puntos_evaluados:
    color = 'red' if fx < 0 else 'blue'
    plt.plot(x, fx, 'o', color=color)

plt.title("Método de Brent - Evaluación de f(x)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
