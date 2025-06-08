import matplotlib.pyplot as plt
import numpy as np
import io

def generar_saludo(nombre: str) -> str:
    return f"Hola, {nombre} este es un backend funcional en Python"

def generar_grafico_exponencial():
    x = np.linspace(0, 5, 100)
    y = np.exp(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, label="e^x", color="blue")
    ax.set_title("Gráfico de $e^x$")
    ax.set_xlabel("x")
    ax.set_ylabel("e^x")
    ax.grid(True)
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf
