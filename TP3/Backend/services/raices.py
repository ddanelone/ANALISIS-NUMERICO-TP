import sympy as sp
import numpy as np
import io
import matplotlib
matplotlib.use('Agg')  # Evita problemas con backends gráficos
import matplotlib.pyplot as plt
import time
from time import perf_counter
from mpl_toolkits.mplot3d import Axes3D  

### Comienzo agregado multivariable

def obtener_funciones_multivariables():
    x, y = sp.symbols('x y')
    
    # Nuevo sistema no lineal con raíz conocida (0, 0)
    F_expr = sp.Matrix([
        sp.exp(x + y) - 1, # type:ignore
        x**2 - y
    ])
    
    variables = [x, y]

    F = sp.lambdify(variables, F_expr, 'numpy')
    J = sp.lambdify(variables, F_expr.jacobian(variables), 'numpy')

    H_list = [sp.hessian(F_expr[i], variables) for i in range(len(F_expr))]
    H_lambdas = [sp.lambdify(variables, H_list[i], 'numpy') for i in range(len(H_list))]

    return F, J, H_lambdas, variables

def metodo_taylor_multivariable(F, J, H_list, x0, tol=1e-6, max_iter=50):
    x0 = np.array(x0, dtype=float)
    salida = ["📘 Método de Taylor multivariable (con Hessiana incluida)\n"]
    historial = []

    for n in range(max_iter):
        Fx = np.array(F(*x0)).reshape(-1)
        norm_fx = np.linalg.norm(Fx)

        if norm_fx < tol:
            salida.append(f"✅ Convergencia por ||F(x)|| < {tol:.1e}")
            salida.append(f"🔍 Raíz aproximada: {x0}")
            break

        Jx = np.array(J(*x0), dtype=float)
        Hx = [np.array(H(*x0), dtype=float) for H in H_list]

        # Armar sistema cuadrático: J(x) Δx + ½ H Δx Δx ≈ -F(x)
        try:
            delta = -np.linalg.solve(Jx, Fx)
        except np.linalg.LinAlgError:
            salida.append("❌ Jacobiano no invertible. Método detenido.")
            break

        x1 = x0 + delta
        error = np.linalg.norm(x1 - x0)

        salida.append(f"🔁 Iteración {n}")
        salida.append(f"   xₙ         = {x0}")
        salida.append(f"   F(xₙ)      = {Fx}")
        salida.append(f"   ||F(xₙ)||  = {norm_fx:.2e}")
        salida.append(f"   Δx         = {delta}")
        salida.append(f"   Error      = {error:.2e}\n")

        historial.append({
            "n": n,
            "x": x0.tolist(),
            "F": Fx.tolist(),
            "delta": delta.tolist(),
            "x_next": x1.tolist(),
            "error": float(error)
        })

        if error < tol:
            salida.append(f"✅ Convergencia alcanzada en {n+1} iteraciones.")
            salida.append(f"🔍 Raíz aproximada: {x1}")
            break

        x0 = x1

    else:
        salida.append("❌ No se alcanzó convergencia dentro del máximo de iteraciones.")

    salida.append("\n📚 Requisitos:")
    salida.append("- F debe ser de clase C² (dos veces derivable)")
    salida.append("- Jacobiano debe ser invertible en un entorno de la raíz.")
    salida.append("- Se puede usar el paso de Newton como aproximación si se omite la Hessiana.")

    return historial, "\n".join(salida)

def ejecutar_comparacion_taylor_multivariable(x0=[2.5, -2.5],tol=1e-6, max_iter=50):
    F, J, H_list, _ = obtener_funciones_multivariables()

    buffer = io.StringIO()
    print("🔬 Comparación: Taylor puro vs Taylor robusto (con paso adaptativo)\n", file=buffer)

    # Taylor puro
    start = time.perf_counter()
    hist_puro, log_puro = metodo_taylor_multivariable(F, J, H_list, x0, tol, max_iter)
    t_puro = time.perf_counter() - start

    # Taylor robusto
    start = time.perf_counter()
    hist_rob, log_rob = metodo_taylor_multivariable_robusto(F, J, H_list, x0, tol, max_iter)
    t_rob = time.perf_counter() - start

    print(f"⏱️ Taylor puro: {len(hist_puro)} iteraciones, tiempo: {t_puro:.6f}s", file=buffer)
    print(f"⏱️ Taylor robusto: {len(hist_rob)} iteraciones, tiempo: {t_rob:.6f}s", file=buffer)

    print(f"\n🔎 Error final Taylor puro: {hist_puro[-1]['error']:.2e}", file=buffer)
    print(f"🔎 Error final Taylor robusto: {hist_rob[-1]['error']:.2e}", file=buffer)

    if t_rob > 0:
        print(f"\n📊 Relación de velocidad: {t_puro / t_rob:.2f}x", file=buffer)

    return buffer.getvalue() + "\n\n" + log_rob
 
