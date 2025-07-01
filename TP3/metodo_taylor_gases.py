import numpy as np
import matplotlib.pyplot as plt

# === Constantes CO₂ ===
R = 0.08314  # L·bar/mol·K
T = 300      # K
a = 3.592    # L²·bar/mol²
b = 0.04267  # L/mol
presiones = [50, 500]  # bar (equivalentes a 0.5 y 5 MPa)

# === Función de Van der Waals ===
def van_der_waals(P):
    def f(V):
        return (P + a / V**2) * (V - b) - R * T
    return f

# === Método ITP ===
def itp_method(f, a, b, tol=1e-10, max_iter=100, k=0.2):
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) * f(b) >= 0, no hay cambio de signo.")

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

        if abs(fx) < tol or (b - a)/2 < tol:
            break

        if fa * fx < 0:
            b = x_itp
            fb = fx
        else:
            a = x_itp
            fa = fx

    return x_itp, iteraciones, errores # type: ignore

# === Graficar ===
def graficar(P, f, iteraciones, raiz_aprox):
    V_vals = np.linspace(0.05, 1.2, 400)
    y_vals = [f(V) for V in V_vals]

    plt.figure(figsize=(10, 5))
    plt.plot(V_vals, y_vals, label=f'f(V) a P={P} bar')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.scatter(iteraciones, [f(v) for v in iteraciones], color='red', label='Iteraciones')
    plt.scatter([raiz_aprox], [f(raiz_aprox)], color='green', s=80, label='Raíz final')
    plt.xlabel('Volumen molar V (L/mol)')
    plt.ylabel('f(V)')
    plt.title(f'Método ITP - Van der Waals a P = {P} bar')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Ejecución para cada presión ===
for P in presiones:
    f = van_der_waals(P)
    try:
        V0, iters, errs = itp_method(f, a=0.05, b=1.0)
        print(f"\n[P = {P} bar] Volumen molar aproximado: {V0:.6f} L/mol")
        print(f"Iteraciones: {len(iters)}")
    except Exception as e:
        print(f"[P = {P} bar] Error: {e}")
        continue

    graficar(P, f, iters, V0)
