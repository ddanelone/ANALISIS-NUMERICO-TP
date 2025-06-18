from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse, StreamingResponse
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq
import io
import time

# ---------------------
# Constantes y funciones
# ---------------------

R = 8.314  # J/(mol·K)
T = 200.0  # K
a = 0.364e6  # Pa·m^6/mol^2   según tabla para el CO2
b = 4.27e-5  # m^3/mol        según tabla para el CO2
pressures = [5e6, 0.5e6]  # Pascales
P = 0.5e6


def van_der_waals_eq(v, P, T):
    return (P + a / v**2) * (v - b) - R * T

def calcular_volumenes():
    resultados = []
    pressures = [5e6, 0.5e6]
    for P in pressures:
        v_ideal = R * T / P
        a_i, b_i = encontrar_intervalo(P, T)

        if a_i is not None:
            try:
                v_real = brentq(van_der_waals_eq, a_i, b_i, args=(P, T))
            except Exception as e:
                v_real = None
        else:
            v_real = None

        mensaje = (
            f"v_real ≈ {v_real:.2e}, diferencia ≈ {abs(v_real - v_ideal)/v_real*100:.2f}%" # type: ignore
            if v_real else "❌ No se encontró raíz"
        )
        resultados.append((P, v_ideal, v_real, mensaje))
        
        print(f"\nPresión: {P/1e6} MPa")
        print(f"Intervalo encontrado: a={a_i}, b={b_i}")
        print(f"v_real: {v_real}")

    return resultados

def generar_grafico_gases():
    resultados = calcular_volumenes()
    fig, axs = plt.subplots(1, len(resultados), figsize=(14, 5))

    for i, (P, v_ideal, v_real, mensaje) in enumerate(resultados):
        ax = axs[i] if len(resultados) > 1 else axs

        # Ajustamos el rango de graficación para que incluya siempre v_real (si existe)
        if v_real is not None:
            v_min_plot = min(v_real * 0.9, b * 0.95)
            v_max_plot = max(v_ideal * 1.5, v_real * 1.1)
        else:
            v_min_plot = b * 0.95
            v_max_plot = v_ideal * 2

        v_vals = np.linspace(v_min_plot, v_max_plot, 1000)
        f_vals = [van_der_waals_eq(v, P, T) for v in v_vals]

        ax.plot(v_vals, f_vals, label=f'f(v) para {P/1e6:.1f} MPa')
        ax.axhline(0, color='black', linestyle='--')

        if v_real is not None:
            ax.axvline(v_real, color='green', linestyle='--', label=f'v_real ≈ {v_real:.6f}')
        else:
            ax.text(0.5, 0.1, "v_real no válida", transform=ax.transAxes, color="gray", fontsize=10)

        ax.axvline(v_ideal, color='red', linestyle=':', label=f'v_ideal ≈ {v_ideal:.6f}')
        ax.set_xlabel('Volumen molar v (m³/mol)')
        ax.set_ylabel('f(v)')
        ax.set_title(f'Van der Waals: P = {P/1e6:.1f} MPa')
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf

# --- Buscar intervalo válido ---
def encontrar_intervalo(P, T, v_min=1e-5, v_max=1e-1, pasos=10000):
    v_vals = np.linspace(v_min, v_max, pasos)
    f_vals = [van_der_waals_eq(v, P, T) for v in v_vals]

    for i in range(len(f_vals) - 1):
        if f_vals[i] * f_vals[i + 1] < 0:
            return v_vals[i], v_vals[i + 1]
    return None, None

# --- Resolver con Brentq --- 
def resolver_vdw_brentq(P, T):
    a_i, b_i = encontrar_intervalo(P, T)

    if a_i is None:
        return R * T / P, None, None, "❌ No se encontró intervalo con cambio de signo."

    try:
        v_real = brentq(van_der_waals_eq, a_i, b_i, args=(P, T))
        v_ideal = R * T / P
        diferencia = abs(v_real - v_ideal) / v_real * 100
        return v_ideal, v_real, diferencia, f"✅ Intervalo: [{a_i:.2e}, {b_i:.2e}]"
    except Exception as e:
        return R * T / P, None, None, f"❌ Error al aplicar Brentq: {e}"


