import numpy as np
import comun
from comun import MAX_ITER, TOL

'''
Bisección
Busca una raíz de f(x) = 0 en un intervalo [a, b] donde f cambia de signo (f(a)·f(b) < 0).
En cada paso toma el punto medio c = (a + b)/2 y se queda con la mitad donde sigue el cambio
de signo. El intervalo se reduce a la mitad en cada iteración (convergencia lineal).
Si no hay cambio de signo, el método no aplica.
'''

def biseccion(f, a, b):
    a, b = np.float64(a), np.float64(b)
    fa, fb = f(a), f(b)
    if not (np.isfinite(fa) and np.isfinite(fb)):
        return "no aplica", [], "f no está definida en un extremo del intervalo"
    if fa * fb > 0:
        return "no aplica", [], f"f(a)·f(b) = {fa * fb:.3g} > 0: no hay cambio de signo"

    filas = []
    c_anterior = None
    for n in range(1, MAX_ITER + 1):
        c = (a + b) / 2
        fc = f(c)
        filas.append((n, c, fc))
        if abs(fc) < TOL or (c_anterior is not None and abs(c - c_anterior) < TOL):
            return "converge", filas, ""
        if fa * fc < 0:
            b = c
        else:
            a, fa = c, fc
        c_anterior = c
    return "no converge", filas, "se alcanzó el máximo de iteraciones"

if __name__ == "__main__":
    resultados = []
    for fun in comun.FUNCIONES:
        a, b = fun["intervalo"]
        estado, filas, obs = biseccion(fun["f"], a, b)
        resultados.append((fun, f"[{a}, {b}]", estado, filas, obs))
    comun.guardar("Bisección", resultados)
