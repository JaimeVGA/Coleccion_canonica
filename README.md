# Colección Canónica LR(0)

Herramienta educativa para la materia de Compiladores. Construye la colección canónica de conjuntos de items LR(0) a partir de una gramática libre de contexto, mostrando el proceso paso a paso mediante una interfaz gráfica.

---

## Descripción

El programa recibe una gramática libre de contexto, la aumenta automáticamente con la producción `S' → S $`, y aplica los algoritmos de **clausura** e **ir_a** para construir todos los estados del autómata LR(0). El resultado se presenta en una ventana con los conjuntos de items de cada estado, sus transiciones y una traza detallada de la construcción.

---

## Requisitos

- Python 3.7 o superior
- tkinter (incluido en la instalación estándar de Python)

---

## Ejecución

```bash
python src/interfaz.py
```

---

## Uso

1. Haz clic en **"Cargar archivo"** y selecciona un archivo de gramática (`.txt`).
2. Revisa la gramática cargada en el panel de texto.
3. Haz clic en **"Construir colección"**.
4. Se abre una ventana con:
   - La traza del algoritmo (operación por operación).
   - Los estados generados con sus items y transiciones.

Para reiniciar, usa el botón **"Limpiar"**.

---

## Formato de gramática

Los archivos de gramática admiten dos formatos:

### Formato etiquetado

```
inicio: E
no_terminales: E T F
terminales: + * ( ) id
producciones:
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
```

### Formato posicional

La primera línea lista los no terminales, la segunda los terminales, y las siguientes son las producciones:

```
E T F
+ * ( ) id
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
```

**Convenciones admitidas:**
- Flechas `->` o `→`
- Epsilon: `ε`, `e` o `epsilon`
- Alternativas con `|`
- Comentarios con `#`

---

## Gramáticas de ejemplo

La carpeta `gramaticas/` contiene seis ejemplos listos para usar:

| Archivo | Descripción |
|---|---|
| `gramatica1.txt` | Expresiones aritméticas (E, T, F) |
| `gramatica2.txt` | Declaraciones de variables con tipos |
| `gramatica3.txt` | Declaraciones con producción épsilon |
| `gramatica4.txt` | Asignaciones e instrucción `print` |
| `gramatica5.txt` | Declaraciones de arreglos multidimensionales |
| `gramatica6.txt` | Expresiones aritméticas sin recursión izquierda |

---

## Estructura del proyecto

```
Coleccion_canonica/
├── gramaticas/              # Gramáticas de ejemplo
│   ├── gramatica1.txt
│   ├── ...
│   └── gramatica6.txt
├── src/
│   ├── interfaz.py          # Ventana principal (punto de entrada)
│   ├── modelos/
│   │   └── modelos_lr0.py   # Estructuras de datos (Grammar, LR0Item, LR0State, ...)
│   ├── persistencia/
│   │   ├── lector_gramatica.py   # Parser de archivos de gramática
│   │   ├── algoritmos_lr0.py     # Algoritmos: closure, goto, canonical_collection
│   │   └── algoritmo_lr0.py      # Fachada pública
│   └── presentacion/
│       ├── estilos.py            # Tema y estilos de la interfaz
│       ├── tabla_estados.py      # Componente de estados con scroll
│       └── ventana_resultados.py # Ventana de traza de construcción
├── uml/
│   ├── diagrama_clases_lr0.png   # Diagrama de clases (PNG)
│   └── diagrama_clases_lr0.svg   # Diagrama de clases (SVG)
└── reporte/
    └── informe/
        ├── InformeActividadesEq1.tex   # Documento principal LaTeX
        ├── InformeActividadesEq1.pdf   # PDF compilado
        ├── imagenes/                   # Logo UTM y diagrama de clases
        └── secciones/
            ├── portada.tex
            ├── analisis.tex
            ├── modelo.tex
            ├── asignacion.tex
            ├── clases_metodos.tex
            ├── avances.tex
            ├── conclusiones.tex
            └── referencias.tex
```

---

## Arquitectura

El proyecto sigue el patrón **Modelo–Vista–Controlador**:

- **Modelo** — `modelos/modelos_lr0.py`: dataclasses inmutables que representan producciones, gramáticas, items y estados LR(0).
- **Controlador** — `persistencia/`: lectura de gramáticas y ejecución de los tres algoritmos LR(0) (clausura, ir_a, colección canónica).
- **Vista** — `presentacion/` e `interfaz.py`: interfaz gráfica construida con tkinter/ttk.

---

## Algoritmos implementados

| Algoritmo | Función | Descripción |
|---|---|---|
| Clausura | `closure(grammar, items)` | Expande un conjunto de items LR(0) cerrándolo bajo las producciones |
| Ir_a | `goto(grammar, items, symbol)` | Calcula el estado destino al consumir un símbolo |
| Colección canónica | `construir_coleccion(grammar)` | Construye el autómata completo, genera la traza y detecta el estado de aceptación |

---

## Diagrama de clases

El diagrama UML se encuentra en `uml/diagrama_clases_lr0.png` e incluye las cinco clases del módulo de modelos (`Production`, `Grammar`, `LR0Item`, `LR0State`, `CanonicalCollection`) y su relación con las capas de persistencia y presentación.

---

## Reporte de actividades

El directorio `reporte/informe/` contiene el informe de actividades del equipo en formato LaTeX. Para compilarlo se requiere XeLaTeX:

```bash
cd reporte/informe
xelatex InformeActividadesEq1.tex
```

El informe cubre: análisis teórico de los algoritmos LR(0), modelo del programa, asignación de actividades por subequipo, descripción de clases y métodos implementados, bitácora de avances (12–16 octubre 2026) y conclusiones.

---

## Autores

Proyecto de la asignatura **Compiladores** — 5.º semestre, UTM.

| Integrante | Subequipo |
|---|---|
| Cortez Vega Jaime Fabian | 1 — Algoritmos LR(0) |
| Lujan De la Rosa Cristian Emir | 1 — Algoritmos LR(0) |
| Arias Mendoza Angel Adrian | 2 — Modelos y lector |
| Vasquez Moreno Zair De Jesus | 2 — Modelos y lector |
| Nicolas Vasquez Joel Osmar | 3 — Interfaz gráfica |
| Carrasco Pacheco Levi Josue | 3 — Interfaz gráfica |