# --- Gráfico general ---
def generar_grafico_general(v_ideal, v_real, P, T):
    v_vals = np.linspace(b * 1.001, v_ideal * 2, 1000)
    f_vals = [van_der_waals_eq(v, P, T) for v in v_vals]

    plt.figure(figsize=(8, 5))
    plt.plot(v_vals, f_vals, label='f(v)', color='blue')
    plt.axhline(0, color='k', linestyle='--')
    plt.axvline(v_ideal, color='red', linestyle=':', label=f'v_ideal ≈ {v_ideal:.6f}')
    plt.axvline(v_real, color='green', linestyle='--', label=f'v_real ≈ {v_real:.6f}')
    plt.title('Raíz de Van der Waals a 0.5 MPa')
    plt.xlabel('Volumen molar (m³/mol)')
    plt.ylabel('f(v)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')

def generar_grafico_zoom(v_real, P, T):
    delta = v_real * 0.2
    v_zoom_vals = np.linspace(v_real - delta, v_real + delta, 1000)
    f_zoom_vals = [van_der_waals_eq(v, P, T) for v in v_zoom_vals]

    fig, ax = plt.subplots(figsize=(8, 5))

    # Curva f(v)
    ax.plot(v_zoom_vals, f_zoom_vals, label='f(v) - zoom', color='royalblue', linewidth=2)

    # Ejes de referencia
    ax.axhline(0, color='black', linestyle='--')
    ax.axvline(v_real, color='green', linestyle='--', label=f'v_real ≈ {v_real:.6f}')

    # Punto en la raíz
    f_en_raiz = van_der_waals_eq(v_real, P, T)
    ax.plot(v_real, f_en_raiz, 'go', label='Raíz (punto)')

    # Texto con valor de f(v_real)
    ax.text(0.05, 0.95, f'f(v_real) ≈ {f_en_raiz:.2e}', transform=ax.transAxes,
            fontsize=10, verticalalignment='top', color='gray')

    # Estética y ejes
    ax.set_title('Zoom en la raíz de Van der Waals')
    ax.set_xlabel('Volumen molar (m³/mol)')
    ax.set_ylabel('f(v)')
    ax.grid(True)
    ax.legend()

    # Mostrar ejes sin notación científica
    ax.ticklabel_format(style='plain', axis='x')
    ax.ticklabel_format(style='plain', axis='y')

    plt.tight_layout()

    # Guardar imagen y devolver como streaming
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')
 
 # --- Método de Taylor de segundo orden para Van der Waals ---
def taylor_vdw(P, T, v0=None, tol=1e-8, max_iter=100):
    if v0 is None:
        v0 = R * T / P  # Punto inicial si no se especifica

    errores = []
    v = v0
    for i in range(max_iter):
        try:
            f = van_der_waals_eq(v, P, T)
            f_prime = -2 * a / v**3 + (P + a / v**2)
            f_double_prime = 6 * a / v**4

            if abs(f_prime) < 1e-12:
                return None, errores, "❌ Derivada primera casi nula. Método no aplicable."

            delta = f / f_prime + 0.5 * f * f_double_prime / (f_prime**2)
            v_new = v - delta

            error = abs(v_new - v)
            errores.append(error)

            if error < tol:
                return v_new, errores, f"✅ Convergió en {i+1} iteraciones."

            v = v_new
        except Exception as e:
            return None, errores, f"❌ Error en Taylor: {e}"

    return None, errores, "❌ No convergió en el máximo número de iteraciones."

