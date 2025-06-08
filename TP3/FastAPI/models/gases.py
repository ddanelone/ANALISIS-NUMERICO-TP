from pydantic import BaseModel
from typing import Optional

class ParametrosGas(BaseModel):
    presion: float
    temperatura: float
    metodo: str  # "newton" o "combinado"
    x0: Optional[float] = None
    a: Optional[float] = None
    b: Optional[float] = None
    tolerancia: float
    max_iter: int