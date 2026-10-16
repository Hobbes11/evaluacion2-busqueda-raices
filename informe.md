# La raíz que se esconde

## 1. Introducción

El objetivo de este trabajo es implementar y comparar seis métodos numéricos para encontrar raíces de funciones: bisección, falsa posición, punto fijo, secante, Newton-Raphson y Newton-Raphson mejorado.

Se estudian seis funciones de distinta naturaleza para observar cómo influyen el tipo de función, las condiciones iniciales y las características de cada algoritmo en la convergencia.

Para realizar las pruebas se utiliza una tolerancia de \(10^{-6}\) y un máximo de 100 iteraciones. Los resultados se registran mediante archivos CSV y se representan mediante gráficas generadas con NumPy y Matplotlib.

## 2. Funciones estudiadas

Las funciones utilizadas son las siguientes:

| Categoría | Función | Condición inicial |
|---|---|---|
| Polinómica, raíz simple | \(f(x)=x^3-x-2\) | Intervalo \([1,2]\) |
| Polinómica, raíz doble | \(f(x)=(x-2)^2\) | \(x_0=1.2\) |
| Logarítmica | \(f(x)=\ln(x)+x-4\) | Intervalo \([2,3]\) |
| Exponencial | \(f(x)=e^{-x}-x\) | Intervalo \([0,1]\) |
| Trigonométrica | \(f(x)=\cos(x)-x\) | Intervalo \([0,1]\) |
| Mixta | \(f(x)=\sqrt{x}-\cos(x)\) | Intervalo \([0.1,1]\) |

En las funciones que cruzan el eje \(x\), el cambio de signo permite comprobar que existe al menos una raíz dentro del intervalo, siempre que la función sea continua en él. En la función \((x-2)^2\), la raíz es doble y la gráfica toca el eje \(x\) sin cruzarlo.

## 3. Análisis de convergencia

### 3.1. ¿Qué método convergió en menos iteraciones en cada función? ¿Por qué?

En las cinco funciones de raíz simple, Newton y Newton mejorado fueron los más rápidos o empataron (5, 3, 3, 4 y 2
iteraciones; en x³ − x − 2 la secante también necesita 5). En la raíz doble solo Newton mejorado da una raíz fiable (1
iteración). La razón es el orden de convergencia (pregunta 2): la bisección gana un bit por iteración y con intervalos de
ancho ≈ 1 necesita ≈ log₂(10⁶) ≈ 20 (19–20 en todas), mientras que Newton eleva el error al cuadrado en cada paso. La falsa
posición (4–12) y el punto fijo (4–34) dependen de la función: de la curvatura y de `|g′|` respectivamente.

### 3.2. ¿Qué orden de convergencia tiene cada método y cómo se refleja en el gráfico del error frente a las iteraciones?

El orden de convergencia describe la rapidez con que disminuye el error al avanzar las iteraciones.

- Bisección: tiene convergencia lineal. En cada iteración reduce a la mitad la longitud del intervalo, por lo que el error disminuye de manera progresiva.
- Falsa posición: normalmente presenta convergencia lineal, aunque su velocidad depende de la función y puede ser irregular si uno de los extremos permanece fijo durante muchas iteraciones.
- Punto fijo: su convergencia depende de la función de iteración \(g(x)\). Si se cumplen las condiciones apropiadas, suele ser lineal; una elección inadecuada puede impedir la convergencia.
- Secante: presenta convergencia superlineal, con orden aproximado de \(1.618\) bajo condiciones habituales.
- Newton-Raphson: presenta convergencia cuadrática cerca de una raíz simple cuando se cumplen las condiciones de regularidad y la derivada no se anula en la raíz.
- Newton-Raphson mejorado: puede recuperar convergencia cuadrática en raíces múltiples si la fórmula implementada corrige adecuadamente la multiplicidad y se cumplen las condiciones necesarias.

