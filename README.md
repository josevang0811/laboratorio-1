# [cite_start]REPORTE TÉCNICO [cite: 1]
## [cite_start]Sistema de Tabla Hash con Persistencia para Videojuego [cite: 2, 3]

[cite_start]**Laboratorio 1 — Manejo de Índices en Archivos** [cite: 4]  
[cite_start]**Estructura de Datos 1** [cite: 5]  
[cite_start]**Universidad del Norte** [cite: 6]  
[cite_start]*Barranquilla, Colombia — 2025* [cite: 7]

---

## 1. Introducción
[cite_start]Este reporte documenta el diseño e implementación de una **Tabla Hash en Python** desarrollada como parte del Laboratorio 1[cite: 9]. [cite_start]El sistema fue construido desde cero, sin el uso de diccionarios nativos de Python, con el objetivo de comprender profundamente esta estructura de datos[cite: 10]. 

[cite_start]La implementación incluye resolución de colisiones por encadenamiento (*chaining*), rehash automático cuando el factor de carga supera **0.75**, persistencia en archivos JSON e integración con un videojuego en versiones de consola y gráfica (Pygame)[cite: 11].

### 1.1 Objetivos del sistema
* [cite_start]Implementar manualmente una tabla hash con encadenamiento[cite: 13].
* [cite_start]Manejar el rehash automático para mantener rendimiento óptimo[cite: 14].
* [cite_start]Persistir los datos de jugadores en archivos JSON entre sesiones[cite: 15].
* [cite_start]Integrar la estructura en un gestor de datos para un videojuego[cite: 16].
* [cite_start]Validar el comportamiento con una suite de **45 pruebas unitarias**[cite: 17].

### 1.2 Tecnologías utilizadas
| Tecnología | Versión | Uso |
| :--- | :--- | :--- |
| [cite_start]**Python** [cite: 19] | [cite_start]3.6+ [cite: 19] | [cite_start]Lenguaje principal del proyecto [cite: 19] |
| [cite_start]**Pygame / Pygame-CE** [cite: 19] | [cite_start]Reciente [cite: 19] | [cite_start]Interfaz gráfica del videojuego [cite: 19] |
| [cite_start]**JSON** [cite: 19] | [cite_start]Estándar [cite: 19] | [cite_start]Persistencia de datos en archivo [cite: 19] |
| [cite_start]**pytest** [cite: 19] | [cite_start]— [cite: 19] | [cite_start]Ejecución de pruebas unitarias [cite: 19] |

---

## 2. Diseño de la Tabla Hash
[cite_start]La tabla fue implementada en el archivo `hashtable.py` mediante las clases `Node` y `HashTable`[cite: 21]. [cite_start]Se utilizan listas enlazadas en cada índice para gestionar el encadenamiento[cite: 22].

### 2.1 Clase Node
[cite_start]Representa cada elemento almacenado en la tabla[cite: 24]:
```python
class Node:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        [cite_start]self.siguiente = None [cite: 25, 26, 27, 28, 29]
```

### 2.2 Clase HashTable
[cite_start]Gestiona el arreglo interno, el tamaño, el conteo de elementos y el límite del factor de carga[cite: 31]. Sus atributos clave son:
* [cite_start]**tamaño**: número de cubetas disponibles (inicia en 16)[cite: 33].
* [cite_start]**tabla**: lista de objetos `Node` o `None`[cite: 34].
* [cite_start]**elementos**: contador de pares almacenados[cite: 35].
* [cite_start]**factor_carga_limite**: umbral fijo de **0.75** que dispara el rehash[cite: 36].

### 2.3 Función Hash
[cite_start]Se utiliza la función `hash()` nativa de Python restringida al rango de la tabla mediante el operador módulo[cite: 38]:
[cite_start]$$\text{índice} = \text{hash}(\text{clave}) \pmod{\text{self.tamaño}} [cite: 39, 40]$$

