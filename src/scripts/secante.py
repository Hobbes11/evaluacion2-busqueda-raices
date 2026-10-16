import numpy as np
import comun
from comun import MAX_ITER

'''
Secante
Como Newton, pero sin derivada: aproxima f' con la recta que pasa por los dos últimos puntos
            x_(n+1) = x_n - f(x_n)·(x_n - x_(n-1)) / (f(x_n) - f(x_(n-1)))
Necesita dos valores iniciales x0 y x1, no necesita cambio de signo.
Orden de convergencia = 1.618 en raíces simples. Falla si f(x_n) = f(x_(n-1)) (división por 0).
Numeración: x0 y x1 son datos, la primera aproximación calculada es x2.
'''

def secante(f, x0, x1):
    x_viejo, x = np.float64(x0), np.float64(x1)
    f_viejo, fx = f(x_viejo), f(x)
    if not (comun.valido(x_viejo, f_viejo) and comun.valido(x, fx)):
        return "no aplica", [], "f no está definida en x0 o x1"
    filas = [(0, x_viejo, f_viejo), (1, x, fx)]
    for n in range(2, MAX_ITER + 1):
        if fx == f_viejo:
            return "no converge", filas, "f(x_n) = f(x_(n-1)): división por cero"
        x_nuevo = x - fx * (x - x_viejo) / (fx - f_viejo)
        fx_nuevo = f(x_nuevo)
        if not comun.valido(x_nuevo, fx_nuevo):
            return "no converge", filas, f"en la iteración {n}: x = {x_nuevo:.3g} fuera del dominio o diverge"
        filas.append((n, x_nuevo, fx_nuevo))
        if comun.cumple_criterio(x_nuevo, x, fx_nuevo):
            return "converge", filas, ""
        x_viejo, f_viejo, x, fx = x, fx, x_nuevo, fx_nuevo
    return "no converge", filas, "se alcanzó el máximo de iteraciones"

if __name__ == "__main__":
    resultados = []
    for fun in comun.FUNCIONES:
        estado, filas, obs = secante(fun["f"], fun["x0"], fun["x1"])
        resultados.append((fun, f"x0 = {fun['x0']}, x1 = {fun['x1']}", estado, filas, obs))
    comun.guardar("Secante", resultados)
