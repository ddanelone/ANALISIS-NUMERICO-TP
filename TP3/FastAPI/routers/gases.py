from fastapi import APIRouter, HTTPException, Body
from models.gases import ParametrosGas
from services.gases import resolver_volumen_real

router = APIRouter(
    prefix="/api/gases",
    tags=["Gases"],
    responses={404: {"description": "Endpoint no encontrado"}}
)

@router.post("/inciso_a", summary="TP3 2.a - Van der Waals a alta presión")
async def inciso_a():
    try:
        params = ParametrosGas(
            presion=5.0,
            temperatura=200.0,
            metodo="newton",
            x0=0.1,
            tolerancia=1e-6,
            max_iter=100
        )
        resultado = resolver_volumen_real(params)
        return {
            "descripcion": "Volumen real del CO₂ a 5 MPa y 200 K usando método de Newton modificado.",
            "presion_MPa": params.presion,
            "temperatura_K": params.temperatura,
            "volumen_molar_L_por_mol": round(resultado.get("raiz", 0), 6),
            "error_final": round(resultado.get("error_final", 0), 10),
            "iteraciones": resultado.get("iteraciones", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/inciso_b", summary="TP3 2.b - Comparación métodos a baja presión")
async def inciso_b(
    params: ParametrosGas = Body(
        ...,
        example={
            "presion": 0.5,
            "temperatura": 200.0,
            "metodo": "newton",
            "x0": 0.1,
            "a": 0.01,
            "b": 1.0,
            "tolerancia": 1e-6,
            "max_iter": 100
        }
    )
):
    try:
        # Método Newton
        params_newton = ParametrosGas(
            presion=params.presion,
            temperatura=params.temperatura,
            metodo="newton",
            x0=params.x0,
            tolerancia=params.tolerancia,
            max_iter=params.max_iter
        )
        resultado_newton = resolver_volumen_real(params_newton)

        # Método Combinado
        params_comb = ParametrosGas(
            presion=params.presion,
            temperatura=params.temperatura,
            metodo="combinado",
            a=params.a if params.a is not None else 0.01,
            b=params.b if params.b is not None else 1.0,
            tolerancia=params.tolerancia,
            max_iter=params.max_iter
        )
        resultado_comb = resolver_volumen_real(params_comb)

        return {
            "descripcion": f"Comparación del volumen molar del CO₂ a {params.presion} MPa y {params.temperatura} K con ambos métodos.",
            "presion_MPa": params.presion,
            "temperatura_K": params.temperatura,
            "metodo_newton": {
                "volumen_molar_L_por_mol": round(resultado_newton.get("raiz", 0), 6),
                "iteraciones": resultado_newton.get("iteraciones", 0),
                "error_final": round(resultado_newton.get("error_final", 0), 10)
            },
            "metodo_combinado": {
                "volumen_molar_L_por_mol": round(resultado_comb.get("raiz", 0), 6),
                "iteraciones": resultado_comb.get("iter_biseccion", [])[-1][0] if resultado_comb.get("iter_biseccion") else 0,
                "error_final": round(resultado_comb.get("error_final", 0), 10)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))