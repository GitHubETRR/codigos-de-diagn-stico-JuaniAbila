# Calculadora Científica Modular

Calculadora científica con interfaz gráfica Tkinter, diseño modular y capacidades avanzadas de derivación.

## Características

- **3 Modos de Operación:**
  - Básica: Operaciones aritméticas simples
  - Científica: Funciones trigonométricas, exponenciales, logarítmicas
  - Funciones: Editor intuitivo con derivación y graficación

- **Motor de Derivadas:**
  - Regla de la potencia
  - Regla de la suma/resta
  - Regla del producto
  - Regla del cociente
  - Regla de la cadena
  - Derivadas de funciones trigonométricas, exponenciales y logarítmicas

- **Interfaz Intuitiva (Estilo GeoGebra):**
  - Botones rápidos para funciones comunes
  - Vista previa en tiempo real
  - Validación de sintaxis

- **Graficación:**
  - Ventana separada para gráficas
  - Visualización de función y derivada simultáneamente

## Estructura del Proyecto

```
calculadora/
├── main.py                     # Punto de entrada
├── ui/                         # Interfaz de usuario
│   ├── calculator_window.py    # Ventana principal
│   ├── graph_window.py         # Ventana de gráficas
│   └── widgets.py              # Widgets personalizados
├── math_engine/                # Motor matemático
│   ├── derivatives.py          # Motor de derivadas
│   ├── parser.py               # Parser de expresiones
│   └── evaluator.py            # Evaluador de expresiones
└── utils/                      # Utilidades
    ├── constants.py            # Constantes y configuración
    └── formatter.py            # Formateo de expresiones
```

## Instalación

```bash
pip install matplotlib numpy
```

## Uso

```bash
cd calculadora
python main.py
```

## Ejemplos de Funciones Soportadas

- Polinomios: `3x^2 + 2x - 5`
- Trigonométricas: `sin(x)`, `cos(2x)`, `tan(x^2)`
- Exponenciales: `e^x`, `e^(2x)`, `2^x`
- Logarítmicas: `ln(x)`, `log(x)`
- Composiciones: `sin(x^2)`, `e^(sin(x))`, `ln(x^2 + 1)`
- Productos: `x*sin(x)`, `x^2*e^x`
- Cocientes: `x/(x+1)`, `sin(x)/x`

## Autor

Creado con ❤️ usando Python y Tkinter
