import numpy as np
import comun
from comun import MAX_ITER

def punto_fijo(f, g, x0):
    x = np.float64(x0)
    filas = [(0, x, f(x))]
    for n in range(1, MAX_ITER + 1):
        x_nuevo = g(x)
        fx_nuevo = f(x_nuevo)
        if not comun.valido(x_nuevo, fx_nuevo):
            return "no converge", filas, f"en la iteración {n}: x = {x_nuevo:.3g} fuera del dominio o diverge"
        filas.append((n, x_nuevo, fx_nuevo))
        if comun.cumple_criterio(x_nuevo, x, fx_nuevo):
            return "converge", filas, ""
        x = x_nuevo
    return "no converge", filas, "se alcanzó el máximo de iteraciones"

if __name__ == "__main__":
    resultados = []
    for fun in comun.FUNCIONES:
        g = fun["g"]
        estado, filas, obs = punto_fijo(fun["f"], g, fun["x0"])
        x_final = filas[-1][1]
        dg = abs((g(x_final + 1e-6) - g(x_final - 1e-6)) / 2e-6)
        nota = f"g(x) = {fun['g_texto']}; |g'(x_n)| = {dg:.3f} en la última aproximación"
        if dg > 0.9:
            nota += " (cerca de 1: contracción muy débil)"
        resultados.append((fun, f"x0 = {fun['x0']}", estado, filas, nota + ("; " + obs if obs else "")))
        