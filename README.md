# 🎮 Hash Table con Persistencia para Videojuego

> Implementación manual de una Tabla Hash en Python con encadenamiento, rehash automático y persistencia JSON — desarrollada como parte del Laboratorio 1 de Estructura de Datos 1 en la **Universidad del Norte**, Barranquilla, Colombia.

---

## 📋 Descripción

Este proyecto implementa una **Tabla Hash desde cero** en Python (sin usar diccionarios nativos), integrada como sistema de gestión de datos para un videojuego disponible en versión de consola y versión gráfica con Pygame.

La implementación incluye:
- ✅ Resolución de colisiones por **encadenamiento separado** (chaining)
- ✅ **Rehash automático** cuando el factor de carga supera 0.75
- ✅ **Persistencia** de datos en archivos JSON entre sesiones
- ✅ Integración con **interfaz gráfica** (Pygame)
- ✅ Suite de **45 pruebas unitarias** con 100% de éxito

---

## 🛠️ Tecnologías

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.6+ | Lenguaje principal del proyecto |
| Pygame / Pygame-CE | Reciente | Interfaz gráfica del videojuego |
| JSON (módulo estándar) | — | Persistencia de datos en archivo |
| pytest (opcional) | — | Ejecución de pruebas unitarias |

---

## 📁 Estructura del Proyecto

```
proyecto/
│
├── hashtable.py          # Implementación base: Node y HashTable
├── game_data_manager.py  # Capa de abstracción para el videojuego
├── pygame_game.py        # Interfaz gráfica con Pygame
├── test.py               # Suite de 45 pruebas unitarias
├── player_data.json      # Archivo de persistencia (generado automáticamente)
└── README.md             # Este archivo
```

### Descripción de archivos

| Archivo | Clase principal | Responsabilidad |
|---|---|---|
| `hashtable.py` | `Node`, `HashTable` | Inserción, búsqueda, eliminación, rehash y persistencia JSON |
| `game_data_manager.py` | `GameDataManager` | Operaciones específicas del dominio del videojuego |
| `pygame_game.py` | `PygameGame` | Pantallas, botones, entrada de texto y navegación |
| `test.py` | `TestSuite` | 45 pruebas organizadas en 10 categorías |

---

## 🚀 Instalación y Uso

### Requisitos previos

```bash
pip install pygame
# o para Pygame-CE:
pip install pygame-ce
```

### Ejecutar el juego (versión gráfica)

```bash
python pygame_game.py
```

### Ejecutar las pruebas unitarias

```bash
python test.py
# o con pytest:
pytest test.py -v
```

---

## ⚙️ Diseño de la Tabla Hash

### Clase `Node`

Cada nodo almacena una clave, un valor y un puntero al siguiente nodo, formando listas enlazadas por índice (chaining):

```python
class Node:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None
```

### Clase `HashTable`

| Atributo | Descripción |
|---|---|
| `tamaño` | Número de cubetas (buckets), inicia en 16 |
| `tabla` | Lista de `Node` o `None` |
| `elementos` | Contador de pares clave-valor almacenados |
| `factor_carga_limite` | Umbral de 0.75 que dispara el rehash |

### Función Hash

```python
def _hash(self, clave):
    return hash(clave) % self.tamaño
```

### Complejidad Algorítmica

| Operación | Caso promedio | Caso peor |
|---|---|---|
| Inserción (`insert`) | O(1) | O(n) |
| Búsqueda (`search`) | O(1) | O(n) |
| Eliminación (`delete`) | O(1) | O(n) |
| Rehash | O(n) | O(n) |

> El caso peor O(n) ocurre únicamente si todas las claves colisionan en el mismo índice, lo cual es extremadamente improbable con una función hash de calidad.

---

## 🔗 Manejo de Colisiones (Chaining)

Cuando dos claves producen el mismo índice, los nodos se encadenan en una lista enlazada. El nuevo nodo se inserta al frente de la cadena (O(1)):

```python
nuevo_nodo = Node(clave, valor)
nuevo_nodo.siguiente = self.tabla[indice]
self.tabla[indice] = nuevo_nodo
```

**Ventajas del chaining:**
- No requiere re-probing ni manejo de posiciones secundarias
- El factor de carga puede superar 1.0 sin romper la estructura
- Funciona bien con tipos de datos complejos como diccionarios Python

---

## 🔄 Rehash Automático

El rehash se activa cuando el factor de carga supera 0.75, duplicando el tamaño de la tabla:

```python
self.tamaño = self.tamaño * 2
self.tabla = [None] * self.tamaño
self.elementos = 0
for indice in range(tamaño_antiguo):
    nodo = tabla_antigua[indice]
    while nodo is not None:
        self._insertar_sin_rehash(nodo.clave, nodo.valor)
        nodo = nodo.siguiente
```

### Progresión del tamaño

| Tamaño tabla | Límite (75%) | Tras rehash | Nuevo límite |
|---|---|---|---|
| 16 | 12 elementos | 32 | 24 elementos |
| 32 | 24 elementos | 64 | 48 elementos |
| 64 | 48 elementos | 128 | 96 elementos |
| 128 | 96 elementos | 256 | 192 elementos |

---

## 💾 Persistencia en JSON

Los datos se guardan automáticamente en `player_data.json` tras cada operación de escritura:

```json
{
  "tamaño": 16,
  "elementos": 2,
  "factor_carga": 0.125,
  "pares": [
    ["player_1", {"nombre": "Juan", "nivel": 10, "puntuacion": 500, "inventario": ["Espada"]}],
    ["player_2", {"nombre": "Ana", "nivel": 5, "puntuacion": 200, "inventario": []}]
  ]
}
```

Al recargar, la tabla se reconstruye con el mismo tamaño original para garantizar que las claves mapeen al mismo índice.

---

## 🧪 Resultados de Pruebas

| Categoría | Pruebas | Estado |
|---|---|---|
| Inserción básica | 4 | ✅ Todas pasan |
| Búsqueda fallida | 2 | ✅ Todas pasan |
| Actualización de valor | 3 | ✅ Todas pasan |
| Eliminación | 4 | ✅ Todas pasan |
| Manejo de colisiones | 10 | ✅ Todas pasan |
| Rehash automático | 2 | ✅ Todas pasan |
| Persistencia en archivo | 7 | ✅ Todas pasan |
| GameDataManager | 6 | ✅ Todas pasan |
| Casos borde | 4 | ✅ Todas pasan |
| Factor de carga | 2 | ✅ Todas pasan |
| **TOTAL** | **45** | **✅ 45/45 (100%)** |

---

## 📌 Conclusiones

- El **encadenamiento** es una estrategia robusta para colisiones: mantiene la integridad de los datos incluso bajo alta carga.
- El **rehash automático a 0.75** mantiene el rendimiento medio en O(1) para todas las operaciones principales.
- La **serialización a JSON** preserva el estado de la tabla (incluyendo el tamaño original) para una reconstrucción exacta.
- La **separación en capas** (`HashTable → GameDataManager → PygameGame`) facilita el mantenimiento y la prueba unitaria independiente de cada componente.

---

## 👤 Autor
- Jose Fernando Van strahlen Garcia
- Daniela Idarraga Gómez
- Jesús Darío Esguerra Fernández
- Jairo Luis Hernández Carvajal
Proyecto desarrollado para el **Laboratorio 1 — Manejo de Índices en Archivos**  
Materia: Estructura de Datos 1  
Universidad del Norte — Barranquilla, Colombia, 2025
