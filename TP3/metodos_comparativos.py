import numpy as np
import matplotlib.pyplot as plt

# === Constantes CO₂ ===
R = 0.08314  # L·bar/mol·K
T = 300      # K
a = 3.592    # L²·bar/mol²
b = 0.04267  # L/mol
presiones = [50, 500]  # bar

# === Funciones de Van der Waals ===
def f_factory(P):
    def f(V):
        return (P + a / V**2) * (V - b) - R * T
    def f1(V):
        return (P - 2 * a / V**3) * (V - b) + (P + a / V**2)
    def f2(V):
        return 6 * a * (V - b) / V**4 - 2 * a / V**3 - 6 * a / V**4
    return f, f1, f2

# === Método ITP ===
def itp_method(f, a_int, b_int, tol=1e-10, max_iter=100, k=0.2):
    if f(a_int) * f(b_int) >= 0:
        raise ValueError("f(a) * f(b) >= 0, no hay cambio de signo.")

    iteraciones = []
    errores = []

    fa = f(a_int)
    fb = f(b_int)

    a, b = a_int, b_int

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

# === Método Taylor 2º orden ===
def taylor_2o(f, f1, f2, x0, tol=1e-10, max_iter=100):
    iteraciones = [x0]
    errores = []

    for _ in range(max_iter):
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

# === Graficar comparación ===
def graficar_comparacion(P, f, itp_iters, itp_raiz, taylor_iters, taylor_raiz):
    V_vals = np.linspace(0.05, 1.2, 400)
    y_vals = [f(V) for V in V_vals]

    plt.figure(figsize=(10, 6))
    plt.plot(V_vals, y_vals, label=f'f(V) a P={P} bar', color='black')
    plt.axhline(0, color='gray', linewidth=0.7)

    # ITP
    plt.scatter(itp_iters, [f(v) for v in itp_iters], color='red', label='ITP iteraciones', s=40)
    plt.scatter([itp_raiz], [f(itp_raiz)], color='darkred', s=80, label='ITP raíz')

    # Taylor
    plt.scatter(taylor_iters, [f(v) for v in taylor_iters], color='orange', label='Taylor 2º iteraciones', s=40)
    plt.scatter([taylor_raiz], [f(taylor_raiz)], color='darkorange', s=80, label='Taylor 2º raíz')

    plt.xlabel('Volumen molar V (L/mol)')
    plt.ylabel('f(V)')
    plt.title(f'Comparación ITP vs Taylor 2º Orden - Van der Waals a P = {P} bar')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Ejecución ===
for P in presiones:
    f, f1, f2 = f_factory(P)

    # Parámetros para ITP - intervalo razonable (búsqueda segura)
    a_int, b_int = 0.05, 1.0
    try:
        raiz_itp, itp_iters, itp_errs = itp_method(f, a_int, b_int)
    except Exception as e:
        print(f"[P={P} bar] ITP error: {e}")
        raiz_itp, itp_iters, itp_errs = None, [], []

    # Parámetros para Taylor - punto inicial cerca de la raíz esperada
    x0 = 0.2 if P == 500 else 0.8
    raiz_taylor, taylor_iters, taylor_errs = taylor_2o(f, f1, f2, x0)

    # Resultados numéricos
    print(f"\n[P = {P} bar]")
    if raiz_itp is not None:
        print(f"ITP: Raíz aproximada = {raiz_itp:.6f} L/mol, iteraciones = {len(itp_iters)}")
    print(f"Taylor 2º: Raíz aproximada = {raiz_taylor:.6f} L/mol, iteraciones = {len(taylor_iters)-1}")

    # Gráfica comparativa
    if raiz_itp is not None:
        graficar_comparacion(P, f, itp_iters, raiz_itp, taylor_iters, raiz_taylor)
    else:
        print(f"No se graficó ITP por error en P={P}")

