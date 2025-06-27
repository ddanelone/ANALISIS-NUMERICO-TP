import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

# Definir la función
def f(x):
    return np.exp(-x) - x

# Buscar la raíz con brentq
raiz = brentq(f, 0, 1)

# Crear valores de x más amplios
x_vals = np.linspace(-2, 4, 800)
y_vals = f(x_vals)

# Graficar la función
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label=r'$f(x) = e^{-x} - x$', color='blue')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')  # Eje x

# Marcar la raíz
plt.plot(raiz, f(raiz), 'ro', label=f'Raíz ≈ {raiz:.6f}') # type: ignore
plt.annotate(f'Raíz ≈ {raiz:.6f}', xy=(raiz, 0), xytext=(raiz + 0.5, 0.5), # type: ignore
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=10, color='red')

# Etiquetas y estilo
plt.title('Visualización ampliada de $f(x) = e^{-x} - x$ y su raíz')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.7)  # Eje y
plt.legend()
plt.tight_layout()
plt.show()