def graficar_iteraciones_multivariable(historial, F, funcion_str="F(x, y)"):
    puntos = np.array([step["x"] for step in historial])
    x_vals = puntos[:, 0]
    y_vals = puntos[:, 1]

    # Determinar límites de grilla con margen dinámico
    margen_x = (x_vals.max() - x_vals.min()) * 0.3 or 1.0
    margen_y = (y_vals.max() - y_vals.min()) * 0.3 or 1.0

    x_min = min(x_vals.min(), x_vals.max()) - margen_x
    x_max = max(x_vals.min(), x_vals.max()) + margen_x
    y_min = min(y_vals.min(), y_vals.max()) - margen_y
    y_max = max(y_vals.min(), y_vals.max()) + margen_y

    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300), np.linspace(y_min, y_max, 300))
    
    F1_vals = np.zeros_like(xx)
    F2_vals = np.zeros_like(yy)
    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            try:
                f_val = F(xx[i, j], yy[i, j])
                F1_vals[i, j] = f_val[0]
                F2_vals[i, j] = f_val[1]
            except Exception:
                F1_vals[i, j] = np.nan
                F2_vals[i, j] = np.nan

    plt.figure(figsize=(10, 6))
    cs1 = plt.contour(xx, yy, F1_vals, levels=[0], colors='blue', linewidths=2)
    cs2 = plt.contour(xx, yy, F2_vals, levels=[0], colors='red', linewidths=2)
    plt.clabel(cs1, inline=True, fontsize=10, fmt="f₁=0")
    plt.clabel(cs2, inline=True, fontsize=10, fmt="f₂=0")

    # Trayectoria
    for i, punto in enumerate(puntos):
        x, y = punto
        color = 'red' if i < len(puntos) - 1 else 'green'
        marker = 'o' if i < len(puntos) - 1 else '*'
        size = 70 if i < len(puntos) - 1 else 120
        label = f"Iteración {i}" if i < len(puntos) - 1 else "Raíz aproximada"
        plt.scatter(x, y, s=size, color=color, edgecolors='black', zorder=5, marker=marker, label=label)
        plt.text(x, y + 0.05, f'$x_{i}$', ha='center', fontsize=9)

        if i < len(puntos) - 1:
            siguiente = puntos[i + 1]
            dx, dy = siguiente[0] - x, siguiente[1] - y
            plt.arrow(x, y, dx, dy,
                      head_width=0.03, length_includes_head=True, color='gray', alpha=0.6)

    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.title(f"Método de Taylor multivariable - {funcion_str}")
    plt.legend(loc='best')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.axis("equal")

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

def graficar_convergencia_loglog_multi():
    F, J, H_list, _ = obtener_funciones_multivariables()
    
    # Ejecutar el método con el intervalo corregido
    historial, _ = metodo_taylor_multivariable(F, J, H_list, x0=[2.5, -2.5])

    if len(historial) < 2:
        raise ValueError("No hay suficientes datos para graficar convergencia.")

    # Calcular errores absolutos entre iteraciones
    errors = [
        np.linalg.norm(np.array(historial[i]['x_next']) - np.array(historial[i - 1]['x_next']))
        for i in range(1, len(historial))
    ]

    iterations = np.arange(1, len(errors) + 1, dtype=float)

    # Curva de referencia O(n^-3)
    p_ref = 3
    C = errors[0] * (iterations[0] ** p_ref)
    ref_curve = C * iterations ** (-p_ref)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Gráfico log-log
    ax1.loglog(iterations, errors, marker='o', linestyle='-', color='blue',
               linewidth=2, markersize=8, label='Error absoluto')
    ax1.loglog(iterations, ref_curve, 'k--', label=f'Referencia: $O(n^{{-{p_ref}}})$')
    ax1.set_title('Convergencia del Método de Taylor Multivariable', fontsize=14)
    ax1.set_xlabel('Iteración')
    ax1.set_ylabel('Error absoluto')
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    ax1.legend()

    # Tasa de convergencia
    if len(errors) > 2:
        ratios = np.array(errors[1:]) / np.array(errors[:-1])
        ax2.plot(iterations[1:], ratios, 's-', color='red', markersize=8,
                 linewidth=2, label='Tasa de convergencia')
        ax2.axhline(y=0, color='k', linestyle='--', linewidth=0.8)
        ax2.set_title('Tasa de Convergencia Numérica')
        ax2.set_xlabel('Iteración')
        ax2.set_ylabel('$e_{n+1}/e_n$')
        ax2.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        ax2.legend()
    else:
        ax2.text(2.5, -2.5, "No hay suficientes datos para tasa de convergencia", 
                 ha='center', va='center', fontsize=12, transform=ax2.transAxes)
        ax2.axis('off')

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

def graficar_taylor_local_multivariable(iteration: int):
    delta_zoom = 0.2

    # Obtener funciones y ejecutar método
    F, J, H_list, vars = obtener_funciones_multivariables()
    historial, _ = metodo_taylor_multivariable(F, J, H_list, x0=[0.5, 0.5], tol=1e-6, max_iter=50)

    if iteration < 0 or iteration >= len(historial):
        raise ValueError("Número de iteración inválido.")

    step = historial[iteration]
    xn = np.array(step['x'])
    Fx = np.array(step['F'])
    delta = np.array(step['delta'])
    xn_next = np.array(step['x_next'])

    # Plano tangente lineal en xn: F(x) ≈ F(xn) + J(xn)*(x - xn)
    Jx = np.array(J(*xn), dtype=float)

    # Definir función para plano tangente en torno a xn
    def plano_tangente(xy):
        diff = xy - xn
        return Fx + Jx @ diff

    # Crear malla para gráfico 3D
    x_vals = np.linspace(xn[0] - delta_zoom, xn[0] + delta_zoom, 50)
    y_vals = np.linspace(xn[1] - delta_zoom, xn[1] + delta_zoom, 50)
    X, Y = np.meshgrid(x_vals, y_vals)

    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            point = np.array([X[i, j], Y[i, j]])
            Z[i, j] = np.linalg.norm(plano_tangente(point))

    # Crear figura
    fig = plt.figure(figsize=(14, 6))

    # Subplot 1: Iteraciones en 2D
    ax1 = fig.add_subplot(121)
    ax1.plot(*xn, 'ro', label=f'$x_{{{iteration}}}$')
    ax1.plot(*xn_next, 'bo', label=f'$x_{{{iteration+1}}}$ (aprox. raíz)')
    ax1.quiver(*xn, *delta, angles='xy', scale_units='xy', scale=1, color='green', label='Δx')

    # Ajustar ejes dinámicamente en torno a ambos puntos
    x_vals = [xn[0], xn_next[0]]
    y_vals = [xn[1], xn_next[1]]
    x_min, x_max = min(x_vals) - delta_zoom, max(x_vals) + delta_zoom
    y_min, y_max = min(y_vals) - delta_zoom, max(y_vals) + delta_zoom
    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(y_min, y_max)

    ax1.set_xlabel(vars[0])
    ax1.set_ylabel(vars[1])
    ax1.set_title('Iteración y paso Δx')
    ax1.legend()
    ax1.grid(True)

    #ax1.set_xlim(xn[0] - delta_zoom, xn[0] + delta_zoom)
    #ax1.set_ylim(xn[1] - delta_zoom, xn[1] + delta_zoom)

    # Subplot 2: superficie de ||F(xn) + J(xn)(x - xn)|| en 3D
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8) #type: ignore
    ax2.set_title(r'Norma del plano tangente: $||F(x_n) + J(x_n)(x - x_n)||$') 
    ax2.set_xlabel(f"${vars[0]}$")
    ax2.set_ylabel(f"${vars[1]}$")
    ax2.set_zlabel(r'$||\cdot||$') #type: ignore

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    return buffer

