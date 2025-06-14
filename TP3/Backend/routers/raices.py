from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from fastapi.responses import PlainTextResponse
from starlette.responses import StreamingResponse
from services.raices import ejecutar_metodos_con_comparacion, graficar_comparacion_convergencia, graficar_convergencia_loglog, graficar_iteraciones, graficar_taylor_local, metodo_taylor_biseccion_con_log, obtener_funciones_numericas, metodo_taylor_segundo_orden

router = APIRouter(
    prefix="/api/raices",
    tags=["Raíces"],
    responses={404: {"description": "Endpoint no encontrado"}}
)

@router.get("/consigna-a", response_class=PlainTextResponse)
def obtener_consigna():
    consigna = """
Trabajo Práctico - Búsqueda de raíces en funciones no-lineales

1. b) Combine el método desarrolado anteriormente con el método de la bisección, en un solo algoritmo. Determinar
y justificar los criterios de aplicación para lograr robustez, teniendo en cuenta que pueden introducirse
diferentes intervalos de búsqueda de raices. Utilizando la misma función del inciso anterior verifique su
funcionamiento y compare el costo computacional de ambas estrategias.
"""
    return consigna.strip()

@router.get("/consigna-b", response_class=PlainTextResponse)
def obtener_consignab():
    consigna = """
Trabajo Práctico - Búsqueda de raíces en funciones no-lineales

1. b) Combine el método desarrolado anteriormente con el método de la bisección, en un solo algoritmo. Determinar
y justificar los criterios de aplicación para lograr robustez, teniendo en cuenta que pueden introducirse
diferentes intervalos de búsqueda de raices. Utilizando la misma función del inciso anterior verifique su
funcionamiento y compare el costo computacional de ambas estrategias.
"""
    return consigna.strip()
 
@router.post("/newton", summary="Método de Taylor 2º orden (parámetros fijos)")
def metodo_taylor_segundo_orden_endpoint():
    f, f1, f2 = obtener_funciones_numericas()
    historial, resultado = metodo_taylor_segundo_orden(f, f1, f2)
    return {
        "resultado": resultado,
        "historial": historial
    }

@router.get("/grafico1", summary="Gráfico de la función y puntos iterativos")
def grafico_funcion_y_iteraciones():
    f, f1, f2 = obtener_funciones_numericas()
    historial, _ = metodo_taylor_segundo_orden(f, f1, f2, max_iter=3)

    if not historial:
        raise HTTPException(status_code=500, detail="No se generaron iteraciones para graficar.")
    
    buffer = graficar_iteraciones(historial, f, "e^{-x} - x")
    return StreamingResponse(buffer, media_type="image/png")

@router.get("/grafico2")
def grafico_convergencia():
    try:
        buffer = graficar_convergencia_loglog()
        return StreamingResponse(buffer, media_type="image/png")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/grafico3/{iteration}")
def grafico_taylor_local_endpoint(iteration: int):
    try:
        buffer = graficar_taylor_local(iteration)
        return StreamingResponse(buffer, media_type="image/png")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/inciso1b", response_class=PlainTextResponse)
def inciso1b():
    a, b = 0, 2
    tol = 1e-6
    max_iter = 50

    _, _, resultado_texto = ejecutar_metodos_con_comparacion(a, b, tol, max_iter)
    return resultado_texto

@router.get("/grafico4")
def grafico4():
    try:
        buffer = graficar_comparacion_convergencia()
        return StreamingResponse(buffer, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
