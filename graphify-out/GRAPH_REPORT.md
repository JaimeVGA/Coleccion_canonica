# Graph Report - Coleccion_canonica  (2026-10-16)

## Corpus Check
- Corpus is ~3,003 words - fits in a single context window. You may not need a graph.

## Summary
- 91 nodes · 193 edges · 9 communities (7 shown, 2 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 27 edges (avg confidence: 0.93)
- Token cost: 2,100 input · 1,800 output

## Community Hubs (Navigation)
- Gramáticas de Ejemplo y Conceptos LR(0)
- Lector y Parser de Gramáticas
- Interfaz Gráfica Principal
- Algoritmos Núcleo LR(0)
- Modelos de Datos
- Presentación de Estados LR(0)
- Colección Canónica
- Producciones y Gramática Aumentada
- Fachada de Algoritmos

## God Nodes (most connected - your core abstractions)
1. `Grammar` - 18 edges
2. `Colección Canónica LR(0)` - 13 edges
3. `_canonical_collection()` - 10 edges
4. `read_grammar_text()` - 10 edges
5. `LR0Item` - 9 edges
6. `InterfazColeccion` - 8 edges
7. `Production` - 8 edges
8. `canonical_collection()` - 8 edges
9. `cargar_gramatica_desde_archivo()` - 8 edges
10. `Gramática Libre de Contexto` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Gramática 4: Asignaciones e Instrucción print` --implements--> `Gramática Libre de Contexto`  [INFERRED]
  gramaticas/gramatica4.txt → README.md
- `Colección Canónica LR(0)` --references--> `Gramática 4: Asignaciones e Instrucción print`  [EXTRACTED]
  README.md → gramaticas/gramatica4.txt
- `Gramática 1: Expresiones Aritméticas (E, T, F)` --implements--> `Gramática Libre de Contexto`  [INFERRED]
  gramaticas/gramatica1.txt → README.md
- `Gramática 2: Declaraciones de Variables con Tipos` --implements--> `Gramática Libre de Contexto`  [INFERRED]
  gramaticas/gramatica2.txt → README.md
- `Gramática 3: Declaraciones con Producción Épsilon` --implements--> `Gramática Libre de Contexto`  [INFERRED]
  gramaticas/gramatica3.txt → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Core LR(0) Algorithm Trio: Closure, Goto, Canonical Collection** — readme_algoritmo_clausura, readme_algoritmo_ir_a, readme_algoritmo_canonical_collection [EXTRACTED 1.00]
- **Seis Gramáticas de Ejemplo para la Colección Canónica LR(0)** — gramaticas_gramatica1_expresiones_aritmeticas, gramaticas_gramatica2_declaraciones_variables, gramaticas_gramatica3_declaraciones_epsilon, gramaticas_gramatica4_asignaciones_print, gramaticas_gramatica5_arreglos_multidimensionales, gramaticas_gramatica6_expresiones_sin_recursion_izquierda [EXTRACTED 1.00]
- **MVC Architecture: Model, Controller (Persistencia), View (Presentacion)** — readme_patron_mvc, readme_gramatica_libre_contexto, readme_automata_lr0 [INFERRED 0.85]

## Communities (9 total, 2 thin omitted)

### Community 0 - "Gramáticas de Ejemplo y Conceptos LR(0)"
Cohesion: 0.20
Nodes (19): Gramática 1: Expresiones Aritméticas (E, T, F), Gramática 2: Declaraciones de Variables con Tipos, Gramática 3: Declaraciones con Producción Épsilon, Gramática 4: Asignaciones e Instrucción print, Gramática 5: Declaraciones de Arreglos Multidimensionales, Gramática 6: Expresiones Aritméticas sin Recursión Izquierda, Algoritmo Colección Canónica, Algoritmo Clausura (Closure) (+11 more)

### Community 1 - "Lector y Parser de Gramáticas"
Cohesion: 0.22
Nodes (14): Path, Adaptadores de persistencia y algoritmos para la interfaz., cargar_gramatica_desde_archivo(), _compact_tokens(), GrammarFormatError, _label(), ValueError, Error de sintaxis o validación en el archivo de gramática. (+6 more)

### Community 2 - "Interfaz Gráfica Principal"
Cohesion: 0.28
Nodes (4): InterfazColeccion, configurar_estilos(), crear_superficie(), VentanaResultados

### Community 3 - "Algoritmos Núcleo LR(0)"
Cohesion: 0.51
Nodes (8): Grammar, LR0Item, _canonical_collection(), closure(), _format_items(), goto(), _ordered_symbols(), Conserva el orden de aparición de los símbolos en el estado.

### Community 4 - "Modelos de Datos"
Cohesion: 0.32
Nodes (5): Modelos de la gramática y de los elementos LR(0)., GrammarError, LR0State, ValueError, La gramática no cumple las invariantes del modelo.

### Community 6 - "Colección Canónica"
Cohesion: 0.40
Nodes (4): CanonicalCollection, Colección canónica LR(0) lista para ser consumida por la interfaz., construir_coleccion(), Construye la colección LR(0) con la API estable de la interfaz.

### Community 8 - "Fachada de Algoritmos"
Cohesion: 0.40
Nodes (4): Fachada de los algoritmos LR(0) para desacoplar la interfaz., canonical_collection(), Compatibilidad pública: devuelve estados y gramática aumentada., Construye estados, transiciones deterministas y marca el estado de aceptación.

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Grammar` connect `Algoritmos Núcleo LR(0)` to `Lector y Parser de Gramáticas`, `Modelos de Datos`, `Colección Canónica`, `Producciones y Gramática Aumentada`, `Fachada de Algoritmos`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Why does `cargar_gramatica_desde_archivo()` connect `Lector y Parser de Gramáticas` to `Interfaz Gráfica Principal`, `Algoritmos Núcleo LR(0)`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `LR0State` connect `Modelos de Datos` to `Fachada de Algoritmos`, `Algoritmos Núcleo LR(0)`, `Presentación de Estados LR(0)`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Grammar` (e.g. with `canonical_collection()` and `_canonical_collection()`) actually correct?**
  _`Grammar` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `LR0Item` (e.g. with `_format_items()` and `goto()`) actually correct?**
  _`LR0Item` has 2 INFERRED edges - model-reasoned connections that need verification._