En las gráficas de \(|error|\) frente a iteración, una escala vertical logarítmica permite observar la rapidez con que disminuye el error. Una disminución progresiva suele reflejar convergencia lineal, mientras que una caída más rápida cerca de la raíz puede indicar un orden superior.

La interpretación debe contrastarse con las gráficas obtenidas. Si el error deja de disminuir, aumenta o presenta valores no válidos, esto puede indicar estancamiento, divergencia o limitaciones numéricas.

### 3.3. ¿Qué métodos requieren un intervalo con cambio de signo y cuáles no?

Bisección y falsa posición (cerrados): sin `f(a)·f(b) < 0` no aplican, y los scripts lo comprueban antes de iterar: en
`(x − 2)²` con `[1, 3]` dan `f(a)·f(b) = 1 > 0` y devuelven «no aplica». Punto fijo, secante, Newton y Newton mejorado
(abiertos) no lo necesitan, pero parten de una estimación y pueden fallar.

### 3.4. En la función con raíz doble, ¿qué métodos fallan o no aplican y cuál se comporta mejor? ¿Por qué?

| Método | Resultado (x₀ = 1,2) | `\|Δx\|` final | `\|f\|` final | Distancia a 2 |
|---|---|---|---|---|
| Bisección, Falsa posición | No aplican | — | — | — |
| Punto fijo `g = x + (x − 2)²` | No converge (100 it.) | 8,7·10⁻⁵ | 8,5·10⁻⁵ | 9,2·10⁻³ |
| Secante | Converge, 14 it. | 4,0·10⁻⁴ | 4,2·10⁻⁷ | 6,5·10⁻⁴ |
| Newton | Converge, 10 it. | 7,8·10⁻⁴ | 6,1·10⁻⁷ | 7,8·10⁻⁴ |
| Newton mejorado | Converge, 1 it. | 0,8 (salto desde x₀) | 0 | 0 |

- La raíz existe, pero la curva toca el eje sin cruzarlo: `f(2) = 0`, `f′(2) = 0` y `f ≥ 0`. Como `f ≥ 0` en todas partes,
  ningún intervalo tiene cambio de signo y los métodos cerrados no tienen nada que atrapar.
- Con `f′ = 0` en la raíz, Newton y la secante pasan a convergencia lineal: `Δ` de Newton se reduce exactamente a la mitad en
  cada paso (`ρ = 0,5` en las 10 iteraciones); la secante tiene `ρ` medio ≈ 0,58.
- Residuo pequeño no es raíz precisa: Newton y secante paran porque `|f| < 10⁻⁶`, pero como `f = (x − 2)²` eso solo exige
  `|x − 2| < 10⁻³`: quedan a 7,8·10⁻⁴ y 6,5·10⁻⁴ de la raíz.
- Diferencia pequeña tampoco es raíz precisa: el punto fijo, tras 100 iteraciones, tiene `|Δx| = 8,7·10⁻⁵` y sin embargo
  está a 9,2·10⁻³ de la raíz, unas 100 veces más lejos. Tiene `g′(2) = 1`: no hay contracción.
- Newton mejorado aplica Newton a `f/f′ = (x − 2)/2`, que tiene raíz simple, y llega a `x = 2` en un paso (`|f| = 0`).

### 3.5. ¿Cómo influyen el intervalo inicial y la estimación inicial en la cantidad de iteraciones y en la convergencia?

- Intervalo (bisección): el número de iteraciones lo fija el ancho. Con ancho 1 (0,9 en la mixta) salen 19–20 iteraciones y
  `log₂(ancho/tol) = 19,9` (19,8). El CSV lo confirma: `Δₙ = ancho/2ⁿ` (en cos(x) − x: 0,25 · 0,125 · 0,0625 …). Un intervalo más
  ancho añadiría ≈ 1 iteración por cada duplicación del ancho. En ln(x) + x − 4 son 19 porque el residuo cumplió `|f| < tol` antes.
- Intervalo (falsa posición): con el mismo ancho ≈ 1 necesita entre 4 (ln, mixta) y 12 (x³ − x − 2) iteraciones, así que no
  depende solo del ancho sino de la curvatura de `f` en el intervalo.
