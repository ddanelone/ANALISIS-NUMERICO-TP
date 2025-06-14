import sympy as sp
import numpy as np

# Definición simbólica
x = sp.Symbol('x')

# EJEMPLO: función conocida con raíz (cambiá esto si querés otra)
f_expr = x**3 - x - 2

# Derivadas
f1_expr = sp.diff(f_expr, x)
f2_expr = sp.diff(f1_expr, x)

# Conversión a funciones numéricas
f = sp.lambdify(x, f_expr, 'numpy')
f1 = sp.lambdify(x, f1_expr, 'numpy')
f2 = sp.lambdify(x, f2_expr, 'numpy')

def metodo_taylor_segundo_orden(x0, tol=1e-6, max_iter=50):
    historial = []  # Al principio del método 
    print("Método de búsqueda de raíces por serie de Taylor (2da derivada incluida)\n")
    for n in range(max_iter):
        fx = f(x0)
        f1x = f1(x0)
        f2x = f2(x0)
        
        discriminante = f1x**2 - 2*fx*f2x
        
        print(f"Iteración {n}:")
        print(f"  x_n = {x0}")
        print(f"  f(x_n) = {fx}")
        print(f"  f'(x_n) = {f1x}")
        print(f"  f''(x_n) = {f2x}")
        print(f"  Discriminante = {discriminante}")
        
        if discriminante < 0:
            print("  ¡Discriminante negativo! Raíces complejas. Se detiene el método.")
            return None
        
        sqrt_disc = np.sqrt(discriminante)
        delta1 = (-f1x + sqrt_disc) / f2x
        delta2 = (-f1x - sqrt_disc) / f2x
        
        # Elegimos la que tenga menor módulo
        delta = delta1 if abs(delta1) < abs(delta2) else delta2
        x1 = x0 + delta
        
        error = abs(x1 - x0)
        print(f"  Δx elegido = {delta}")
        print(f"  x_{n+1} = {x1}")
        print(f"  Error = {error}\n")
        
        if error < tol:
            print(f"Convergencia alcanzada en {n+1} iteraciones. Raíz aproximada: {x1}")
            return x1
        
        x0 = x1
        
        historial.append({
            'n': n,
            'x': x0,
            'f': fx,
            'f1': f1x,
            'f2': f2x,
            'disc': discriminante,
            'delta': delta,
            'x_next': x1,
            'error': error
        })
    
    print("No se alcanzó la convergencia en el número máximo de iteraciones.")
    return None

# Ejecutamos el método con un valor inicial cercano a la raíz real (~1.5)
metodo_taylor_segundo_orden(x0=1.5)
