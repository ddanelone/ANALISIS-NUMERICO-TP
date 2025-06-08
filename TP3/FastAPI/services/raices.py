from typing import Dict, Any, Callable, Tuple, List
import math
import numpy as np
from sympy import sympify, symbols
from services.utils import eval_func
from services.graficos import (
    generar_grafico_newton_base64,
    generar_grafico_combinado_base64,
)

def newton_modificado(funcion, derivada, segunda_derivada, x0, tolerancia, max_iter):
    f = eval_func(funcion)
    f_prime = eval_func(derivada)
    f_double_prime = eval_func(segunda_derivada)

    x_n = x0
    errores = []
    ordenes = []
    x_prev = None
    i = 0  # Inicializo i

    for i in range(max_iter):
        fx = f(x_n)
        fpx = f_prime(x_n)
        fppx = f_double_prime(x_n)

        denom = fpx**2 - fx * fppx
        if denom == 0:
            break

        x_next = x_n - (fx * fpx) / denom

        if x_prev is not None:
            e_n = abs(x_n - x_prev)
            errores.append(e_n)
            if len(errores) > 1 and errores[-2] != 0:
                p = np.log(errores[-1]) / np.log(errores[-2])
                ordenes.append(p)

        if abs(x_next - x_n) < tolerancia:
            x_n = x_next
            break

        x_prev = x_n
        x_n = x_next

    resultado = {
        "raiz": x_n,
        "iteraciones": i + 1,
        "error_final": abs(x_n - x_prev) if x_prev is not None else None,
        "errores": errores,
        "orden_convergencia": ordenes
    }

    return resultado

def metodo_biseccion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float,
    max_iter: int
) -> Tuple[List[Tuple[int, float, float]], float]:
    iter_data = []
    fa = f(a)
    fb = f(b)
    
    if fa * fb > 0:
        raise ValueError("La función no cambia de signo en el intervalo [a,b]")
    
    c = (a + b) / 2
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        iter_data.append((i, c, fc))
        
        if abs(fc) < tol or (b - a) / 2 < tol:
            break
            
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
            
    return iter_data, c

def metodo_taylor_segunda(
    f: Callable[[float], float],
    f1: Callable[[float], float],
    f2: Callable[[float], float],
    x0: float,
    tol: float,
    max_iter: int
) -> Tuple[List[Tuple[int, float, float]], float]:
    iter_data = []
    x_old = x0
    x_new = x0
    
    for i in range(max_iter):
        fx = f(x_old)
        f1x = f1(x_old)
        f2x = f2(x_old)

        a_quad = 0.5 * f2x
        b_quad = f1x
        c_quad = fx

        discriminante = b_quad**2 - 4*a_quad*c_quad
        if discriminante < 0:
            break
            
        sqrt_disc = np.sqrt(discriminante)
        h1 = (-b_quad + sqrt_disc) / (2 * a_quad) if a_quad != 0 else -c_quad / b_quad
        h2 = (-b_quad - sqrt_disc) / (2 * a_quad) if a_quad != 0 else -c_quad / b_quad

        h_candidates = [h for h in [h1, h2] if np.isreal(h)]
        if not h_candidates:
            break
            
        h = min(h_candidates, key=lambda x: abs(x))
        x_new = x_old + h.real
        iter_data.append((i, x_new, f(x_new)))

        if abs(x_new - x_old) < tol:
            break
            
        x_old = x_new
        
    return iter_data, x_new

def metodo_combinado(params):
    f = eval_func(params.funcion)
    a, b = params.a, params.b
    tol = params.tolerancia
    max_iter = params.max_iter

    c = (a + b) / 2  # inicializo c
    iter_biseccion = []
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        iter_biseccion.append((i, c, fc))
        if abs(fc) < tol or (b - a) / 2 < tol:
            break
        if f(a) * fc < 0:
            b = c
        else:
            a = c

    derivada = params.derivada
    segunda_derivada = params.segunda_derivada
    f_prime = eval_func(derivada)
    if abs(f_prime(c)) > 1e-6:
        resultado_newton = newton_modificado(
            params.funcion,
            params.derivada,
            params.segunda_derivada,
            c,
            tol,
            max_iter
        )
        # Iteraciones de Taylor con estructura más completa
        iter_taylor = [{"iter": i, "x": x, "fx": f(x)} for i, (x, _) in enumerate(zip(resultado_newton.get("errores", []), resultado_newton.get("errores", [])))]
    else:
        resultado_newton = {}
        iter_taylor = []

    resultado = {
        "raiz": resultado_newton.get("raiz", c),
        "iter_biseccion": iter_biseccion,
        "iter_taylor": iter_taylor,
        "error_final": resultado_newton.get("error_final", None),
        "orden_convergencia": resultado_newton.get("orden_convergencia", [])
    }

    # Generar el gráfico base64
    grafico_base64 = generar_grafico_combinado_base64(f, params, iter_biseccion, iter_taylor)
    resultado["grafico_base64"] = grafico_base64

    return resultado

