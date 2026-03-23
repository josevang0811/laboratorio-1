
REPORTE TÉCNICO
Sistema de Tabla Hash con Persistencia
para Videojuego



Laboratorio 1 — Manejo de Índices en Archivos
Estructura de Datos 1
Universidad del Norte

Barranquilla, Colombia — 2025
 
1. Introducción
Este reporte documenta el diseño e implementación de una Tabla Hash en Python desarrollada como parte del Laboratorio 1 de Estructura de Datos 1 en la Universidad del Norte. El sistema fue construido desde cero, sin el uso de diccionarios nativos de Python, con el objetivo de comprender profundamente cómo funciona esta estructura de datos fundamental.

La implementación incluye resolución de colisiones por encadenamiento (chaining), rehash automático cuando el factor de carga supera 0.75, persistencia en archivos JSON, y una integración completa con un videojuego simple tanto en versión de consola como en versión gráfica con Pygame.

1.1 Objetivos del sistema
•	Implementar manualmente una tabla hash con encadenamiento.
•	Manejar el rehash automático para mantener rendimiento óptimo.
•	Persistir los datos de jugadores en archivos JSON entre sesiones.
•	Integrar la estructura en un gestor de datos para un videojuego.
•	Validar el comportamiento con una suite de 45 pruebas unitarias.

1.2 Tecnologías utilizadas
Tecnología	Versión	Uso
Python	3.6+	Lenguaje principal del proyecto
Pygame / Pygame-CE	Reciente	Interfaz gráfica del videojuego
JSON (módulo estándar)	—	Persistencia de datos en archivo
pytest (opcional)	—	Ejecución de pruebas unitarias

2. Diseño de la Tabla Hash
La tabla hash fue implementada en el archivo hashtable.py mediante dos clases: Node y HashTable. Cada nodo almacena una clave, un valor y un puntero al nodo siguiente, lo que permite construir listas enlazadas por cada índice de la tabla (chaining).

2.1 Clase Node
Representa cada elemento almacenado en la tabla:
class Node:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None

2.2 Clase HashTable
La clase principal gestiona el arreglo interno, el tamaño de la tabla, el conteo de elementos y el límite de factor de carga. Sus atributos clave son:
•	tamaño: número de cubetas (buckets) disponibles, inicia en 16.
•	tabla: lista de Node o None de longitud igual a tamaño.
•	elementos: contador de pares clave-valor almacenados.
•	factor_carga_limite: umbral de 0.75 que dispara el rehash.

2.3 Función Hash
Se utiliza la función hash() nativa de Python, restringida al rango de la tabla mediante el operador módulo:
def _hash(self, clave):
    return hash(clave) % self.tamaño

Esta función garantiza una distribución razonablemente uniforme de las claves en la tabla, minimizando colisiones bajo condiciones normales.

2.4 Complejidad algorítmica
Operación	Caso promedio	Caso peor
Inserción (insert)	O(1)	O(n)
Búsqueda (search)	O(1)	O(n)
Eliminación (delete)	O(1)	O(n)
Rehash	O(n)	O(n)

El caso peor O(n) ocurre únicamente si todas las claves colisionan en el mismo índice, lo cual es extremadamente improbable con una función hash de calidad.

3. Manejo de Colisiones
Una colisión ocurre cuando dos claves distintas producen el mismo índice al aplicar la función hash. La estrategia elegida para resolverlas es el encadenamiento separado (separate chaining): cada índice de la tabla apunta a una lista enlazada de nodos, de forma que todos los elementos con el mismo índice conviven en una misma cadena.

3.1 Inserción con colisión
Cuando se inserta un elemento y el índice objetivo ya está ocupado, se recorre la cadena en busca de la clave. Si se encuentra, se actualiza su valor. Si no, el nuevo nodo se enlaza al inicio de la cadena (inserción al frente, O(1)):
nuevo_nodo = Node(clave, valor)
nuevo_nodo.siguiente = self.tabla[indice]
self.tabla[indice] = nuevo_nodo

3.2 Búsqueda con colisiones
La búsqueda recorre linealmente la cadena en el índice calculado hasta encontrar la clave coincidente o llegar al final (None):
nodo_actual = self.tabla[indice]
while nodo_actual is not None:
    if nodo_actual.clave == clave:
        return nodo_actual.valor
    nodo_actual = nodo_actual.siguiente
return None

3.3 Eliminación con colisiones
La eliminación distingue dos casos: si el nodo a eliminar es el primero de la cadena, se reemplaza la cabeza por su siguiente. En caso contrario, se recorre con un puntero previo para saltar el nodo eliminado:
# Caso 1: nodo es la cabeza de la cadena
self.tabla[indice] = self.tabla[indice].siguiente
# Caso 2: nodo está en medio o al final
nodo_anterior.siguiente = nodo_actual.siguiente

3.4 Ventajas del chaining
•	No requiere re-probing ni manejo de posiciones secundarias.
•	El factor de carga puede superar 1.0 sin romper la estructura.
•	Las operaciones sobre la cadena son sencillas de implementar y depurar.
•	Funciona bien con tipos de datos complejos como diccionarios Python.