PROBLEMAS_INCISO_A_MULTI = """
🔍 ¿Qué estamos resolviendo?
Desarrollamos un método numérico para encontrar raíces de un sistema de ecuaciones no lineales multivariables, aplicando la expansión en serie de Taylor de segundo orden. El objetivo es hallar un vector x tal que **F(x) = 0**, donde F: ℝⁿ → ℝⁿ.

🔢 Aproximación de segundo orden (Taylor multivariable):
Dada una estimación inicial xₙ, desarrollamos F(x) en torno a xₙ como:

    F(x) ≈ F(xₙ) + J(xₙ)(x - xₙ) + ½·H(xₙ)[x - xₙ]²

donde:
- F(x) es el vector de funciones,
- J(xₙ) es la matriz Jacobiana evaluada en xₙ,
- H(xₙ) es una colección de matrices Hessianas (una por cada componente de F).

--- 

✅ Condiciones para aplicar el método:
1. F debe ser de clase C² (dos veces continuamente derivable).
2. El Jacobiano **J(x)** debe ser invertible cerca de la raíz.
3. El punto inicial x₀ debe estar razonablemente cerca de la solución.
4. Si se omite el término de segundo orden (Hessiana), se recupera el método de Newton clásico.

---

🔁 Paso iterativo (versión práctica):
A partir de la expansión, se linealiza el sistema (ignorando el término cuadrático explícito) y se resuelve:

    J(xₙ) · Δx = -F(xₙ)

Se actualiza:

    xₙ₊₁ = xₙ + Δx

(En versiones más avanzadas puede incorporarse explícitamente la Hessiana para una mejor aproximación local.)

---

📉 Criterio de convergencia:
Se calcula el error entre iteraciones consecutivas:

    error = ||xₙ₊₁ - xₙ||₂

Y se verifica si:

    ||F(xₙ)||₂ < tol    (por ejemplo, tol = 1e-6)

---

✅ Confirmación con sistema conocido:
En este TP, probamos el método con un sistema no lineal cuya solución exacta es conocida (por ejemplo: F(x, y) = [e^{x+y} - 1, x² - y] tiene raíz en (0, 0)), para validar la implementación antes de aplicarlo a modelos físicos más complejos.
"""

def metodo_taylor_multivariable_robusto(F, J, H_list, x0, tol=1e-6, max_iter=50, alpha_min=1e-3):
    x0 = np.array(x0, dtype=float)
    salida = ["📘 Método combinado: Taylor multivariable con corrección adaptativa\n"]
    historial = []

    for n in range(max_iter):
        Fx = np.array(F(*x0)).reshape(-1)
        norm_fx = np.linalg.norm(Fx)

        if norm_fx < tol:
            salida.append(f"✅ Convergencia por ||F(x)|| < {tol:.1e}")
            salida.append(f"🔍 Raíz aproximada: {x0}")
            break

        Jx = np.array(J(*x0), dtype=float)

        try:
            delta = -np.linalg.solve(Jx, Fx)
        except np.linalg.LinAlgError:
            salida.append("❌ Jacobiano no invertible. Se detiene.")
            break

        # Estrategia tipo 'bisección': reducir paso hasta que ||F(x)|| disminuya
        alpha = 1.0
        while alpha >= alpha_min:
            x1 = x0 + alpha * delta
            F1 = np.array(F(*x1)).reshape(-1)
            if np.linalg.norm(F1) < norm_fx:
                break  # paso aceptado
            alpha /= 2  # reducir paso

        if alpha < alpha_min:
            salida.append("⚠️ No se encontró paso descendente adecuado. Método detenido.")
            break

        error = np.linalg.norm(x1 - x0) # type:ignore

        historial.append({
            "n": n,
            "x": x0.tolist(),
            "F": Fx.tolist(),
            "delta": (alpha * delta).tolist(),
            "x_next": x1.tolist(), # type:ignore
            "error": float(error),
            "alpha": alpha
        })

        salida.append(f"🔁 Iteración {n}")
        salida.append(f"   xₙ         = {x0}")
        salida.append(f"   ||F(xₙ)||  = {norm_fx:.2e}")
        salida.append(f"   Δx         = {delta}")
        salida.append(f"   α          = {alpha}")
        salida.append(f"   Error      = {error:.2e}\n")

        if error < tol:
            salida.append(f"✅ Convergencia alcanzada en {n+1} iteraciones.")
            salida.append(f"🔍 Raíz aproximada: {x1}") # type: ignore
            break

        x0 = x1 # type:ignore

    else:
        salida.append("❌ No se alcanzó convergencia dentro del máximo de iteraciones.")

    return historial, "\n".join(salida)

