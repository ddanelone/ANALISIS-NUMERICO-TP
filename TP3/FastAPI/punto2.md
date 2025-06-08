# TP3 - Punto 2: Aplicación en sistemas de gases

## Contexto

Un equipo de científicos estudia el comportamiento del dióxido de carbono (CO₂) en condiciones extremas de presión y temperatura (como en ambientes planetarios o industriales). Se requiere usar un modelo más realista que la ley de gases ideales.

Se considera la **ecuación de Van der Waals**:

\[
\left(P + \frac{a}{v^2}\right)(v - b) = RT
\]

donde:

- \( P \): presión (MPa)
- \( v \): volumen molar (L/mol)
- \( T \): temperatura (K)
- \( R \): constante de los gases (0.08314 L·bar/K·mol)
- \( a = 3.592 \), \( b = 0.04267 \): constantes para el CO₂

> ⚠️ Importante: Se convierten unidades para mantener coherencia (MPa a bar, etc.)

---

## Inciso a

### Objetivo

Calcular el volumen real del CO₂ a **200 K y 5 MPa**, utilizando el método de Newton para resolver la ecuación de Van der Waals.

### Endpoint

`POST /api/gases/inciso_a`

### Respuesta esperada (ejemplo)

```json
{
  "descripcion": "Volumen real del CO₂ a 5 MPa y 200 K usando método de Newton modificado.",
  "presion_MPa": 5.0,
  "temperatura_K": 200.0,
  "volumen_molar_L_por_mol": 0.003484,
  "error_final": 0.00000196,
  "iteraciones": 46
}
```
