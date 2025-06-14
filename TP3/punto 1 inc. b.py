import numpy as np
import matplotlib.pyplot as plt

# ---------- Método combinado Bisección + Taylor ----------

def combinado_biseccion_taylor(f, df, d2f, a, b, tol=1e-10, max_iter=100):
    if f(a) * f(b) >= 0:
        raise ValueError("El intervalo [a, b] no encierra una raíz")

    errores = []
    x = (a + b) / 2
    
    for i in range(max_iter):
        fx = f(x)

        if abs(fx) < tol or abs(b - a) < tol:
            break

        try:
            dfx = df(x)
            d2fx = d2f(x)
            discriminante = dfx**2 - 2 * fx * d2fx

            if discriminante >= 0 and d2fx != 0:
                sqrt_disc = np.sqrt(discriminante)
                if abs(dfx + sqrt_disc) > abs(dfx - sqrt_disc):
                    h = (-2 * fx) / (dfx + sqrt_disc)
                else:
                    h = (-2 * fx) / (dfx - sqrt_disc)
                x_new = x + h

                if a < x_new < b:
                    x = x_new
                else:
                    x = (a + b) / 2
            else:
                x = (a + b) / 2

        except Exception:
            x = (a + b) / 2

        if f(a) * f(x) < 0:
            b = x
        else:
            a = x

        error = abs(b - a)
        errores.append(error)

    return x, errores, i + 1

# ---------- Método de Bisección puro ----------

def biseccion_pura(f, a, b, tol=1e-10, max_iter=100):
    errores = []
    for i in range(max_iter):
        x = (a + b) / 2
        fx = f(x)
        if abs(fx) < tol or abs(b - a) < tol:
            break
        if f(a) * fx < 0:
            b = x
        else:
            a = x
        errores.append(abs(b - a))
    return x, errores, i + 1

# ---------- Función de prueba ----------
f = lambda x: x**3 - x - 2
df = lambda x: 3*x**2 - 1
d2f = lambda x: 6*x

# ---------- Ejecución de ambos métodos ----------
raiz_comb, errores_comb, iter_comb = combinado_biseccion_taylor(f, df, d2f, a=1, b=2)
raiz_bis, errores_bis, iter_bis = biseccion_pura(f, a=1, b=2)

# ---------- Salida por consola ----------
print("=== Método Combinado Bisección + Taylor ===")
print(f"Raíz aproximada: {raiz_comb}")
print(f"Error final: {errores_comb[-1]}")
print(f"Iteraciones: {iter_comb}")

print("\n=== Método Bisección Pura ===")
print(f"Raíz aproximada: {raiz_bis}")
print(f"Error final: {errores_bis[-1]}")
print(f"Iteraciones: {iter_bis}")

# ---------- Gráfico comparativo ----------
plt.figure(figsize=(10, 6))
plt.semilogy(range(1, len(errores_comb)+1), errores_comb, label="Combinado Bisección + Taylor", marker='o')
plt.semilogy(range(1, len(errores_bis)+1), errores_bis, label="Bisección pura", marker='s')
plt.xlabel("Iteración")
plt.ylabel("Error absoluto (escala log)")
plt.title("Comparación de convergencia entre métodos")
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
import numpy as np
import matplotlib.pyplot as plt
import time

# ---------- Método combinado Bisección + Taylor ----------

def combinado_biseccion_taylor(f, df, d2f, a, b, tol=1e-10, max_iter=100):
    if f(a) * f(b) >= 0:
        raise ValueError("El intervalo [a, b] no encierra una raíz")

    errores = []
    x = (a + b) / 2
    
    for i in range(max_iter):
        fx = f(x)
        if abs(fx) < tol or abs(b - a) < tol:
            break

        try:
            dfx = df(x)
            d2fx = d2f(x)
            discriminante = dfx**2 - 2 * fx * d2fx

            if discriminante >= 0 and d2fx != 0:
                sqrt_disc = np.sqrt(discriminante)
                if abs(dfx + sqrt_disc) > abs(dfx - sqrt_disc):
                    h = (-2 * fx) / (dfx + sqrt_disc)
                else:
                    h = (-2 * fx) / (dfx - sqrt_disc)
                x_new = x + h

                if a < x_new < b:
                    x = x_new
                else:
                    x = (a + b) / 2
            else:
                x = (a + b) / 2

        except Exception:
            x = (a + b) / 2

        if f(a) * f(x) < 0:
            b = x
        else:
            a = x

        error = abs(b - a)
        errores.append(error)

    return x, errores, i + 1

# ---------- Método de Bisección puro ----------

def biseccion_pura(f, a, b, tol=1e-10, max_iter=100):
    errores = []
    for i in range(max_iter):
        x = (a + b) / 2
        fx = f(x)
        if abs(fx) < tol or abs(b - a) < tol:
            break
        if f(a) * fx < 0:
            b = x
        else:
            a = x
        errores.append(abs(b - a))
    return x, errores, i + 1

# ---------- Función de prueba ----------
f = lambda x: x**3 - x - 2
df = lambda x: 3*x**2 - 1
d2f = lambda x: 6*x

# ---------- Ejecución y medición de tiempo ----------
start_comb = time.perf_counter()
raiz_comb, errores_comb, iter_comb = combinado_biseccion_taylor(f, df, d2f, a=1, b=2)
end_comb = time.perf_counter()
tiempo_comb = end_comb - start_comb

start_bis = time.perf_counter()
raiz_bis, errores_bis, iter_bis = biseccion_pura(f, a=1, b=2)
end_bis = time.perf_counter()
tiempo_bis = end_bis - start_bis

# ---------- Salida por consola ----------
print("=== Método Combinado Bisección + Taylor ===")
print(f"Raíz aproximada: {raiz_comb}")
print(f"Error final: {errores_comb[-1]}")
print(f"Iteraciones: {iter_comb}")
print(f"Tiempo de ejecución: {tiempo_comb:.6f} segundos")

print("\n=== Método Bisección Pura ===")
print(f"Raíz aproximada: {raiz_bis}")
print(f"Error final: {errores_bis[-1]}")
print(f"Iteraciones: {iter_bis}")
print(f"Tiempo de ejecución: {tiempo_bis:.6f} segundos")

# ---------- Gráfico 1: Error por iteración ----------
plt.figure(figsize=(10, 5))
plt.semilogy(range(1, len(errores_comb)+1), errores_comb, label="Combinado Bisección + Taylor", marker='o')
plt.semilogy(range(1, len(errores_bis)+1), errores_bis, label="Bisección pura", marker='s')
plt.xlabel("Iteración")
plt.ylabel("Error absoluto (escala log)")
plt.title("Comparación de convergencia entre métodos")
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# ---------- Gráfico 2: Comparación de tiempos ----------
plt.figure(figsize=(6, 4))
plt.bar(["Combinado", "Bisección pura"], [tiempo_comb, tiempo_bis], color=["#2ca02c", "#1f77b4"])
plt.ylabel("Tiempo de ejecución (segundos)")
plt.title("Comparación de tiempo entre métodos")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