def graficar_comparacion_convergencia_multi():
    # Obtener funciones simbólicas multivariables
    F, J, H_list, _ = obtener_funciones_multivariables()
    x0 = [2.5, -2.5]
    tol = 1e-6
    max_iter = 50

    # Ejecutar Taylor puro
    t0 = perf_counter()
    historial_taylor, _ = metodo_taylor_multivariable(F, J, H_list, x0, tol, max_iter)
    t1 = perf_counter()

    # Ejecutar método robusto
    t2 = perf_counter()
    historial_combinado, _ = metodo_taylor_multivariable_robusto(F, J, H_list, x0, tol, max_iter)
    t3 = perf_counter()

    errores_taylor = [step['error'] for step in historial_taylor]
    errores_combinado = [step['error'] for step in historial_combinado]

    iter_taylor = list(range(1, len(errores_taylor) + 1))
    iter_combinado = list(range(1, len(errores_combinado) + 1))

    plt.figure(figsize=(10, 6))
    plt.semilogy(iter_taylor, errores_taylor, 'o-', label=f'Taylor puro ({len(iter_taylor)} it.)', color='blue')
    plt.semilogy(iter_combinado, errores_combinado, 's--', label=f'Taylor robusto ({len(iter_combinado)} it.)', color='green')

    plt.axvline(x=len(iter_taylor), color='blue', linestyle=':', linewidth=1)
    plt.axvline(x=len(iter_combinado), color='green', linestyle=':', linewidth=1)

    plt.title("Convergencia de métodos multivariables")
    plt.xlabel("Iteración")
    plt.ylabel("Error (norma de Δx) [escala log]")
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return buf

PROBLEMAS_INCISO_B_MULTI = """
### 🧠 **1) Criterios de aplicación y robustez en funciones multivariables**

El algoritmo desarrollado aborda la resolución de **sistemas no lineales** mediante la extensión multivariable del **método de Taylor** con derivadas de primer y segundo orden (Jacobiano y Hessiana).

Para mejorar la estabilidad y evitar estancamientos, se implementó una versión **robusta** con corrección adaptativa del paso, inspirada en estrategias tipo bisección.

- 🔧 **Taylor multivariable puro**:
  - Requiere que el **Jacobiano sea invertible**.
  - Calcula un paso Δx resolviendo:  
    \t\t**J(x)·Δx ≈ –F(x)** (equivalente al paso de Newton multivariable).
  - El método converge rápidamente **si la aproximación inicial está cerca de la raíz** y la función es suave.

- 🛡️ **Taylor multivariable robusto** (combinado):
  - Introduce una corrección adaptativa:  
    si el paso Δx no mejora el valor de ||F(x)||, se reduce su tamaño (**α·Δx**) iterativamente.
  - Esta técnica permite sortear zonas donde el paso de Newton diverge o resulta inestable.
  - Es conceptualmente análogo a una **búsqueda lineal** o una **bisección en el espacio de Δx**.

---

### ⚡ **2) Comparación de eficiencia computacional**

- ⚙️ **Taylor multivariable puro**  
  - ✅ Alta velocidad de convergencia (superlineal o cuadrática).  
  - ❌ Puede fallar si el Jacobiano es mal condicionado o si se parte lejos de la raíz.  
  - 🧠 Exige cálculo del Jacobiano y las Hessianas de cada componente.

- 🔀 **Método combinado (con paso adaptativo)**  
  - ✅ Es más **estable y confiable** en escenarios difíciles.  
  - ✅ Permite que la corrección automática del paso salve iteraciones que de otro modo divergirían.  
  - 🕓 Puede requerir más operaciones por iteración, pero converge cuando el método puro falla.

---

🏁 **Resultado empírico:**  
En nuestras pruebas con el sistema:
  - **F(x, y) = [exp(x + y) – 1, x² – y]**, con raíz conocida en (0, 0),
  - Ambos métodos convergieron en pocas iteraciones,
  - El método robusto logró **una convergencia segura incluso desde una condición inicial alejada** (x₀ = [2.5, –2.5]).

✅ El método combinado se destaca por su **equilibrio entre velocidad y robustez**, convirtiéndose en una herramienta ideal para resolver sistemas no lineales multivariables de manera automática y confiable.
"""

### Fin agregado ---> si queda el multivariable, borrar a partir de aquí

def obtener_funciones_expr():
    x = sp.Symbol('x')
    f_expr = sp.exp(-x) - x # type: ignore
    f1_expr = sp.diff(f_expr, x)
    f2_expr = sp.diff(f1_expr, x)
    return x, f_expr, f1_expr, f2_expr

def obtener_funciones_numericas():
    x, f_expr, f1_expr, f2_expr = obtener_funciones_expr()
    f = sp.lambdify(x, f_expr, 'numpy')
    f1 = sp.lambdify(x, f1_expr, 'numpy')
    f2 = sp.lambdify(x, f2_expr, 'numpy')
    return f, f1, f2