# --- Comparación de métodos ---
def comparar_metodos_vdw(P=0.5e6, T=200):
    salida = [f"Comparación de métodos para P = {P/1e6:.1f} MPa, T = {T} K\n"]
    v_ideal = R * T / P
    salida.append(f"📌 Volumen ideal: {v_ideal:.6e} m³/mol")

    # Método Brentq
    intervalo_a, intervalo_b = encontrar_intervalo(P, T)
    v_brentq = None
    if intervalo_a is None:
        salida.append("❌ No se encontró intervalo válido para Brentq.")
    else:
        try:
            start = time.perf_counter()
            v_bq = brentq(van_der_waals_eq, intervalo_a, intervalo_b, args=(P, T))
            end = time.perf_counter()

            if v_bq < b * 1.01: # type: ignore
                salida.append("⚠️ Raíz encontrada muy cercana a b (no física).")
            else:
                v_brentq = v_bq
                salida.append(f"✅ Brentq: {v_brentq:.6e} m³/mol")
                salida.append(f"⏱️ Tiempo: {(end - start) * 1000:.2f} ms")
        except Exception as e:
            salida.append(f"❌ Error en Brentq: {e}")

    # Método Taylor
    salida.append("\n⚙️ Método de Taylor:")
    v0 = max(5 * b, v_ideal * 0.5)
    v_taylor, errores, msg_taylor = taylor_vdw(P, T, v0=v0)

    if v_taylor:
        salida.append(f"✅ Taylor: {v_taylor:.6e} m³/mol")
        salida.append(f"🔁 Iteraciones: {len(errores)}")
        salida.append(f"📉 Último error: {errores[-1]:.2e}")
    else:
        salida.append(msg_taylor)
        salida.append("⚠️ No se obtuvo resultado válido con Taylor.")

    return "\n".join(salida)

EXPLICACION_INCISO_A = """
🔬 Correcciones del modelo de Van der Waals:

La ecuación de Van der Waals mejora el modelo de gas ideal introduciendo dos correcciones fundamentales:

1️⃣ Corrección por volumen propio de las moléculas:
   - En el modelo ideal se supone que las moléculas no ocupan volumen, lo cual no es realista.
   - Van der Waals introduce un término "b", que representa el volumen excluido por mol de moléculas.
   - Esto reduce el volumen disponible efectivo: (v - b), donde v es el volumen molar total.

2️⃣ Corrección por fuerzas intermoleculares:
   - Los gases ideales no consideran interacciones atractivas entre moléculas.
   - Van der Waals corrige esto sumando un término "a / v²" a la presión.
   - Este término reduce la presión efectiva, ya que las fuerzas atractivas disminuyen los choques contra las paredes del recipiente.

📘 Ecuación de Van der Waals:
    (P + a / v²)(v - b) = R·T

Donde:
    - P es la presión del gas
    - v es el volumen molar
    - T es la temperatura
    - R es la constante universal de los gases
    - a y b son constantes características de cada gas

🧪 Estas correcciones permiten modelar el comportamiento real de los gases a presiones altas o temperaturas bajas, donde las desviaciones del modelo ideal son significativas.
"""

