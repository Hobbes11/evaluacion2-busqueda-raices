# La raíz que se esconde

## 1. Descripción del proyecto

Este proyecto implementa y compara seis métodos numéricos para encontrar raíces de funciones:

- Bisección.
- Falsa posición.
- Punto fijo.
- Secante.
- Newton-Raphson.
- Newton-Raphson mejorado.

El objetivo es analizar la convergencia de los métodos, comparar la cantidad de iteraciones que necesitan y estudiar las condiciones en las que cada uno funciona o falla.

Se utilizan seis funciones de distinta naturaleza: polinómica con raíz simple, polinómica con raíz doble, logarítmica, exponencial, trigonométrica y mixta.

## 2. Requisitos

Python 3 con un entorno virtual (`venv`) y dos librerías: `numpy` y `matplotlib`.

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Estructura del proyecto

```text
evaluacion2-busqueda-raices/
├── README.md
├── requirements.txt
├── informe.md
└── src/
    ├── scripts/
    │   ├── comun.py
    │   ├── biseccion.py
    │   ├── falsaPosicion.py
    │   ├── puntoFijo.py
    │   ├── secante.py
    │   ├── newtonRaphson.py
    │   └── newtonMejorado.py
    ├── data/
    │   └── Archivos CSV generados
    └── assets/
        └── Graficas PNG generadas
```

## 4. Ejecución

Desde la raíz del proyecto (también funciona desde cualquier otra carpeta):

```bash
python src/scripts/biseccion.py
python src/scripts/falsaPosicion.py
python src/scripts/puntoFijo.py
python src/scripts/secante.py
python src/scripts/newtonRaphson.py
python src/scripts/newtonMejorado.py
```

| Script | Qué hace |
|---|---|
| `biseccion.py` | Divide a la mitad un intervalo con cambio de signo hasta encontrar la raíz. |
| `falsa_posicion.py` | Como la bisección, pero usa el corte con el eje x de la recta entre `(a, f(a))` y `(b, f(b))`. |
| `punto_fijo.py` | Itera `x = g(x)` con un despeje `g` de cada función. |
| `secante.py` | Como Newton, pero aproxima la derivada con los dos últimos puntos. |
| `newton_raphson.py` | Sigue la tangente de `f` hasta el eje x (usa `f'`). |
| `newton_mejorado.py` | Newton que mantiene orden 2 en raíces múltiples (usa `f'` y `f''`). |

`comun.py` no se ejecuta: guarda las funciones de prueba y el código compartido (CSV y gráficos).

Cada script guarda su CSV y actualiza `resumen.csv` sin borrar los otros métodos. Al terminar los
seis quedan 7 CSV en `src/data/` y 13 gráficos PNG en `src/assets/`.

## 5. Parámetros numéricos

Para las pruebas se utiliza una tolerancia de `1e-6` y un máximo de 100 iteraciones.

Los métodos de intervalo, como bisección y falsa posición, necesitan un intervalo válido con cambio de signo, salvo que un extremo sea directamente una raíz. Los métodos abiertos utilizan aproximaciones iniciales y pueden depender de la elección de estas para converger.

La función polinómica \((x-2)^2\) tiene una raíz doble en \(x=2\), pero no presenta cambio de signo alrededor de ella. Este caso permite estudiar una limitación de los métodos que requieren un intervalo con cambio de signo.

## 6. Informe

El archivo `informe.md` presenta el análisis de los resultados, responde las seis preguntas de convergencia de la evaluación y expone las conclusiones sobre la velocidad, robustez y aplicabilidad de los métodos.

## 7. Reproducibilidad

Para reproducir las pruebas:

1. Clonar o descargar el repositorio.
2. Crear y activar el entorno virtual.
3. Instalar las dependencias.
4. Ejecutar los scripts de los métodos.
5. Revisar los archivos CSV y las gráficas generadas.
6. Consultar `informe.md` para el análisis de los resultados.