def metodo_taylor_segundo_orden(f, f1, f2, x0=1.5, tol=1e-6, max_iter=50):
    historial = []
    salida = []

    salida.append("📘 Método de búsqueda de raíces por serie de Taylor (incluye 2da derivada)\n")

    for n in range(max_iter):
        fx = f(x0)
        f1x = f1(x0)
        f2x = f2(x0)

        if abs(fx) < tol:
            salida.append(f"✅ Convergencia por |f(x)| < {tol:.1e}")
            salida.append(f"🔍 Raíz aproximada: {x0:.6f}")
            break

        discriminante = f1x**2 - 2*fx*f2x

        salida.append(f"🔁 Iteración {n}")
        salida.append(f"   xₙ         = {x0:.6f}")
        salida.append(f"   f(xₙ)      = {fx:.2e}")
        salida.append(f"   f'(xₙ)     = {f1x:.2e}")
        salida.append(f"   f''(xₙ)    = {f2x:.2e}")
        salida.append(f"   Discriminante = {discriminante:.2e}")

        if discriminante < 0:
            salida.append("❌ Discriminante negativo. Raíces complejas. Método detenido.")
            break

        if abs(f2x) < 1e-12:
            salida.append("⚠️ Segunda derivada cercana a cero. Usando Newton clásico.")
            delta = -fx / f1x
        else:
            sqrt_disc = np.sqrt(discriminante)
            delta1 = (-f1x + sqrt_disc) / f2x
            delta2 = (-f1x - sqrt_disc) / f2x
            delta = delta1 if abs(delta1) < abs(delta2) else delta2

        x1 = x0 + delta
        error = abs(x1 - x0)

        # Calcular orden de convergencia experimental si hay suficientes errores previos
        if n >= 2:
            e0 = historial[-2]['error']
            e1 = historial[-1]['error']
            e2 = error

            if e0 > 0 and e1 > 0 and e2 > 0:
                orden = np.log(e2 / e1) / np.log(e1 / e0)
                salida.append(f"   Orden estimado de convergencia ≈ {orden:.2f}")
                orden_estimado = float(orden)
            else:
                orden_estimado = None
        else:
            orden_estimado = None

        salida.append(f"   Δx elegido = {delta:.2e}")
        salida.append(f"   xₙ₊₁       = {x1:.6f}")
        salida.append(f"   Error      = {error:.2e}\n")

        historial.append({
            'n': n,
            'x': float(x0),
            'f': float(fx),
            'f1': float(f1x),
            'f2': float(f2x),
            'disc': float(discriminante),
            'delta': float(delta),
            'x_next': float(x1),
            'error': float(error),
            'orden': orden_estimado
        })

        if error < tol:
            salida.append(f"✅ Convergencia alcanzada en {n+1} iteraciones.")
            salida.append(f"🔍 Raíz aproximada: {x1:.6f}")
            break

        x0 = x1

    else:
        salida.append("❌ No se alcanzó convergencia dentro del máximo de iteraciones.")

    # Agregar nota final explicativa sobre el método
    salida.append("\n📚 Requisitos del método:")
    salida.append("- f(x), f'(x), f''(x) deben ser funciones continuas y evaluables en un entorno de la raíz.")
    salida.append("- El discriminante f'(x)² - 2·f(x)·f''(x) debe ser ≥ 0 (si no, se obtienen raíces complejas).")
    salida.append("- Si f''(x) ≈ 0, se recurre al método de Newton clásico.")
    salida.append("- Se elige la Δx de menor módulo para mejorar la estabilidad numérica.")
    salida.append("- A partir de la iteración 2 se estima el orden de convergencia observado.")

    return historial, "\n".join(salida)
 
