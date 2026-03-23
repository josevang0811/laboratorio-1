# [cite_start]REPORTE TÉCNICO [cite: 1]
## [cite_start]Sistema de Tabla Hash con Persistencia para Videojuego [cite: 2, 3]

[cite_start]**Laboratorio 1 — Manejo de Índices en Archivos** [cite: 4]  
[cite_start]**Estructura de Datos 1** [cite: 5]  
[cite_start]**Universidad del Norte** [cite: 6]  
[cite_start]*Barranquilla, Colombia — 2025* [cite: 7]

---

## [cite_start]1. Introducción [cite: 8]
[cite_start]Este proyecto documenta el diseño e implementación de una **Tabla Hash en Python** desarrollada para el Laboratorio 1 de Estructura de Datos 1 en la Universidad del Norte[cite: 9]. [cite_start]El sistema fue construido desde cero, prescindiendo de los diccionarios nativos de Python para profundizar en el funcionamiento interno de esta estructura[cite: 10].

La implementación destaca por:
* [cite_start]Resolución de colisiones por encadenamiento (*chaining*)[cite: 11].
* [cite_start]Rehash automático al superar un factor de carga de **0.75**[cite: 11].
* [cite_start]Persistencia de datos mediante archivos **JSON**[cite: 11].
* [cite_start]Integración con un videojuego en versiones de consola y gráfica (Pygame)[cite: 11].

### [cite_start]1.1 Objetivos del sistema [cite: 12]
* [cite_start]Implementar manualmente una tabla hash con encadenamiento[cite: 13].
* [cite_start]Manejar el rehash automático para un rendimiento óptimo[cite: 14].
* [cite_start]Persistir datos de jugadores entre sesiones[cite: 15].
* [cite_start]Integrar la estructura en un gestor de datos de videojuego[cite: 16].
* [cite_start]Validar el sistema con una suite de **45 pruebas unitarias**[cite: 17].

### [cite_start]1.2 Tecnologías utilizadas [cite: 18]
| Tecnología | Versión | Uso |
| :--- | :--- | :--- |
| Python | 3.6+ | [cite_start]Lenguaje principal del proyecto [cite: 19] |
| Pygame / Pygame-CE | Reciente | [cite_start]Interfaz gráfica del videojuego [cite: 19] |
| JSON (módulo estándar) | — | [cite_start]Persistencia de datos en archivo [cite: 19] |
| pytest (opcional) | — | [cite_start]Ejecución de pruebas unitarias [cite: 19] |

---

## [cite_start]2. Diseño de la Tabla Hash [cite: 20]
[cite_start]La lógica reside en `hashtable.py` mediante las clases `Node` y `HashTable`[cite: 21]. [cite_start]Se utilizan listas enlazadas en cada índice para gestionar el encadenamiento[cite: 22].

### [cite_start]2.1 Clase Node [cite: 23]
[cite_start]Almacena la clave, el valor y el puntero al siguiente nodo[cite: 24]:
```python
class Node:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        [cite_start]self.siguiente = None [cite: 25, 26, 27, 28, 29]
```

### [cite_start]2.2 Clase HashTable [cite: 30]
[cite_start]Gestiona el arreglo interno y el control del factor de carga[cite: 31].
* [cite_start]**tamaño**: Inicia en 16 cubetas (*buckets*)[cite: 33].
* [cite_start]**tabla**: Lista de objetos `Node` o `None`[cite: 34].
* [cite_start]**elementos**: Contador de pares almacenados[cite: 35].
* [cite_start]**factor_carga_limite**: Umbral fijo de **0.75**[cite: 36].

### [cite_start]2.3 Función Hash [cite: 37]
[cite_start]Utiliza la función determinista `hash()` de Python limitada por el operador módulo[cite: 38]:
[cite_start]$$index = hash(clave) \pmod{self.tamaño}$$ [cite: 39, 40]

### [cite_start]2.4 Complejidad algorítmica [cite: 42]
| Operación | Caso promedio | Caso peor |
| :--- | :--- | :--- |
| Inserción (*insert*) | $O(1)$ | [cite_start]$O(n)$ [cite: 43] |
| Búsqueda (*search*) | $O(1)$ | [cite_start]$O(n)$ [cite: 43] |
| Eliminación (*delete*) | $O(1)$ | [cite_start]$O(n)$ [cite: 43] |
| Rehash | $O(n)$ | [cite_start]$O(n)$ [cite: 43] |

