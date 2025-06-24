from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.responses import PlainTextResponse
from starlette.responses import StreamingResponse
import time
import io
from services.raices import PROBLEMAS_INCISO_A, PROBLEMAS_INCISO_A_MULTI, PROBLEMAS_INCISO_B, PROBLEMAS_INCISO_B_MULTI, ejecutar_comparacion_taylor_multivariable, ejecutar_metodos_con_comparacion, graficar_comparacion_convergencia, graficar_comparacion_convergencia_multi, graficar_convergencia_loglog, graficar_convergencia_loglog_multi, graficar_iteraciones, graficar_iteraciones_multivariable, graficar_taylor_local, graficar_taylor_local_multivariable, metodo_taylor_biseccion_con_log, metodo_taylor_multivariable, metodo_taylor_multivariable_robusto, obtener_funciones_multivariables, obtener_funciones_numericas, metodo_taylor_segundo_orden

router = APIRouter(
    prefix="/api/raices",
    tags=["Raíces"],
    responses={404: {"description": "Endpoint no encontrado"}}
)

@router.get("/consigna-a", response_class=PlainTextResponse)
def obtener_consigna():
    consigna = """
Trabajo Práctico - Búsqueda de raíces en funciones no-lineales

1. a) Desarrollar y codificar un método para la resolución de ecuaciones no-lineales que utilice la expansión de
la serie de Taylor hasta la segunda derivada incluida. Qué condiciones debe cumplir la función para poder
aplicar el método? Justifique los pasos para determinar el valor de la siguiente iteración. Determinar el
error y el orden de convergencia. Confirme su buen funcionamiento con alguna función conocida.
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

### Agregado multivariable

@router.get("/taylor-multivariable", summary="Taylor multivariable con Hessiana")
def taylor_multivariable_json():
    F, J, H, _ = obtener_funciones_multivariables()
    historial, salida = metodo_taylor_multivariable(F, J, H, x0=[2.5, -2.5])
    return JSONResponse(content={"historial": historial, "salida": salida})

@router.get("/grafico1-multivariable", summary="Gráfico Taylor multivariable")
def grafico_taylor_multivariable():
    F, J, H, _ = obtener_funciones_multivariables()
    historial, _ = metodo_taylor_multivariable(F, J, H, x0=[2.5, -2.5])

    if not historial:
        raise HTTPException(status_code=500, detail="No se generaron iteraciones.")

    buffer = graficar_iteraciones_multivariable(historial, F, funcion_str="Sistema F(x, y)")
    return StreamingResponse(buffer, media_type="image/png")

@router.get("/grafico2-multivariable", summary="Gráfico de convergencia log-log Taylor multivariable")
def grafico_convergencia_multi():
    try:
        buffer = graficar_convergencia_loglog_multi()
        return StreamingResponse(buffer, media_type="image/png")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/grafico3-multivariable/{iteration}", summary="Gráfico local multivariable por iteración")
def grafico_taylor_local_multivariable_endpoint(iteration: int):
    try:
        buffer = graficar_taylor_local_multivariable(iteration)
        return StreamingResponse(buffer, media_type="image/png")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dificultad-a-multi", response_class=PlainTextResponse)
def obtener_dificultada_multi():
    return PROBLEMAS_INCISO_A_MULTI
 
@router.get("/inciso1b-multi", response_class=PlainTextResponse)
def inciso1b_multi():
    return ejecutar_comparacion_taylor_multivariable()
 
@router.get("/grafico4-multi", summary="Gráfico de convergencia Taylor multivariable")
def grafico4_multi():
    try:
        buffer = graficar_comparacion_convergencia_multi()
        return StreamingResponse(buffer, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
 
@router.get("/dificultad-b-multi", response_class=PlainTextResponse)
def obtener_dificultadb_multi():
    return PROBLEMAS_INCISO_B_MULTI
 
### Fin agregado  ---> Si se queda el multi, borrar a partir de aquí

@router.get("/taylor", summary="Taylor (datos + texto enriquecido)")
def metodo_taylor_segundo_orden_json():
    f, f1, f2 = obtener_funciones_numericas()
    historial, salida = metodo_taylor_segundo_orden(f, f1, f2)
    return JSONResponse(content={"historial": historial, "salida": salida})

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
    a, b = 0.1, 18
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
 
@router.get("/dificultad-a", response_class=PlainTextResponse)
def obtener_dificultada():
    return PROBLEMAS_INCISO_A
 
@router.get("/dificultad-b", response_class=PlainTextResponse)
def obtener_dificultadb():
    return PROBLEMAS_INCISO_B