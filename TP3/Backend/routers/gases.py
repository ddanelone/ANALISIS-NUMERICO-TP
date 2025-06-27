from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse, StreamingResponse

from services.gases import EXPLICACION_INCISO_A, PROBLEMAS_INCISO_A, PROBLEMAS_INCISO_B, comparar_metodos_vdw, generar_grafico_gases, generar_grafico_general, generar_grafico_volumenes_comparados, generar_grafico_zoom
from services.prestacion_gases import generar_grafico_comparativo_gral, generar_grafico_comparativo_z
from services.raices import ejecutar_metodos_con_comparacion, obtener_funciones_numericas

router = APIRouter(
    prefix="/api/gases",
    tags=["Aplicación a un sistema de Gases"],
    responses={404: {"description": "Endpoint no encontrado"}}
)

@router.get("/consigna-gral", response_class=PlainTextResponse)
def obtener_consigna_planteo():
    consigna = """
   Aplicación en sistemas de gases
Un equipo de científicos inaugura un laboratorio subterráneo de alta presión ubicado en Bariloche. Su misión
es investigar el comportamiento de gases reales bajo condiciones extremas de presión y temperatura, como
las que se dan en el interior de planetas o en procesos industriales avanzados. Una de las primeras tareas del
equipo consiste en estudiar el comportamiento del dióxido de carbono (CO2), que sería utilizado como fluido
supercrítico en procesos de extracción. Los ingenieros logran mantener el gas a una temperatura constante de
200 K, y mediante un sistema de compresión controlada, lo someten a una presión de 5 MPa. Sin embargo,
al intentar calcular el volumen molar del gas usando la ley de los gases ideales:
                                       Pv = RT (1)
obtienen un resultado que no concuerda con las mediciones experimentales. Sospechan que a esa presión, las
interacciones moleculares y el volumen finito de las moléculas empiezan a jugar un papel importante, por lo
que deciden usar una versión mejorada: la ecuación de Van der Waals, que introduce correcciones al modelo
ideal.
"""
    return consigna.strip()
 
@router.get("/consigna-a", response_class=PlainTextResponse)
def obtener_consigna():
    consigna = """
2. a) Investigar cuales son las correcciones que introduce el modelo de Van der Waals. Determinar el volumen
real que tendría el gas bajo esas condiciones.
"""
    return consigna.strip()
 
@router.get("/consigna-b", response_class=PlainTextResponse)
def obtener_consignabis():
    consigna = """
2. b) Determinar nuevamente el volumen real del gas utilizando ahora una presion de 0.5 MPa utilizando los dos
métodos desarrollados en el insiso anterior. Evalue diferentes condiciones iniciales. Obtener conclusiones
a partir de los resultados.
"""
    return consigna.strip()

@router.get("/grafico-a")
def grafico_gases():
    buf = generar_grafico_gases()
    return StreamingResponse(buf, media_type="image/png")

@router.get("/grafico-b")
def grafico_gas():
    P = 0.5e6
    T = 200.0
    R = 8.314  # J/(mol·K)

    _, historial_combinado, _ = ejecutar_metodos_con_comparacion(a=0.001, b=0.05)

    if not historial_combinado:
        return {"error": "No se pudo calcular volumen real para graficar"}

    v_real = historial_combinado[-1]["x"]
    v_ideal = R * T / P

    return generar_grafico_general(v_ideal, v_real, P, T)

@router.get("/zoom")
def grafico_zoom_gas():
    P = 0.5e6
    T = 200.0

    # Usamos los mismos límites iniciales que en 2.b
    a_ini = 0.001
    b_fin = 0.05

    _, historial_combinado, _ = ejecutar_metodos_con_comparacion(a_ini, b_fin)

    if not historial_combinado:
        return {"error": "No se pudo calcular volumen real para graficar"}

    v_real = historial_combinado[-1]["x"]
    return generar_grafico_zoom(v_real, P, T)

 
@router.get("/taylor-vdw", response_class=PlainTextResponse)
def aplicar_taylor_vdw():
    return comparar_metodos_vdw() 
 
@router.get("/explicacion-inciso-a", response_class=PlainTextResponse)
def obtener_explicacion_inciso_a():
    return EXPLICACION_INCISO_A

@router.get("/grafico_comparativo_gral")
def grafico_comparativo_gral():
    return StreamingResponse(generar_grafico_comparativo_gral(), media_type="image/png")

@router.get("/grafico_comparativo_z")
def grafico_comparativo_z():
    return StreamingResponse(generar_grafico_comparativo_z(), media_type="image/png")
 
@router.get("/dificultad-a", response_class=PlainTextResponse)
def obtener_dificultada():
    return PROBLEMAS_INCISO_A
 
@router.get("/dificultad-b", response_class=PlainTextResponse)
def obtener_dificultadb():
    return PROBLEMAS_INCISO_B
 
@router.get("/grafico_comparacion_volumenes", response_class=Response)
def grafico_comparacion_volumenes():
    imagen = generar_grafico_volumenes_comparados()
    return Response(content=imagen.getvalue(), media_type="image/png")
 
# Cambio en la resolución del item b
@router.get("/resultado")
def resultado_taylor_05mpa():
    P = 0.5e6
    T = 200.0
    R = 8.314  # J/(mol·K)

    # Ajustar valores globales si tus funciones dependen de ellos (por ejemplo en van_der_waals_eq)

    # Ejecutar ambos métodos
    historial_taylor, historial_combinado, log = ejecutar_metodos_con_comparacion(a=0.001, b=0.05)

    # Calcular volumen ideal
    v_ideal = R * T / P

    # Extraer resultados de los métodos
    v_taylor = historial_taylor[-1]["x"]
    v_combinado = historial_combinado[-1]["x"]

    dif_taylor = abs(v_taylor - v_ideal) / v_taylor * 100
    dif_combinado = abs(v_combinado - v_ideal) / v_combinado * 100

    return {
        "mensaje": "Resolución del inciso 2.b con los métodos solicitados",
        "volumen_ideal": f"{v_ideal:.6e}",
        "volumen_taylor": f"{v_taylor:.6e}",
        "volumen_combinado": f"{v_combinado:.6e}",
        "diferencia_taylor_%": f"{dif_taylor:.4f}",
        "diferencia_combinado_%": f"{dif_combinado:.4f}",
        "log": log
    }