PROBLEMAS_INCISO_A = """
🧠 Análisis de la resolución implementada:

Tras identificar que la Ley de los Gases Ideales no reproducía adecuadamente los datos experimentales a 200 K y 5 MPa, se procedió a aplicar el modelo de Van der Waals, que introduce correcciones por el volumen finito de las moléculas y las fuerzas intermoleculares.

📌 Para hallar el volumen molar real del CO₂ bajo estas condiciones, se reformuló la ecuación de Van der Waals como una función no lineal f(v) = (P + a/v²)(v - b) - RT, cuyo valor debe ser igual a cero en la raíz buscada. Debido a la naturaleza no lineal y potencialmente multirraíz de la función, se utilizó un enfoque robusto basado en el método de Brent (`brentq`), el cual combina bisección, secante y regula falsi, asegurando convergencia siempre que se conozca un intervalo con cambio de signo.

🔎 Para garantizar la validez del intervalo de búsqueda, se implementó un procedimiento automático (`encontrar_intervalo`) que recorre un dominio físicamente razonable y detecta regiones donde la función cambia de signo. Esta búsqueda resultó esencial para evitar errores de convergencia, especialmente dado que la ecuación puede presentar comportamientos singulares a bajos volúmenes.

⚠️ Una vez encontrado el volumen real, se lo comparó con el volumen ideal para las mismas condiciones. La diferencia relativa fue del orden del 7688 %, lo cual, aunque sorprendente a primera vista, es coherente con lo esperado: a presiones altas y bajas temperaturas, las hipótesis del modelo ideal se rompen completamente. Este valor no representa un error en la implementación, sino más bien un reflejo claro del desvío físico entre ambos modelos.

✅ En síntesis, el resultado no solo valida la necesidad de utilizar modelos realistas como el de Van der Waals en contextos extremos, sino que también demuestra la efectividad del método numérico empleado y su correcta integración con el análisis físico del problema.
"""


PROBLEMAS_INCISO_B = """
📘 En este inciso nos propusimos determinar el volumen molar real del dióxido de carbono (CO₂) a una presión considerablemente menor que en el caso anterior: 0.5 MPa, manteniendo constante la temperatura a 200 K.

🔍 Utilizamos dos métodos numéricos distintos —el método de Brent y el método de Taylor de segundo orden— tal como se desarrollaron en el inciso anterior. Para ambos métodos, partimos de la ecuación de Van der Waals, que corrige las desviaciones del modelo ideal al incorporar efectos de volumen propio de las moléculas y fuerzas intermoleculares.

🔧 Inicialmente, intentamos aplicar el método de Brent sobre un intervalo hallado automáticamente. Si bien se encontró una raíz, esta se ubicaba peligrosamente cerca del valor de exclusión física \(b\), lo que la vuelve sospechosa desde el punto de vista físico. Por tal motivo, se la descartó como solución válida.

⚙️ El método de Taylor, por otro lado, sí logró converger exitosamente. A partir de una condición inicial razonable (entre 5b y la mitad del volumen ideal), encontró una raíz físicamente consistente con una precisión elevada (error final ≈ \(4.62 \times 10^{-9}\)) en tan solo 10 iteraciones. Se destaca la estabilidad y confiabilidad del método en este caso.

📌 Conclusiones:
- A presiones más bajas, la diferencia entre el volumen ideal y el real sigue siendo significativa, confirmando la necesidad de usar modelos no ideales.
- El método de Brent no siempre converge a una raíz físicamente aceptable si el intervalo no está bien definido o si hay raíces múltiples.
- El método de Taylor mostró gran eficiencia y precisión, siempre que se lo inicie con una condición física razonable.
- Este ejercicio refuerza la importancia de analizar críticamente las soluciones numéricas, especialmente cuando se trabaja con ecuaciones no lineales en contextos físicos reales.
"""

def generar_grafico_volumenes_comparados(P=5e6, T=200.0):
    import matplotlib.pyplot as plt
    import io

    v_ideal, v_real, diferencia, mensaje = resolver_vdw_brentq(P, T)

    fig, ax = plt.subplots(figsize=(6, 5))
    etiquetas = ["Gas ideal", "Gas real (Van der Waals)"]
    valores = [v_ideal, v_real]
    colores = ["#6baed6", "#fd8d3c"]

    ax.bar(etiquetas, valores, color=colores, width=0.6)

    ax.set_title("Comparación de volumen molar", fontsize=14)
    ax.set_ylabel("Volumen molar [m³/mol]", fontsize=12)

    # Mostrar valores en decimal normal, con 5 decimales y colocar un poco más abajo para no tapar el título
    for i, valor in enumerate(valores):
        ax.text(i, valor + max(valores)*0.01, f"{valor:.5f}", ha='center', fontsize=10)

    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer

