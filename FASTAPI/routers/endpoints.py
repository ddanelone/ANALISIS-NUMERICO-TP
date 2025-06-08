from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, StreamingResponse
from services import procesador

router = APIRouter()

@router.get("/saludo")
def saludo(nombre: str = Query(...)):
    mensaje = procesador.generar_saludo(nombre)
    return JSONResponse(content={"mensaje": mensaje})

@router.get("/imagen")
def imagen_exponencial():
    img_bytes = procesador.generar_grafico_exponencial()
    return StreamingResponse(img_bytes, media_type="image/png")
