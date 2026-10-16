import numpy as np
import comun
from comun import MAX_ITER

def newton(f, df, x0):
    x = np.float64(x0)
    fx = f(x)
    if not comun.valido(x, fx):
        return "no aplica", [], "f no está definida en x0"
    filas = [(0, x, fx)]
    for n in range(1, MAX_ITER + 1):
        derivada = df(x)
        if derivada == 0 or not np.isfinite(derivada):
            return "no converge", filas, f"f'(x) = 0 o no definida en la iteración {n}"
        x_nuevo = x - fx / derivada
        fx_nuevo = f(x_nuevo)
        if not comun.valido(x_nuevo, fx_nuevo):
            return "no converge", filas, f"en la iteración {n}: x = {x_nuevo:.3g} fuera del dominio o diverge"
        filas.append((n, x_nuevo, fx_nuevo))
        if comun.cumple_criterio(x_nuevo, x, fx_nuevo):
            return "converge", filas, ""
        x, fx = x_nuevo, fx_nuevo
    return "no converge", filas, "se alcanzó el máximo de iteraciones"

if __name__ == "__main__":
    resultados = []
    for fun in comun.FUNCIONES:
        estado, filas, obs = newton(fun["f"], fun["df"], fun["x0"])
        resultados.append((fun, f"x0 = {fun['x0']}", estado, filas, obs))
    comun.guardar("Newton-Raphson", resultados)
    