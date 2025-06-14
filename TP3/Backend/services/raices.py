import sympy as sp
import numpy as np
import io
import matplotlib
matplotlib.use('Agg')  # Evita problemas con backends gráficos
import matplotlib.pyplot as plt
import time

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
    log = io.StringIO()

    print("Método de búsqueda de raíces por serie de Taylor (2da derivada incluida)\n", file=log)

    for n in range(max_iter):
        fx = f(x0)
        f1x = f1(x0)
        f2x = f2(x0)

        if abs(fx) < tol:
            print(f"Convergencia alcanzada por criterio de función (|f(x)| < {tol})", file=log)
            print(f"Raíz aproximada: {x0}", file=log)
            break

        discriminante = f1x**2 - 2*fx*f2x

        print(f"Iteración {n}:", file=log)
        print(f"  x_n = {x0}", file=log)
        print(f"  f(x_n) = {fx}", file=log)
        print(f"  f'(x_n) = {f1x}", file=log)
        print(f"  f''(x_n) = {f2x}", file=log)
        print(f"  Discriminante = {discriminante}", file=log)

        if discriminante < 0:
            print("  ¡Discriminante negativo! Raíces complejas. Se detiene el método.", file=log)
            break

        if abs(f2x) < 1e-12:
            print("  ¡Segunda derivada cercana a cero! Revertiendo a método de Newton.", file=log)
            delta = -fx / f1x
        else:
            sqrt_disc = np.sqrt(discriminante)
            delta1 = (-f1x + sqrt_disc) / f2x
            delta2 = (-f1x - sqrt_disc) / f2x
            delta = delta1 if abs(delta1) < abs(delta2) else delta2

        x1 = x0 + delta
        error = abs(x1 - x0)

        print(f"  Δx elegido = {delta}", file=log)
        print(f"  x_{n+1} = {x1}", file=log)
        print(f"  Error = {error}\n", file=log)

        historial.append({
            'n': n,
            'x': float(x0),
            'f': float(fx),
            'f1': float(f1x),
            'f2': float(f2x),
            'disc': float(discriminante),
            'delta': float(delta),
            'x_next': float(x1),
            'error': float(error)
        })

        if error < tol:
            print(f"Convergencia alcanzada en {n+1} iteraciones. Raíz aproximada: {x1}", file=log)
            break

        x0 = x1

    return historial, log.getvalue()

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

    # Contadores para el análisis comparativo
    iter_taylor = 0
    iter_biseccion = 0

    for n in range(max_iter):
        fx = f(x0)
        f1x = f1(x0)
        f2x = f2(x0)
        discriminante = f1x**2 - 2*fx*f2x

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

        # Actualizar intervalo para bisección
        if f(a)*f(x0) < 0:
            b = x0
        else:
            a = x0

        x0 = x1

    # Al final, agregar el resumen comparativo al log:
    print("Resumen comparativo de uso de métodos:", file=log)
    print(f"  Iteraciones totales: {n+1}", file=log)                        # type: ignore
    print(f"  Iteraciones con método Taylor: {iter_taylor}", file=log)
    print(f"  Iteraciones con método Bisección: {iter_biseccion}", file=log)

    # También podemos agregar estadísticas adicionales si quieres, por ejemplo el error final
    error_final = historial[-1]["error"] if historial else None
    print(f"  Error final aproximado: {error_final:.15e}", file=log)

    return historial, log.getvalue()
 
def ejecutar_metodos_con_comparacion(a=0, b=2, tol=1e-6, max_iter=50):
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
    
    print("Iteraciones Taylor:", len(historial_taylor))
    print("Iteraciones Combinado:", len(historial_combinado))


    # Comparación
    print(f"Tiempo de ejecución Taylor puro: {tiempo_taylor:.12f} segundos", file=log)
    print(f"Tiempo de ejecución Método combinado: {tiempo_combinado:.12f} segundos\n", file=log)

    if tiempo_combinado > 0:
        mejora = tiempo_taylor / tiempo_combinado
        print(f"Relación de velocidad (Taylor/Combinado): {mejora:.2f}x", file=log)

    return historial_taylor, historial_combinado, log.getvalue() + "\n\n" + log_combinado
 
def graficar_convergencia_loglog():
    f, f1, f2 = obtener_funciones_numericas()
    raiz_real = 0.5671432904097838  # Raíz conocida
    historial, _ = metodo_taylor_segundo_orden(f, f1, f2, x0=1.5, tol=1e-6, max_iter=50)

    errors = [abs(step['x_next'] - raiz_real) for step in historial if abs(step['x_next'] - raiz_real) > 0]
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

    x_local = np.linspace(0, 0.9, 300)

    def taylor2(x_val):
        return fxn + f1n * (x_val - xn) + 0.5 * f2n * (x_val - xn)**2

    y_original = f(x_local)
    y_taylor = taylor2(x_local)

    plt.figure(figsize=(8, 5))
    plt.plot(x_local, y_original, label='Función original $f(x)$', color='navy', linewidth=2)
    plt.plot(x_local, y_taylor, label=f'Aprox. Taylor 2° orden en $x_{{{iteration}}}$',
             color='green', linestyle='--', linewidth=2)
    plt.scatter([xn], [fxn], color='red', s=80, label=f'$x_{{{iteration}}}$ (punto de expansión)')
    plt.scatter([xn_next], [0], color='blue', s=80, label=f'$x_{{{iteration+1}}}$ (aprox. raíz)')
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(xn, color='red', linestyle=':', linewidth=1)
    plt.axvline(xn_next, color='blue', linestyle=':', linewidth=1)
    plt.fill_between(x_local, y_original, y_taylor, color='lightgreen', alpha=0.3)

    plt.title(f'Aproximación local con Serie de Taylor 2° orden\nIteración {iteration}', fontsize=14)
    plt.xlabel('$x$', fontsize=12)
    plt.ylabel('$f(x)$', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xlim(0, 0.9)

    y_min = min(np.min(y_original), np.min(y_taylor)) - 0.1
    y_max = max(np.max(y_original), np.max(y_taylor)) + 0.1
    plt.ylim(y_min, y_max)

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