### 2.4 Complejidad algorítmica
| Operación | Caso promedio | Caso peor |
| :--- | :--- | :--- |
| **Inserción** (*insert*) | [cite_start]$O(1)$ [cite: 43] | [cite_start]$O(n)$ [cite: 43] |
| **Búsqueda** (*search*) | [cite_start]$O(1)$ [cite: 43] | [cite_start]$O(n)$ [cite: 43] |
| **Eliminación** (*delete*) | [cite_start]$O(1)$ [cite: 43] | [cite_start]$O(n)$ [cite: 43] |
| **Rehash** | [cite_start]$O(n)$ [cite: 43] | [cite_start]$O(n)$ [cite: 43] |

---

## 3. Manejo de Colisiones
[cite_start]Se emplea **encadenamiento separado** (*separate chaining*): cada índice apunta a una lista enlazada donde conviven los elementos colisionados[cite: 47].

* [cite_start]**Inserción**: Si la clave ya existe, se actualiza; si no, el nuevo nodo se enlaza al inicio de la cadena (inserción al frente, $O(1)$)[cite: 49, 50, 53].
* [cite_start]**Búsqueda**: Recorrido lineal de la cadena en el índice calculado hasta encontrar la coincidencia[cite: 55, 61].
* [cite_start]**Eliminación**: Se ajustan los punteros para saltar el nodo a eliminar (usando un puntero previo si es necesario)[cite: 63, 64].

---

## 4. Estrategia de Rehash
[cite_start]El rehash duplica el tamaño de la tabla y reinserta todos los elementos para mantener la eficiencia[cite: 75]. [cite_start]Se activa automáticamente cuando el factor de carga supera el **0.75**[cite: 76, 82].

* [cite_start]**Factor de carga**: mide qué tan llena está la tabla mediante la fórmula $\text{elementos} / \text{tamaño}$[cite: 78, 79].
* [cite_start]**Proceso**: Crea una nueva tabla del doble de tamaño y reinserta los nodos usando un método que evita la recursión[cite: 84, 86, 88].

---

## 5. Estructura del Proyecto
[cite_start]El proyecto se organiza en archivos con responsabilidades separadas[cite: 100]:

| Archivo | Clase principal | Responsabilidad |
| :--- | :--- | :--- |
| [cite_start]`hashtable.py` [cite: 102] | [cite_start]`HashTable` [cite: 102] | [cite_start]Lógica base, rehash y persistencia JSON [cite: 102] |
| [cite_start]`game_data_manager.py` [cite: 102] | [cite_start]`GameDataManager` [cite: 102] | [cite_start]Operaciones específicas del videojuego [cite: 102] |
| [cite_start]`pygame_game.py` [cite: 102] | [cite_start]`PygameGame` [cite: 102] | [cite_start]Interfaz gráfica y navegación [cite: 102] |
| [cite_start]`test.py` [cite: 102] | [cite_start]`TestSuite` [cite: 102] | [cite_start]Suite de 45 pruebas unitarias [cite: 102] |

### 5.1 Persistencia en JSON
[cite_start]El archivo `player_data.json` se actualiza en cada escritura[cite: 104]. [cite_start]Al cargar, se reconstruye la tabla con el mismo tamaño original para asegurar que el mapeo de índices sea idéntico[cite: 115].

---

## 6. Conclusiones
* [cite_start]El encadenamiento mantiene la integridad de los datos incluso bajo alta carga[cite: 121].
* [cite_start]El rehash a **0.75** garantiza un rendimiento medio de $O(1)$ para operaciones principales[cite: 122].
* [cite_start]La serialización JSON preserva fielmente el estado y tamaño original de la tabla[cite: 123].
* [cite_start]La arquitectura en capas facilita el mantenimiento y las pruebas independientes de cada componente[cite: 124].
* [cite_start]Se validó la solidez del sistema superando el **100% de las 45 pruebas unitarias**[cite: 117, 125].