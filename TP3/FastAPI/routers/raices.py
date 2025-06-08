from fastapi import APIRouter, HTTPException
from models.raices import ParametrosNewton, ParametrosCombinado
from services.raices import newton_modificado, metodo_combinado
from services.graficos import generar_grafico_newton_base64
from fastapi.responses import JSONResponse, StreamingResponse

router = APIRouter(
    prefix="/api/raices",  # Cambiado a /api/raices para mejor estructura
    tags=["Raíces"],
    responses={404: {"description": "Endpoint no encontrado"}}
)

@router.post(
    "/newton",
    summary="Método de Newton",
    response_description="Resultado del cálculo o gráfico"
)
async def calcular_newton(params: ParametrosNewton):
    try:
        resultado = newton_modificado(
            funcion=params.funcion,
            derivada=params.derivada,
            segunda_derivada=params.segunda_derivada,
            x0=params.x0,
            tolerancia=params.tolerancia,
            max_iter=params.max_iter
        )
        
        if "raiz" in resultado:
            grafico_base64 = generar_grafico_newton_base64(params, resultado)
            import base64, io
            img_data = base64.b64decode(grafico_base64)
            buf = io.BytesIO(img_data)
            return StreamingResponse(buf, media_type="image/png")
        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/combinado",
    summary="Método Combinado",
    response_description="Resultado combinado con gráfico"
)
async def calcular_combinado(params: ParametrosCombinado):
    try:
        resultado = metodo_combinado(params)

        if "grafico_base64" in resultado:
            import base64
            import io
            from fastapi.responses import StreamingResponse

            # Convertir base64 a imagen en streaming
            img_data = base64.b64decode(resultado["grafico_base64"])
            buf = io.BytesIO(img_data)
            return StreamingResponse(buf, media_type="image/png")

        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))