- Estimación inicial (Newton): la distancia a la raíz no lo explica todo. En x³ − x − 2, `x₀ = 1` está a 0,52 de la raíz y
  necesita 5 iteraciones, mientras que en ln(x) + x − 4, `x₀ = 2` está a 0,93 y necesita 3. Mirando el CSV: como `f′(1) = 2` es
  pequeña, el primer paso de x³ − x − 2 salta a `x₁ = 2` (se aleja al otro lado), mientras que en ln pasa a `x₁ = 2,871`. En la
  mixta, `x₀` está a 0,14 de la raíz y necesita solo 2. Cuenta la distancia **y** la pendiente `f′(x₀)`.
- Prueba manual: en √x − cos(x) con `x₀ = 0,1`, Newton converge en 3 iteraciones, pero Newton mejorado
  salta a `x₁ ≈ −0,51`, fuera del dominio de √x, y no converge. Por eso el ambiente usa `x₀ = 0,5`. Un mal `x₀` puede decidir
  si un método converge, no solo cuántas iteraciones necesita.
- Raíz doble: el intervalo no importa para los cerrados (nunca hay cambio de signo). En los abiertos, ver la pregunta 3.4.

### 3.6. ¿Qué método se recomienda según el tipo de función, considerando velocidad y robustez?

| Función | Recomendación | Respaldo |
|---|---|---|
| Polinómica (raíz simple) | Newton | 5 it. (empata con la secante y Newton mejorado). |
| Polinómica (raíz doble) | Newton mejorado | Único con raíz fiable: 1 it. y `\|f\| = 0`. |
| Logarítmica | Newton o secante con `x₀` dentro del dominio; bisección si no se sabe dónde está la raíz | 3–4 it. frente a 19. Teoría: Newton puede lanzar la estimación a `x < 0`, donde ln no existe. |
| Exponencial | Newton | 3 it. |
| Trigonométrica | Newton | 4 it. (la secante, 5). |
| Mixta | Newton o falsa posición | Newton 2 it.; falsa posición 4 it. y sin derivadas. |

Velocidad vs robustez: Newton y la secante son los más rápidos (2–5 iteraciones) pero necesitan una buena estimación inicial
(ver prueba manual). La bisección es lenta (19–20 iteraciones) pero, mientras haya cambio de signo, su convergencia está garantizada
(Bolzano) y siempre da `Δ = ancho/2ⁿ`, predecible. La secante evita calcular `f′` y cada iteración cuesta una sola evaluación de `f`. El
punto fijo es simple pero depende de `|g′|` (4 a 34 iteraciones según la función).

## 4. Conclusiones

- Qué método elegir: no hay un método que gane siempre. Con una buena estimación inicial y una función suave, Newton (2–5
  iteraciones) o la secante (4–5) superan a la bisección (19–20). Si se necesita certeza y hay cambio de signo, la bisección. Para
  una raíz múltiple, Newton mejorado. Con punto fijo, hay que elegir `g` con `|g′| < 1`.
- Raíz doble: `(x − 2)²` tiene raíz en `x = 2`, pero `f(1)·f(3) = 1 > 0`: tener una raíz no implica cambiar de signo.
  Bolzano da una condición suficiente, no necesaria, y por eso los métodos cerrados no aplican. Además, como `f′(2) = 0`,
  Newton y la secante pasan a convergencia lineal y paran con un residuo pequeño aunque estén a ≈ 10⁻³ de la raíz. Ni un residuo
  pequeño ni una diferencia pequeña entre aproximaciones bastan para asegurar una raíz precisa.
- Efecto del intervalo y de `x₀`: la bisección necesita ≈ `log₂(ancho/tol)` iteraciones (≈ 20 con ancho 1). En Newton cuenta la
  distancia a la raíz y la pendiente en `x₀`, y un `x₀` inadecuado puede sacar la iteración del dominio.
