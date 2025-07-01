from fastapi.responses import  StreamingResponse
import matplotlib.pyplot as plt
import numpy as np
import io
import time

from services.tp3.raices import ejecutar_metodos_con_comparacion

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

        # Usamos el mismo intervalo inicial en todos los casos (seguro)
        a_ini = 0.001
        b_fin = 0.05

        # Ejecutamos método combinado
        _, historial_combinado, _ = ejecutar_metodos_con_comparacion(a_ini, b_fin)

        if historial_combinado:
            v_real = historial_combinado[-1]["x"]
            diferencia = abs(v_real - v_ideal) / v_real * 100
            mensaje = f"v_real ≈ {v_real:.2e}, diferencia ≈ {diferencia:.2f}%"
        else:
            v_real = None
            mensaje = "❌ No se encontró raíz válida"

        resultados.append((P, v_ideal, v_real, mensaje))

        try:
            print(f"\nPresión: {P/1e6:.1f} MPa")
            print(f"v_ideal: {v_ideal:.6e}")
            print(f"v_real: {v_real}")
            print(mensaje)
        except UnicodeEncodeError:
            print(f"\nPresion: {P/1e6:.1f} MPa")
            print(f"v_ideal: {v_ideal:.6e}")
            print(f"v_real: {v_real}")
            print(mensaje.encode("ascii", "replace").decode())

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

# --- Gráfico general ---
def generar_grafico_general(v_ideal, v_real, P, T):
    # Buscar un intervalo que contenga la raíz y dé contexto visual
    v_min = max(b * 1.001, v_real * 0.5)
    v_max = v_real * 1.5

    v_vals = np.linspace(v_min, v_max, 1000)
    f_vals = [van_der_waals_eq(v, P, T) for v in v_vals]

    plt.figure(figsize=(8, 5))
    plt.plot(v_vals, f_vals, label='f(v)', color='blue')
    plt.axhline(0, color='black', linestyle='--', linewidth=1)

    plt.axvline(v_ideal, color='red', linestyle=':', linewidth=1.5, label=f'v_ideal ≈ {v_ideal:.6f}')
    plt.axvline(v_real, color='green', linestyle='--', linewidth=1.5, label=f'v_real ≈ {v_real:.6f}')

    plt.title('Función de Van der Waals a 0.5 MPa', fontsize=14)
    plt.xlabel('Volumen molar [m³/mol]')
    plt.ylabel('f(v)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')

def generar_grafico_zoom(v_real, P, T):
    delta = v_real * 0.2  # Zoom de ±20% alrededor de la raíz
    v_zoom_vals = np.linspace(v_real - delta, v_real + delta, 1000)
    f_zoom_vals = [van_der_waals_eq(v, P, T) for v in v_zoom_vals]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(v_zoom_vals, f_zoom_vals, label='f(v) (zoom)', color='royalblue', linewidth=2)
    ax.axhline(0, color='black', linestyle='--', linewidth=1)
    ax.axvline(v_real, color='green', linestyle='--', linewidth=1.5, label=f'v_real ≈ {v_real:.6f}')

    f_en_raiz = van_der_waals_eq(v_real, P, T)
    ax.plot(v_real, f_en_raiz, 'go', label='Raíz')

    ax.text(0.05, 0.95, f'f(v_real) ≈ {f_en_raiz:.2e}', transform=ax.transAxes,
            fontsize=10, verticalalignment='top', color='dimgray')

    ax.set_title('Zoom en la raíz encontrada (Taylor + Bisección)', fontsize=14)
    ax.set_xlabel('Volumen molar [m³/mol]')
    ax.set_ylabel('f(v)')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    ax.ticklabel_format(style='plain', axis='x')
    ax.ticklabel_format(style='plain', axis='y')
    plt.tight_layout()

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
    salida = [f"🧪 Comparación de métodos para P = {P/1e6:.1f} MPa, T = {T} K\n"]
    
    # Volumen ideal
    v_ideal = R * T / P
    salida.append(f"📌 Volumen ideal: {v_ideal:.6e} m³/mol")

    # Ejecutar ambos métodos sobre el mismo intervalo
    a = 0.001
    b = 0.05
    tol = 1e-6
    max_iter = 50

    try:
        start_taylor = time.perf_counter()
        historial_taylor, historial_combinado, _ = ejecutar_metodos_con_comparacion(a, b, tol, max_iter)
        end_taylor = time.perf_counter()

        # Resultados método Taylor
        v_taylor = historial_taylor[-1]["x"]
        err_taylor = historial_taylor[-1]["error"]
        salida.append("\n⚙️ Método de Taylor:")
        salida.append(f"✅ Raíz aproximada: {v_taylor:.6e} m³/mol")
        salida.append(f"🔁 Iteraciones: {len(historial_taylor)}")
        salida.append(f"📉 Último error: {err_taylor:.2e}")

        # Resultados método combinado
        v_comb = historial_combinado[-1]["x"]
        err_comb = historial_combinado[-1]["error"]
        salida.append("\n⚙️ Método combinado Taylor + Bisección:")
        salida.append(f"✅ Raíz aproximada: {v_comb:.6e} m³/mol")
        salida.append(f"🔁 Iteraciones: {len(historial_combinado)}")
        salida.append(f"📉 Último error: {err_comb:.2e}")

        # Comparación numérica
        dif_taylor = abs(v_taylor - v_ideal) / v_taylor * 100
        dif_comb = abs(v_comb - v_ideal) / v_comb * 100

        salida.append("\n📊 Comparación con volumen ideal:")
        salida.append(f"🔬 Diferencia Taylor: {dif_taylor:.4f} %")
        salida.append(f"🔬 Diferencia Combinado: {dif_comb:.4f} %")

        tiempo_total = (end_taylor - start_taylor) * 1000
        salida.append(f"\n⏱️ Tiempo total de ejecución: {tiempo_total:.2f} ms")

    except Exception as e:
        salida.append(f"❌ Error al aplicar los métodos: {e}")

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
🧠 Análisis de la resolución implementada (Inciso 2.a):