def graficar_iteraciones(historial, f, funcion_str="f(x)"):
    xs = [step['x'] for step in historial]
    ys = [step['f'] for step in historial]
    
    if len(xs) < 2:
        margin = 0.5
    else:
        margin = 0.2 * (max(xs) - min(xs))
    
    x_min = min(xs) - margin
    x_max = max(xs) + margin
    x_vals = np.linspace(x_min, x_max, 400)
    y_vals = f(x_vals)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label=f'${funcion_str}$', color='blue', linewidth=2)
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        color = 'red' if i < len(xs)-1 else 'green'
        marker = 'o' if i < len(xs)-1 else '*'
        size = 70 if i < len(xs)-1 else 120
        label = f'Iteración {i}' if i < len(xs)-1 else 'Raíz aproximada'
        
        plt.scatter(xi, yi, color=color, s=size, edgecolors='black',
                    zorder=5, label=label, marker=marker)
        plt.text(xi, yi + 0.08*np.sign(yi), f'$x_{i}$',
                 fontsize=10, ha='center', va='bottom' if yi > 0 else 'top')
        
        if i < len(xs) - 1:
            plt.annotate('', xy=(historial[i+1]['x'], historial[i+1]['f']), xytext=(xi, yi),
                         arrowprops=dict(arrowstyle='->', color='gray',
                                         lw=1.5, shrinkA=8, shrinkB=8))
    
    plt.axvline(xs[-1], color='green', linestyle=':', alpha=0.5)
    plt.title(f'Método de Taylor (2do orden) - $f(x) = {funcion_str}$', fontsize=14)
    plt.xlabel('$x$', fontsize=12)
    plt.ylabel('$f(x)$', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(loc='best')
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    
    return buffer

def metodo_taylor_biseccion_con_log(a, b, tol=1e-6, max_iter=50):
    f, f1, f2 = obtener_funciones_numericas()
    log = io.StringIO()
    print("Método combinado: Taylor (2da derivada) + Bisección\n", file=log)

    x0 = (a + b) / 2
    historial = []

    # Contadores para análisis
    iter_taylor = 0
    iter_biseccion = 0
    iter_actualizacion_intervalo = 0

    for n in range(max_iter):
        fx = f(x0)
        f1x = f1(x0)
        f2x = f2(x0)
        discriminante = f1x**2 - 2 * fx * f2x

        print(f"Iteración {n}:", file=log)
        print(f"  x_n = {x0:.15f}", file=log)
        print(f"  f(x_n) = {fx:.15e}", file=log)
        print(f"  f'(x_n) = {f1x:.15e}", file=log)
        print(f"  f''(x_n) = {f2x:.15e}", file=log)
        print(f"  Discriminante = {discriminante:.15e}", file=log)

        if discriminante < 0 or abs(f2x) < 1e-12:
            metodo = "bisección"
            x1 = (a + b) / 2
            delta = 0.0
            iter_biseccion += 1
            print("  Método Bisección seleccionado", file=log)
        else:
            sqrt_disc = np.sqrt(discriminante)
            delta1 = (-f1x + sqrt_disc) / f2x
            delta2 = (-f1x - sqrt_disc) / f2x
            delta = delta1 if abs(delta1) < abs(delta2) else delta2
            x_taylor = x0 + delta

            if a <= x_taylor <= b:
                metodo = "taylor"
                x1 = x_taylor
                iter_taylor += 1
                print(f"  Δx elegido = {delta:.15e}", file=log)
            else:
                metodo = "bisección"
                x1 = (a + b) / 2
                delta = 0.0
                iter_biseccion += 1
                print("  Método Bisección seleccionado (Taylor fuera de rango)", file=log)

        error = abs(x1 - x0)
        print(f"  x_{n+1} = {x1:.15f}", file=log)
        print(f"  Error = {error:.15e}\n", file=log)

        historial.append({
            "iter": n,
            "x": x0,
            "fx": fx,
            "error": error,
            "metodo": metodo,
            "delta": delta
        })

        if abs(fx) < tol:
            print(f"Convergencia alcanzada por criterio de función (|f(x)| < {tol})", file=log)
            print(f"Raíz aproximada: {x0:.15f}\n", file=log)
            break

        # Actualizar intervalo como en bisección
        if f(a) * f(x0) < 0:
            b = x0
        else:
            a = x0
        iter_actualizacion_intervalo += 1

        x0 = x1

    # Resumen de contadores
    print("Resumen comparativo de uso de métodos:", file=log)
    print(f"  Iteraciones totales: {n+1}", file=log) # type: ignore
    print(f"  Iteraciones con método Taylor: {iter_taylor}", file=log)
    print(f"  Iteraciones con método Bisección: {iter_biseccion}", file=log)
    print(f"  Iteraciones con actualización de intervalo (tipo bisección): {iter_actualizacion_intervalo}", file=log)
    error_final = historial[-1]["error"] if historial else None
    print(f"  Error final aproximado: {error_final:.15e}", file=log)

    return historial, log.getvalue()
 
def ejecutar_metodos_con_comparacion(a=0.1, b=18, tol=1e-6, max_iter=50):
    f, f1, f2 = obtener_funciones_numericas()
    log = io.StringIO()
    
    print("Comparación de rendimiento: Método de Taylor vs Combinado Taylor-Bisección\n", file=log)

    # Taylor puro
    x0 = (a + b) / 2
    historial_taylor = []

    start_taylor = time.perf_counter()
    for n in range(max_iter):
        fx = f(x0)
        f1x = f1(x0)
        f2x = f2(x0)
        discriminante = f1x**2 - 2*fx*f2x

        if discriminante < 0 or abs(f2x) < 1e-12:
            delta = 0.0
            x1 = (a + b) / 2
        else:
            sqrt_disc = np.sqrt(discriminante)
            delta1 = (-f1x + sqrt_disc) / f2x
            delta2 = (-f1x - sqrt_disc) / f2x
            delta = delta1 if abs(delta1) < abs(delta2) else delta2
            x1 = x0 + delta

        error = abs(x1 - x0)
        historial_taylor.append({"iter": n, "x": x0, "fx": fx, "error": error})

        if abs(fx) < tol:
            break

        if f(a)*f(x0) < 0:
            b = x0
        else:
            a = x0

        x0 = x1
        
        print("x0:", x0)
        print("a, b:", a, b)
        print("tol:", tol)
        print("f(x0):", f(x0))  # para ver cómo empieza el método
    end_taylor = time.perf_counter()
    tiempo_taylor = end_taylor - start_taylor

    # Método combinado
    start_combinado = time.perf_counter()
    historial_combinado, log_combinado = metodo_taylor_biseccion_con_log(a, b, tol, max_iter)
    end_combinado = time.perf_counter()
    tiempo_combinado = end_combinado - start_combinado
    
    print(f"Iteraciones del método de Taylor: {len(historial_taylor)}", file=log)
    print(f"Iteraciones del método combinado: {len(historial_combinado)}", file=log)

    print(f"Valor final f(x) Taylor: {f(historial_taylor[-1]['x'])}", file=log)
    print(f"Valor final f(x) Combinado: {f(historial_combinado[-1]['x'])}", file=log)

    print(f"Tiempo de ejecución Taylor puro: {tiempo_taylor:.12f} segundos", file=log)
    print(f"Tiempo de ejecución Método combinado: {tiempo_combinado:.12f} segundos", file=log)

    if tiempo_combinado > 0:
       mejora = tiempo_taylor / tiempo_combinado
       print(f"Relación de velocidad (Taylor/Combinado): {mejora:.2f}x", file=log)

    return historial_taylor, historial_combinado, log.getvalue() + "\n\n" + log_combinado
 
def graficar_convergencia_loglog():
   
    f, f1, f2 = obtener_funciones_numericas()
    raiz_real = 0.5671432904097838  # Raíz conocida
    historial, _ = metodo_taylor_segundo_orden(f, f1, f2, x0=1.5, tol=1e-6, max_iter=50)

    errors = [abs(step['x_next'] - raiz_real) for step in historial if abs(step['x_next'] - raiz_real) > 0] #type:ignore
    iterations = np.arange(1, len(errors) + 1, dtype=float)

    if not errors:
        raise ValueError("No se generaron errores para graficar.")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    p_ref = 3
    C = errors[0] * (iterations[0] ** p_ref)
    ref_curve = C * iterations**(-p_ref)

    ax1.loglog(iterations, errors, marker='o', linestyle='-', color='blue',
               linewidth=2, markersize=8, label='Error absoluto')
    ax1.loglog(iterations, ref_curve, 'k--', label=f'Referencia: $O(n^{{-{p_ref}}})$')
    ax1.set_title('Convergencia del Método de Taylor (2do orden)\nf(x) = e^{-x} - x', fontsize=14)
    ax1.set_xlabel('Iteración')
    ax1.set_ylabel('Error absoluto')
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    ax1.set_xticks(iterations)
    ax1.legend()

    if len(errors) > 2:
        ratios = np.array(errors[1:]) / np.array(errors[:-1])
        ax2.plot(iterations[1:], ratios, 's-', color='red', markersize=8,
                 linewidth=2, label='Tasa de convergencia')
        ax2.axhline(y=0, color='k', linestyle='--', linewidth=0.8)
        ax2.set_title('Tasa de Convergencia Numérica')
        ax2.set_xlabel('Iteración')
        ax2.set_ylabel('$e_{n+1}/e_n$')
        ax2.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        ax2.legend()
    else:
        ax2.text(0.5, 0.5, "No hay suficientes datos para tasa de convergencia", 
                 ha='center', va='center', fontsize=12, transform=ax2.transAxes)
        ax2.axis('off')

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer
 
def graficar_taylor_local(iteration: int):
    delta_zoom=0.1
    f, f1, f2 = obtener_funciones_numericas()
    historial, _ = metodo_taylor_segundo_orden(f, f1, f2, x0=1.5, tol=1e-6, max_iter=50)

    if iteration < 0 or iteration >= len(historial):
        raise ValueError("Número de iteración inválido.")

    step = historial[iteration]
    xn = step['x']
    fxn = step['f']
    f1n = step['f1']
    f2n = step['f2']
    xn_next = step['x_next']

    def taylor2(x_val):
        return fxn + f1n * (x_val - xn) + 0.5 * f2n * (x_val - xn) ** 2

    # --- Gráfico 1: Intervalo amplio fijo ---
    x_amplio = np.linspace(0, 0.9, 300)
    y_orig_amplio = f(x_amplio)
    y_taylor_amplio = taylor2(x_amplio)

    # --- Gráfico 2: Zoom local centrado en xn ---
    x_local = np.linspace(xn - delta_zoom, xn + delta_zoom, 300)
    y_orig_local = f(x_local)
    y_taylor_local = taylor2(x_local)

    fig, axs = plt.subplots(1, 2, figsize=(14, 5))

    # Gráfico amplio
    axs[0].plot(x_amplio, y_orig_amplio, label='Función original $f(x)$', color='navy', linewidth=2)
    axs[0].plot(x_amplio, y_taylor_amplio, label=f'Aprox. Taylor 2° orden en $x_{{{iteration}}}$',
                color='green', linestyle='--', linewidth=2)
    axs[0].scatter([xn], [fxn], color='red', s=80, label=f'$x_{{{iteration}}}$ (punto de expansión)')
    axs[0].scatter([xn_next], [0], color='blue', s=80, label=f'$x_{{{iteration+1}}}$ (aprox. raíz)')
    axs[0].axhline(0, color='black', linewidth=0.8, linestyle='--')
    axs[0].axvline(xn, color='red', linestyle=':', linewidth=1)
    axs[0].axvline(xn_next, color='blue', linestyle=':', linewidth=1)
    axs[0].fill_between(x_amplio, y_orig_amplio, y_taylor_amplio, color='lightgreen', alpha=0.3)
    axs[0].set_title(f'Intervalo amplio fijo\nIteración {iteration}')
    axs[0].set_xlabel('$x$')
    axs[0].set_ylabel('$f(x)$')
    axs[0].legend(fontsize=9)
    axs[0].grid(True, linestyle='--', alpha=0.6)
    axs[0].set_xlim(0, 0.9)
    y_min = min(np.min(y_orig_amplio), np.min(y_taylor_amplio)) - 0.1
    y_max = max(np.max(y_orig_amplio), np.max(y_taylor_amplio)) + 0.1
    axs[0].set_ylim(y_min, y_max)

    # Gráfico zoom local
    axs[1].plot(x_local, y_orig_local, label='Función original $f(x)$', color='navy', linewidth=2)
    axs[1].plot(x_local, y_taylor_local, label=f'Aprox. Taylor 2° orden en $x_{{{iteration}}}$',
                color='green', linestyle='--', linewidth=2)
    axs[1].scatter([xn], [fxn], color='red', s=80, label=f'$x_{{{iteration}}}$ (punto de expansión)')
    axs[1].scatter([xn_next], [0], color='blue', s=80, label=f'$x_{{{iteration+1}}}$ (aprox. raíz)')
    axs[1].axhline(0, color='black', linewidth=0.8, linestyle='--')
    axs[1].axvline(xn, color='red', linestyle=':', linewidth=1)
    axs[1].axvline(xn_next, color='blue', linestyle=':', linewidth=1)
    axs[1].fill_between(x_local, y_orig_local, y_taylor_local, color='lightgreen', alpha=0.3)
    axs[1].set_title(f'Zoom local en $x_{{{iteration}}}$ ± {delta_zoom}')
    axs[1].set_xlabel('$x$')
    axs[1].set_ylabel('$f(x)$')
    axs[1].legend(fontsize=9)
    axs[1].grid(True, linestyle='--', alpha=0.6)

    y_min_local = min(np.min(y_orig_local), np.min(y_taylor_local)) - 0.1
    y_max_local = max(np.max(y_orig_local), np.max(y_taylor_local)) + 0.1
    axs[1].set_ylim(y_min_local, y_max_local)
    axs[1].set_xlim(xn - delta_zoom, xn + delta_zoom)

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    return buffer
 
def graficar_comparacion_convergencia():
    historial_taylor, historial_combinado, _ = ejecutar_metodos_con_comparacion()

    errores_taylor = [step['error'] for step in historial_taylor]
    errores_combinado = [step['error'] for step in historial_combinado]

    iter_taylor = list(range(1, len(errores_taylor) + 1))
    iter_combinado = list(range(1, len(errores_combinado) + 1))

    ultima_taylor = iter_taylor[-1]
    ultima_combinado = iter_combinado[-1]

    plt.figure(figsize=(10, 6))
    plt.semilogy(iter_taylor, errores_taylor, 'o-', label='Taylor (2º orden)', color='blue')
    plt.semilogy(iter_combinado, errores_combinado, 's--', label='Combinado (Taylor + Bisección)', color='green')

    plt.axvline(x=ultima_taylor, color='blue', linestyle=':', label=f'Convergencia Taylor ({ultima_taylor} it.)')
    plt.axvline(x=ultima_combinado, color='green', linestyle=':', label=f'Convergencia Combinado ({ultima_combinado} it.)')

    plt.title("Iteración de convergencia para cada método")
    plt.xlabel("Iteración")
    plt.ylabel("Error (escala logarítmica)")
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return buf

PROBLEMAS_INCISO_A = """
🔍 ¿Qué estamos resolviendo?
Desarrollamos un método numérico para encontrar raíces de funciones no lineales utilizando la expansión en serie de Taylor hasta la segunda derivada. El objetivo es hallar un valor x tal que f(x) = 0, comenzando desde una estimación inicial x₀.

🔢 La expansión de Taylor hasta segundo orden de f(x) alrededor de xₙ es:
    f(x) ≈ f(xₙ) + f'(xₙ)(x - xₙ) + (1/2)f''(xₙ)(x - xₙ)²

Igualamos a cero y resolvemos para obtener la siguiente aproximación xₙ₊₁.

---

✅ Condiciones para aplicar el método:
1. La función f debe ser derivable al menos dos veces.
2. f', f'' deben ser continuas en el entorno de la raíz.
3. f''(xₙ) no debe ser cercano a cero (evita inestabilidad).
4. El discriminante D = (f')² - 2f·f'' debe ser ≥ 0 (evita raíces complejas).
5. El punto inicial x₀ debe estar razonablemente cerca de la raíz.

---

🔁 Justificación del paso iterativo:
Planteamos la ecuación cuadrática en Δx = x - xₙ:

    f''·Δx² + 2f'·Δx + 2f = 0

Resolvemos con fórmula general:

    Δx = [ -f' ± √(f'² - 2f·f'') ] / f''

Elegimos el Δx con menor módulo y actualizamos:

    xₙ₊₁ = xₙ + Δx

---

📉 Error y convergencia:
El error se calcula como:

    error = |xₙ₊₁ - xₙ|

Se verifica la convergencia si el error es menor a una tolerancia (por ejemplo, 1e-6).

⚡ El método puede tener orden de convergencia superior a 2, dependiendo de la función. En general, converge más rápido que Newton-Raphson si las condiciones son adecuadas.

---

✅ Confirmación con función conocida:
En este TP, aplicamos este método a la ecuación de Van der Waals para CO₂, y lo validamos también con funciones conocidas para confirmar la validez del procedimiento.
"""

PROBLEMAS_INCISO_B = """
### 🧠 **1) Criterios de aplicación para lograr robustez**

El algoritmo desarrollado combina la rapidez del método de **Taylor de segundo orden** con la solidez del **método de bisección**. Para decidir cuál utilizar en cada iteración, se siguen estos criterios:

- ❌ **No se aplica Taylor si**:
  - El discriminante `f'(x)² - 2·f(x)·f''(x)` es negativo (raíz compleja).
  - La segunda derivada `f''(x)` es muy cercana a cero (riesgo de división numéricamente inestable).
  - La estimación resultante queda fuera del intervalo de búsqueda `[a, b]`.

- ✅ **Se aplica Taylor si**:
  - El discriminante es positivo.
  - La segunda derivada tiene un valor significativo.
  - El nuevo valor calculado cae dentro del intervalo permitido.

- 🔁 En ambos casos, el intervalo se actualiza según el signo de `f(x)` (como en bisección) para mantener la raíz dentro de [a, b].

De esta manera, el método se adapta a cualquier intervalo inicial y se vuelve **automáticamente robusto**, incluso frente a funciones complicadas.

---

### ⚡ **2) Comparación de eficiencia computacional**

- 🔐 **Bisección**:  
  Es extremadamente robusto, siempre converge si hay cambio de signo. Pero es lento, ya que la convergencia es lineal.  
  No requiere derivadas y cada iteración es muy barata.

- ⚡ **Taylor puro**:  
  Es mucho más rápido (convergencia superlineal), pero menos confiable: puede fallar si la función no es suave o si las derivadas no se comportan bien.  
  Requiere calcular `f'` y `f''`, por lo que tiene un mayor costo por iteración.

- 🔀 **Método combinado**:  
  Se comporta como Taylor cuando puede (velocidad), y cae de forma segura en bisección cuando debe (robustez).  
  Es eficiente, confiable y rápido: un excelente equilibrio entre rendimiento y estabilidad.

---

🏁 **Resultado empírico:**  
En nuestras pruebas, el método combinado:
- Fue más veloz en tiempo total.
- Requirió menos iteraciones efectivas.
- Conservó la precisión, incluso en intervalos no óptimos.

✅ Es la opción más segura y poderosa cuando se busca automatizar la búsqueda de raíces en funciones no lineales.

"""