---

## [cite_start]3. Manejo de Colisiones [cite: 45]
[cite_start]Se emplea **encadenamiento separado** (*separate chaining*): cada índice apunta a una lista enlazada donde conviven los elementos colisionados[cite: 46, 47].

* [cite_start]**Inserción**: Si la clave existe, se actualiza; si no, se inserta al frente de la cadena ($O(1)$)[cite: 48, 49, 50].
* [cite_start]**Búsqueda**: Recorrido lineal de la cadena en el índice calculado[cite: 54, 55].
* [cite_start]**Eliminación**: Se ajustan los punteros para saltar el nodo objetivo[cite: 62, 63, 64].

---

## [cite_start]4. Estrategia de Rehash [cite: 74]
[cite_start]El proceso duplica el tamaño de la tabla y reinserta todos los elementos para mantener la eficiencia[cite: 75].

### [cite_start]4.1 Factor de carga [cite: 77]
Se define mediante la fórmula:
[cite_start]$$factor\_de\_carga = \frac{elementos}{tamaño}$$ [cite: 78, 79]
[cite_start]Al superar **0.75**, se dispara automáticamente el rehash para evitar la degradación del rendimiento hacia $O(n)$[cite: 80, 81, 82].

### [cite_start]4.2 Progresión del tamaño [cite: 97]
| Tamaño tabla | Límite (75%) | Tras rehash | Nuevo límite |
| :--- | :--- | :--- | :--- |
| 16 | 12 elementos | 32 | [cite_start]24 elementos [cite: 98] |
| 32 | 24 elementos | 64 | [cite_start]48 elementos [cite: 98] |
| 64 | 48 elementos | 128 | [cite_start]96 elementos [cite: 98] |

---

## [cite_start]5. Estructura del Proyecto [cite: 99]
[cite_start]El código se organiza siguiendo el principio de responsabilidad única[cite: 100]:

| Archivo | Clase principal | Responsabilidad |
| :--- | :--- | :--- |
| `hashtable.py` | `Node`, `HashTable` | [cite_start]Lógica base y persistencia JSON [cite: 102] |
| `game_data_manager.py` | `GameDataManager` | [cite_start]Abstracción de operaciones del juego [cite: 102] |
| `pygame_game.py` | `PygameGame` | [cite_start]Interfaz gráfica y navegación [cite: 102] |
| `test.py` | `TestSuite` | [cite_start]45 pruebas unitarias [cite: 102] |

### [cite_start]5.1 Persistencia en JSON [cite: 103]
[cite_start]Los datos se guardan en `player_data.json` con la siguiente estructura[cite: 104, 105]:
```json
{
  "tamaño": 16,
  "elementos": 2,
  "factor_carga": 0.125,
  "pares": [
    ["player_1", {"nombre": "Juan", "nivel": 10}],
    ["player_2", {"nombre": "Ana", "nivel": 5}]
  ]
[cite_start]} [cite: 106, 107, 108, 109, 110, 111, 112, 113, 114]
```

### [cite_start]5.2 Resultados de pruebas [cite: 116]
| Categoría | Pruebas | Estado |
| :--- | :--- | :--- |
| Inserción y Búsqueda | 6 | [cite_start]✓ Pasan [cite: 117] |
| Colisiones y Rehash | 12 | [cite_start]✓ Pasan [cite: 117] |
| Persistencia y Gestión | 13 | [cite_start]✓ Pasan [cite: 117] |
| Otros (Borde, Eliminación) | 14 | [cite_start]✓ Pasan [cite: 117] |
| **TOTAL** | **45** | [cite_start]**100% Exitosas** [cite: 117] |

---

## [cite_start]6. Conclusiones [cite: 118]
* [cite_start]El encadenamiento es una estrategia robusta y sencilla para la integridad de datos[cite: 121].
* [cite_start]El rehash a 0.75 garantiza un rendimiento medio de $O(1)$[cite: 122].
* [cite_start]La serialización JSON permite una reconstrucción exacta del estado de la tabla[cite: 123].
* [cite_start]La arquitectura en capas facilita el mantenimiento y las pruebas independientes[cite: 124].