4. Estrategia de Rehash
El rehash es el proceso mediante el cual la tabla duplica su tamaño y reinsertar todos los elementos existentes en las nuevas posiciones. Se activa automáticamente al finalizar cada inserción cuando el factor de carga supera el límite configurado.

4.1 Factor de carga
El factor de carga (load factor) mide qué tan llena está la tabla:
factor_de_carga = elementos / tamaño

Un factor de 0.75 significa que tres cuartas partes de las cubetas están ocupadas. A medida que el factor crece, aumentan las colisiones y se degrada el rendimiento hacia O(n). El umbral elegido (0.75) equilibra uso eficiente de memoria con buen rendimiento.

4.2 Proceso de rehash
El método _rehash() ejecuta los siguientes pasos en orden:
•	Guarda la referencia de la tabla actual y su tamaño.
•	Crea una nueva tabla del doble de tamaño: 4 → 8 → 16 → 32 → ...
•	Reinicia el contador de elementos a 0.
•	Recorre todos los nodos de la tabla antigua y los reinserta usando _insertar_sin_rehash() para evitar recursión.

self.tamaño = self.tamaño * 2
self.tabla = [None] * self.tamaño
self.elementos = 0
for indice in range(tamaño_antiguo):
    nodo = tabla_antigua[indice]
    while nodo is not None:
        self._insertar_sin_rehash(nodo.clave, nodo.valor)
        nodo = nodo.siguiente

4.3 Progresión del tamaño
Tamaño tabla	Límite (75%)	Tras rehash	Nuevo límite
16	12 elementos	32	24 elementos
32	24 elementos	64	48 elementos
64	48 elementos	128	96 elementos
128	96 elementos	256	192 elementos

5. Estructura de Archivos del Proyecto
El proyecto está organizado en cinco archivos principales, cada uno con responsabilidades claramente separadas siguiendo el principio de responsabilidad única.

5.1 Descripción de archivos
Archivo	Clase principal	Responsabilidad
hashtable.py	Node, HashTable	Implementación base: inserción, búsqueda, eliminación, rehash, persistencia JSON
game_data_manager.py	GameDataManager	Capa de abstracción: operaciones específicas del dominio del videojuego sobre la hash table
pygame_game.py	PygameGame	Interfaz gráfica con Pygame: pantallas, botones, entrada de texto, navegación por mouse
test.py	TestSuite	Suite de 45 pruebas unitarias organizadas en 10 categorías
README.md	—	Documentación del proyecto: instalación, uso, conceptos educativos

5.2 Persistencia en JSON
El archivo player_data.json se genera y actualiza automáticamente en cada operación de escritura. La estructura serializada incluye el tamaño de la tabla, el conteo de elementos, el factor de carga y la lista completa de pares clave-valor:
{
  "tamaño": 16,
  "elementos": 2,
  "factor_carga": 0.125,
  "pares": [
    ["player_1", {"nombre": "Juan", "nivel": 10, "puntuacion": 500, "inventario": ["Espada"]}],
    ["player_2", {"nombre": "Ana", "nivel": 5,  "puntuacion": 200, "inventario": []}]
  ]
}

Al cargar el archivo, se reconstruye la tabla con el mismo tamaño original y se reinsertan todos los elementos, garantizando que las claves mapeén al mismo índice gracias a la misma función hash determinista.

5.3 Resultados de pruebas
Categoría	Pruebas	Estado
Inserción básica	4	✓ Todas pasan
Búsqueda fallida	2	✓ Todas pasan
Actualización de valor	3	✓ Todas pasan
Eliminación	4	✓ Todas pasan
Manejo de colisiones	10	✓ Todas pasan
Rehash automático	2	✓ Todas pasan
Persistencia en archivo	7	✓ Todas pasan
GameDataManager	6	✓ Todas pasan
Casos borde	4	✓ Todas pasan
Factor de carga	2	✓ Todas pasan
TOTAL	45	45/45 (100%)

6. Conclusiones
La implementación manual de la tabla hash demostró ser funcional, eficiente y bien integrada en el contexto de un videojuego. Las principales conclusiones del proyecto son:

•	El encadenamiento es una estrategia robusta para manejar colisiones: mantiene la integridad de los datos incluso bajo alta carga y es sencillo de implementar correctamente.
•	El rehash automático a 0.75 de factor de carga mantiene el rendimiento medio en O(1) para todas las operaciones principales, al costo de un rehash periódico de O(n) que ocurre con cada vez menos frecuencia conforme la tabla crece.
•	La serialización a JSON preserva fielmente el estado de la tabla, incluyendo el tamaño original, lo que permite reconstruir la estructura de forma exacta al recargar.
•	La separación en capas (HashTable → GameDataManager → PygameGame) facilita el mantenimiento, la extensibilidad y la prueba unitaria de cada componente de forma independiente.
•	Los 45 tests cubren todos los caminos relevantes del código, incluyendo casos borde como claves vacías, valores None y estructuras de datos anidadas, validando la solidez de la implementación.

