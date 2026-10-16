from pathlib import Path
import numpy as np
import csv
np.seterr(all="ignore")

TOL = 1e-6
MAX_ITER = 100

SRC = Path(__file__).resolve().parents[1]
CARPETA_DATOS = SRC / "data"
CARPETA_GRAFICOS = SRC / "assets"
RESUMEN = CARPETA_DATOS / "resumen.csv"
METODOS = ["Bisección", "Falsa posición", "Punto fijo", "Secante",
           "Newton-Raphson", "Newton mejorado"]
ARCHIVOS = {"Bisección": "biseccion.csv", "Falsa posición": "falsa_posicion.csv",
            "Punto fijo": "punto_fijo.csv", "Secante": "secante.csv",
            "Newton-Raphson": "newton_raphson.csv", "Newton mejorado": "newton_mejorado.csv"}

#------------------------------------------------
#Funciones
#------------------------------------------------
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

#------------------------------------------------
#CSV
#------------------------------------------------
def numero(v):
    return f"{float(v):.12g}"

def leer_csv(ruta):
    if not ruta.exists():
        return []
    with open(ruta, newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))

def guardar(metodo, resultados):
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
    filas_metodo, filas_resumen = [], []
    for fun, condicion, estado, filas, obs in resultados:
        errores = [None] + [abs(filas[i][1] - filas[i - 1][1]) for i in range(1, len(filas))]
        for (n, x, fx), error in zip(filas, errores):
            filas_metodo.append([fun["nombre"], n, numero(x), numero(fx), "" if error is None else numero(error), numero(abs(fx))])

        iteraciones = filas[-1][0] if filas else ""
        raiz = error_final = residuo_final = ""
        if estado == "converge":
            raiz = numero(filas[-1][1])
            error_final = "" if errores[-1] is None else numero(errores[-1])
            residuo_final = numero(abs(filas[-1][2]))
        elif estado == "no converge" and len(filas) > 1:
            obs = (obs + "; " if obs else "") + (
                f"última diferencia = {errores[-1]:.2e}, último residuo = {abs(filas[-1][2]):.2e}")
        filas_resumen.append({"metodo": metodo, "funcion": fun["nombre"],
                              "condicion_inicial": condicion, "estado": estado,
                              "iteraciones": iteraciones, "raiz_aproximada": raiz,
                              "error_final": error_final, "residuo_final": residuo_final,
                              "observacion": obs})
        print(f"{fun['nombre']:18s} {condicion:12s} {estado:12s} iteraciones:{str(iteraciones):>3s}  {obs}")

    with open(CARPETA_DATOS / ARCHIVOS[metodo], "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo, lineterminator="\n")
        escritor.writerow(["funcion", "iteracion", "x_n", "f_x", "error", "residuo"])
        escritor.writerows(filas_metodo)

    columnas = ["metodo", "funcion", "condicion_inicial", "estado", "iteraciones",
                "raiz_aproximada", "error_final", "residuo_final", "observacion"]
    filas_nuevas = [f for f in leer_csv(RESUMEN) if f["metodo"] != metodo] + filas_resumen
    filas_nuevas.sort(key=lambda f: METODOS.index(f["metodo"]))  # orden estable: no mezcla funciones
    with open(RESUMEN, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas, lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(filas_nuevas)
