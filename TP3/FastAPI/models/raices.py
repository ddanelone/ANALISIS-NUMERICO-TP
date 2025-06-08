from pydantic import BaseModel, Field
from typing import Optional

class ParametrosNewton(BaseModel):
    funcion: str = Field(..., example="x**2 - 2")
    derivada: str = Field(..., example="2*x")
    segunda_derivada: str = Field(..., example="2")
    x0: float = Field(..., example=1.0)
    tolerancia: float = Field(..., example=1e-6)
    max_iter: int = Field(..., example=50)

class ParametrosCombinado(BaseModel):
    funcion: str = Field(..., example="x**3 - x - 2")
    derivada: str = Field(..., example="3*x**2 - 1")
    segunda_derivada: str = Field(..., example="6*x")
    a: float = Field(..., example=1.0, description="Límite inferior del intervalo")
    b: float = Field(..., example=2.0, description="Límite superior del intervalo")
    tolerancia: float = Field(..., example=1e-6)
    max_iter: int = Field(..., example=100)