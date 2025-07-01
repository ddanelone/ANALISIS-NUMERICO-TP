from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse
from services.tp2 import inciso_1

router = APIRouter(prefix="/inciso_1", tags=["TP2 - Esteganografíca LSB -Inciso 1"])


@router.post("/ocultar", response_class=PlainTextResponse, summary="Ocultar mensaje en imagen")
def ocultar_mensaje(mensaje: str = Query(..., description="Mensaje de texto a ocultar")):
    """
    Oculta un mensaje de texto en una imagen utilizando el método LSB.
    Guarda la imagen esteganográfica en disco.

    - **mensaje**: Texto plano a ocultar (se agrega '&' al final automáticamente)
    """
    return inciso_1.ocultar_mensaje_en_imagen(mensaje)


@router.get("/extraer", response_class=PlainTextResponse, summary="Extraer mensaje oculto")
def extraer_mensaje():
    """
    Extrae el mensaje oculto desde la imagen generada con el método LSB.
    """
    return inciso_1.extraer_mensaje_de_imagen()

@router.get("/consigna", response_class=PlainTextResponse, summary="Consigna original")
def get_consigna():
    """
    Devuelve la consigna original del inciso 1 del TP2.
    """
    return inciso_1.CONSIGNA_LSB