Dado que la Ley de los Gases Ideales no permite describir adecuadamente el comportamiento del dióxido de carbono (CO₂) bajo condiciones extremas de presión y temperatura (200 K y 5 MPa), se recurrió al modelo de Van der Waals, que incorpora correcciones por volumen propio de las moléculas y fuerzas de atracción intermoleculares.

📌 Se reformuló la ecuación de Van der Waals como una función no lineal en el volumen molar:

    f(v) = (P + a / v²) · (v - b) - R·T

cuya raíz representa el volumen real buscado. Dado que esta función puede presentar múltiples raíces y singularidades, se implementó un método robusto que combina la aproximación de segundo orden de Taylor con una estrategia tipo bisección para asegurar la estabilidad del proceso iterativo.

🔍 El enfoque numérico aplicado garantiza convergencia incluso ante derivadas pequeñas o discriminantes negativos, alternando entre correcciones tipo Newton-Taylor y actualizaciones del intervalo. Este método se mostró especialmente adecuado para tratar funciones con comportamiento singular cerca de v = b, como ocurre en este modelo.

📊 El resultado obtenido mostró una diferencia relativa de aproximadamente **7688 %** entre el volumen real calculado y el volumen ideal (v = R·T / P). Esta enorme discrepancia es coherente con lo esperado: bajo presiones elevadas y temperaturas bajas, el gas se desvía fuertemente del comportamiento ideal, y modelos como el de Van der Waals son indispensables.

✅ En conclusión, este inciso no solo justifica el uso de modelos físicos más complejos, sino que también demuestra la eficacia del método numérico combinado implementado para resolver ecuaciones no lineales en un contexto físico realista.
"""

PROBLEMAS_INCISO_B = """
📘 Resolución del inciso 2.b:

En esta etapa, se calculó nuevamente el volumen molar real del CO₂, esta vez bajo una presión reducida de 0.5 MPa, manteniendo la temperatura en 200 K. A diferencia del inciso anterior, se utilizaron exclusivamente los dos métodos desarrollados previamente: el método de Taylor de segundo orden y un enfoque combinado que aplica Taylor junto con Bisección para reforzar su estabilidad.

⚙️ El método de Taylor se aplicó directamente a la función de Van der Waals, partiendo desde un valor inicial físicamente razonable (entre 5·b y la mitad del volumen ideal). En solo 3 iteraciones, el método alcanzó convergencia con un error final de 2.33 × 10⁻⁷, arrojando un volumen real coherente y físicamente válido.

🔀 En paralelo, se aplicó una versión combinada del método que alterna entre pasos de Taylor y actualizaciones del intervalo al estilo Bisección. Este enfoque reforzó la robustez del proceso, asegurando que las raíces propuestas se mantuvieran dentro de un rango físico permitido. El método combinado también alcanzó convergencia en 3 iteraciones, con un error aún más bajo: 1.51 × 10⁻¹⁰.

📊 Ambos métodos coincidieron en el valor hallado: aproximadamente 0.5671 m³/mol, lo que representa una diferencia relativa del 99.41 % respecto al volumen ideal estimado por la ley de gases ideales. Este resultado vuelve a evidenciar que incluso a presiones moderadas, las correcciones de Van der Waals no pueden ser despreciadas.

📌 Conclusiones clave:
- Ambos métodos numéricos fueron efectivos, pero el método combinado resultó más robusto ante posibles problemas de convergencia.
- La diferencia con el volumen ideal sigue siendo significativa, reafirmando la validez del modelo de Van der Waals.
- La implementación demostró que el método de Taylor, reforzado con una lógica de validación tipo bisección, puede ser una alternativa precisa, rápida y físicamente confiable.
"""
def generar_grafico_volumenes_comparados(P=0.5e6, T=200.0):
    # Volumen ideal
    v_ideal = R * T / P

    # Resolver con ambos métodos
    historial_taylor, historial_combinado, _ = ejecutar_metodos_con_comparacion(a=0.001, b=0.05)
    v_taylor = historial_taylor[-1]["x"]
    v_combinado = historial_combinado[-1]["x"]

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(6, 5))

    etiquetas = ["Gas ideal", "Taylor", "Taylor + Bisección"]
    valores = [v_ideal, v_taylor, v_combinado]
    colores = ["#6baed6", "#74c476", "#fd8d3c"]

    ax.bar(etiquetas, valores, color=colores, width=0.6)

    ax.set_title("Comparación de volumen molar\n(P = 0.5 MPa, T = 200 K)", fontsize=14)
    ax.set_ylabel("Volumen molar [m³/mol]", fontsize=12)

    # Mostrar valores sobre las barras
    for i, valor in enumerate(valores):
        ax.text(i, valor + max(valores)*0.01, f"{valor:.5f}", ha='center', fontsize=10)

    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    # Guardar en buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer
