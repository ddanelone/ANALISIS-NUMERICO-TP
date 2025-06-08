import io
import base64
import matplotlib.pyplot as plt
import numpy as np
from services.utils import eval_func

def generar_grafico_newton_base64(params, resultado):
    f = eval_func(params.funcion)
    x_vals = np.linspace(params.x0 - 5, params.x0 + 5, 400)
    y_vals = [f(x) for x in x_vals]

    plt.figure(figsize=(8, 4))
    plt.plot(x_vals, y_vals, label=f"f(x) = {params.funcion}")
    plt.axhline(0, color="gray", linestyle="--")
    plt.scatter(resultado["raiz"], f(resultado["raiz"]),
                color="red", label=f"Raíz: {resultado['raiz']:.4f}")
    plt.legend()
    plt.title("Método de Newton Modificado")
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def generar_grafico_combinado_base64(f, params, biseccion_iters, taylor_iters):
    xs = np.linspace(params.a, params.b, 200)
    ys = [f(xi) for xi in xs]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs, ys, label='Función f(x)')
    ax.axhline(0, color='black', linewidth=0.8)

    bisecc_x = [it[1] for it in biseccion_iters]
    bisecc_y = [it[2] for it in biseccion_iters]
    ax.scatter(bisecc_x, bisecc_y, color='red', label='Iteraciones Bisección')

    taylor_x = [it[1] for it in taylor_iters]
    taylor_y = [it[2] for it in taylor_iters]
    ax.scatter(taylor_x, taylor_y, color='blue', label='Iteraciones Taylor')

    ax.legend()
    ax.set_title('Comparación Métodos Bisección y Taylor')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
