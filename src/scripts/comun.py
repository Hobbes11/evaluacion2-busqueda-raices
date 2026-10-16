from pathlib import Path
import numpy as np
np.seterr(all="ignore")

TOL = 1e-6
MAX_ITER = 100

FUNCIONES = [
    {"clave": "polinomica_simple", "categoria": "Polinómica (raíz simple)", "nombre": "x^3 - x - 2",
     "f": lambda x: x**3 - x - 2,
     "df": lambda x: 3 * x**2 - 1,
     "d2f": lambda x: 6 * x,
     "g": lambda x: np.cbrt(x + 2), "g_texto": "(x + 2)^(1/3)",
     "intervalo": (1, 2), "x0": 1.0, "x1": 1.5,
     "rango": (0.5, 2.5)},
    {"clave": "polinomica_doble", "categoria": "Polinómica (raíz doble)", "nombre": "(x - 2)^2",
     "f": lambda x: (x - 2) ** 2,
     "df": lambda x: 2 * (x - 2),
     "d2f": lambda x: 2.0,
     "g": lambda x: x + (x - 2) ** 2, "g_texto": "x + (x - 2)^2",
     "intervalo": (1, 3), "x0": 1.2, "x1": 1.7,
     "rango": (0.5, 3.5)},
    {"clave": "logaritmica", "categoria": "Logarítmica", "nombre": "ln(x) + x - 4",
     "f": lambda x: np.log(x) + x - 4,
     "df": lambda x: 1 / x + 1,
     "d2f": lambda x: -1 / x**2,
     "g": lambda x: 4 - np.log(x), "g_texto": "4 - ln(x)",
     "intervalo": (2, 3), "x0": 2.0, "x1": 2.5,
     "rango": (0.5, 4.5)},
    {"clave": "exponencial", "categoria": "Exponencial", "nombre": "exp(-x) - x",
     "f": lambda x: np.exp(-x) - x,
     "df": lambda x: -np.exp(-x) - 1,
     "d2f": lambda x: np.exp(-x),
     "g": lambda x: np.exp(-x), "g_texto": "exp(-x)",
     "intervalo": (0, 1), "x0": 0.0, "x1": 0.5,
     "rango": (-0.5, 1.5)},
    {"clave": "trigonometrica", "categoria": "Trigonométrica", "nombre": "cos(x) - x",
     "f": lambda x: np.cos(x) - x,
     "df": lambda x: -np.sin(x) - 1,
     "d2f": lambda x: -np.cos(x),
     "g": lambda x: np.cos(x), "g_texto": "cos(x)",
     "intervalo": (0, 1), "x0": 0.0, "x1": 0.5,
     "rango": (-1, 2)},
    {"clave": "mixta", "categoria": "Mixta", "nombre": "sqrt(x) - cos(x)",
     "f": lambda x: np.sqrt(x) - np.cos(x),
     "df": lambda x: 1 / (2 * np.sqrt(x)) + np.sin(x),
     "d2f": lambda x: -1 / (4 * x**1.5) + np.cos(x),
     "g": lambda x: (x + np.cos(x) ** 2) / 2, "g_texto": "(x + cos(x)^2) / 2",
     "intervalo": (0.1, 1), "x0": 0.5, "x1": 1.0,
     "rango": (0.01, 1.5)},
]

def cumple_criterio(x_nuevo, x_viejo, f_nuevo):
    return abs(f_nuevo) < TOL or abs(x_nuevo - x_viejo) < TOL

def valido(x, fx):
    return bool(np.isfinite(x) and np.isfinite(fx) and abs(x) < 1e12)
