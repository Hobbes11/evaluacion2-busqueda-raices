import numpy as np
import comun
from comun import MAX_ITER

def newton_mejorado(f, df, d2f, x0):
    x = np.float64(x0)
    fx = f(x)
    if not comun.valido(x, fx):
        return "no aplica", [], "f no está definida en x0"
    filas = [(0, x, fx)]
    for n in range(1, MAX_ITER + 1):
        d1, d2 = df(x), d2f(x)
        denominador = d1 * d1 - fx * d2
        if denominador == 0 or not np.isfinite(denominador):
            return "no converge", filas, f"denominador f'^2 - f·f'' nulo o no definido en la iteración {n}"
        x_nuevo = x - fx * d1 / denominador
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
        estado, filas, obs = newton_mejorado(fun["f"], fun["df"], fun["d2f"], fun["x0"])
        resultados.append((fun, f"x0 = {fun['x0']}", estado, filas, obs))
    comun.guardar("Newton mejorado", resultados)
    