from services.raices import newton_modificado, metodo_combinado
from services.utils import eval_func
from models.gases import ParametrosGas  # Asegurate de importar el modelo
from models.raices import ParametrosCombinado  # Usado en el método combinado

# Constantes para el CO₂
R = 0.0821  # atm·L/mol·K
a = 3.592   # L²·atm/mol²
b = 0.0427  # L/mol

def ecuacion_vdw(presion, temperatura):
    """Devuelve la ecuación de Van der Waals como string"""
    P = presion * 9.86923  # MPa → atm
    T = temperatura
    return f"{P} - ({a}) / v**2 + ({b} * {P}) / v - ({R} * {T}) / v"

def resolver_volumen_real(params: ParametrosGas):
    expr = ecuacion_vdw(params.presion, params.temperatura)
    funcion = f"{expr}"
    derivada = "(-2)*3.592/(v**3) - 0.0427*{:.6f}/(v**2) + 0.0821*{:.2f}/(v**2)".format(
        params.presion * 9.86923, params.temperatura)
    segunda_derivada = "(3*2)*3.592/(v**4) + 2*0.0427*{:.6f}/(v**3) - 2*0.0821*{:.2f}/(v**3)".format(
        params.presion * 9.86923, params.temperatura)

    f_str = funcion.replace("v", "x")
    deriv_str = derivada.replace("v", "x")
    seg_deriv_str = segunda_derivada.replace("v", "x")

    if params.metodo == "newton":
        if params.x0 is None:
            raise ValueError("Para el método de Newton, se requiere el parámetro x0")
        return newton_modificado(f_str, deriv_str, seg_deriv_str, params.x0, params.tolerancia, params.max_iter)

    elif params.metodo == "combinado":
        if params.a is None or params.b is None:
            raise ValueError("Para el método combinado, se requieren los parámetros a y b")
        comb_params = ParametrosCombinado(
            funcion=f_str,
            derivada=deriv_str,
            segunda_derivada=seg_deriv_str,
            a=params.a,
            b=params.b,
            tolerancia=params.tolerancia,
            max_iter=params.max_iter
        )
        return metodo_combinado(comb_params)

    else:
        raise ValueError("Método no reconocido: debe ser 'newton' o 'combinado'")
