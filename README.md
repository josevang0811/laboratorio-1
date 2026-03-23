# Sistema de Tabla Hash con Persistencia para Videojuego

## Descripción General

Implementación manual de una **Tabla Hash** en Python con:
- ✅ Resolución de colisiones por encadenamiento (chaining)
- ✅ Rehash automático cuando factor de carga > 0.75
- ✅ Persistencia en archivos JSON
- ✅ Integración con un videojuego simple
- ✅ Suite completa de 45 pruebas unitarias

**Objetivo**: Aprender cómo funcionan las estructuras de datos de tabla hash mientras se implementa un sistema de almacenamiento para datos de jugadores en un videojuego.

---

## Archivos del Proyecto

### 1. **hashtable.py** - Implementación Base
- Clase `Node`: Nodos para encadenamiento
- Clase `HashTable`: Tabla hash con métodos:
  - `insert(clave, valor)` - Inserta/actualiza
  - `search(clave)` - Busca un elemento
  - `delete(clave)` - Elimina un elemento
  - `save_to_file()` - Guarda a JSON
  - `load_from_file()` - Carga desde JSON
  - `_rehash()` - Duplica tamaño automáticamente

### 2. **game_data_manager.py** - Gestor de Datos
- Clase `GameDataManager`: Encapsula la tabla hash
- Métodos específicos del juego:
  - `crear_jugador()`, `obtener_jugador()`, `actualizar_jugador()`, `eliminar_jugador()`
  - `agregar_item_inventario()`, `remover_item_inventario()`
  - `obtener_estadisticas()`, `guardar()`, `cargar()`

### 3. **game.py** - Videojuego Interactivo
- Clase `SimpleGame`: Loop principal con menú de texto
- 9 opciones de interacción:
  1. Crear jugador
  2. Ver jugador
  3. Actualizar jugador
  4. Agregar item al inventario
  5. Remover item del inventario
  6. Listar todos los jugadores
  7. Eliminar jugador
  8. Ver estadísticas de tabla hash
  9. Guardar datos

### 4. **test.py** - Suite de Pruebas
- 10 categorías de pruebas (45 pruebas totales):
  1. Inserción básica
  2. Búsqueda fallida
  3. Actualización de valor
  4. Eliminación
  5. Manejo de colisiones
  6. Rehash automático
  7. Persistencia en archivo
  8. GameDataManager
  9. Casos borde
  10. Factor de carga

---

## Requisitos

- Python 3.6 o superior
- **Para versión gráfica (Pygame):** Instalar dependencias adicionales
- Ninguna librería externa necesaria para la versión de texto (solo módulos estándar)

## Instalación

### Versión Básica (Texto)
```bash
# No requiere instalación adicional
python game.py
```

### Versión con Pygame (Gráfica)
```bash
# Instalar pygame-ce (recomendado para Python 3.14+)
pip install pygame-ce

# O instalar desde requirements.txt
pip install -r requirements.txt

# Ejecutar juego gráfico
python pygame_game.py
```

✅ **Compatible con Python 3.14:** Se recomienda usar `pygame-ce` (Community Edition) que tiene mejor soporte para versiones modernas de Python.

#### **Características de la Versión Pygame:**
- ✅ Interfaz visual con botones y menús
- ✅ Entrada de texto interactiva
- ✅ Navegación por mouse
- ✅ Pantallas separadas para cada función
- ✅ **Manejo visual de errores y mensajes de éxito**
- ✅ **Mensajes temporales que desaparecen automáticamente**
- ✅ Estadísticas visuales de la tabla hash
- ✅ **Mismo sistema de datos** que versión texto

**Características de la versión gráfica:**
- ✅ Interfaz visual con botones y menús
- ✅ Entrada de texto interactiva
- ✅ Navegación por mouse
- ✅ Pantallas separadas para cada función
- ✅ Estadísticas visuales de la tabla hash

---

## Uso

### Opción 1: Ejecutar las Pruebas

```bash
python test.py
```

**Salida esperada**:
```
✓ ¡TODAS LAS PRUEBAS PASARON! 🎉
RESUMEN: 45/45 pruebas pasadas
```

### Opción 2: Ejecutar el Videojuego (Texto)

```bash
python game.py
```

**Ejemplo de flujo**:
```
⚔️  VIDEOJUEGO - GESTOR DE DATOS CON TABLA HASH  ⚔️

╔════════════════════════════════════════╗
║         MENÚ PRINCIPAL                 ║
╠════════════════════════════════════════╣
║  1. Crear jugador                     ║
║  2. Ver jugador                       ║
│  ... (más opciones)
│  0. Salir                             ║
╚════════════════════════════════════════╝

Seleccione una opción: 1

--- Crear Jugador ---
Ingrese ID del jugador: player_1
Ingrese nombre del jugador: Juan
Ingrese nivel inicial (por defecto 1): 10
Ingrese puntuación inicial (por defecto 0): 500

✓ Jugador creado: player_1 (Juan)
✓ Tabla hash guardada en: player_data.json
```

### Opción 3: Ejecutar el Videojuego (Gráfico con Pygame)

#### **Método Fácil (Recomendado):**
```bash
python launch_game.py
```
*Este script verifica dependencias automáticamente y lanza el juego.*

#### **Método Manual:**
```bash
# Instalar pygame-ce
pip install pygame-ce

# Ejecutar juego gráfico
python pygame_game.py
```

**Características de la versión gráfica:**
- ✅ Interfaz visual con botones y menús
- ✅ Entrada de texto interactiva
- ✅ Navegación por mouse
- ✅ Pantallas separadas para cada función
- ✅ Mismo sistema de datos que la versión de texto
- ✅ Estadísticas visuales de la tabla hash

**Controles:**
- **Mouse:** Click en botones y cajas de texto
- **Teclado:** Escribir en campos de entrada
- **Enter:** Confirmar entrada de texto

---

## Archivos Adicionales para Pygame

### **pygame_game.py** - Componentes Principales

#### 1. **Inicialización de Pygame**
```python
pygame.init()
self.screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Videojuego - Tabla Hash")
```

#### 2. **Sistema de Pantallas**
- **Menu principal:** Crear/cargar jugador, ver estadísticas
- **Creación de jugador:** Formulario con entrada de texto
- **Pantalla de juego:** Información del jugador, acciones disponibles
- **Inventario:** Lista visual de items
- **Estadísticas:** Información de la tabla hash

#### 3. **Controles Interactivos**
- **Botones:** Click para navegación
- **Cajas de texto:** Entrada de nombres e items
- **Eventos:** Manejo de mouse y teclado

#### 4. **Integración con Tabla Hash**
- ✅ Mismo `GameDataManager` que versión de texto
- ✅ Persistencia automática en `player_data.json`
- ✅ Estadísticas visuales de la tabla hash
- ✅ Rehash automático cuando aplica

### **Diferencias entre Versiones**

| Característica | Versión Texto | Versión Pygame |
|----------------|----------------|----------------|
| Interfaz | Consola/texto | Gráfica/GUI |
| Controles | Números/teclado | Mouse/teclado |
| Navegación | Menú numérico | Botones visuales |
| Entrada | input() | Cajas de texto |
| Sistema de datos | ✅ Idéntico | ✅ Idéntico |
| Persistencia | ✅ JSON | ✅ JSON |
| Estadísticas | Texto | Visual |

### **Ventajas de la Versión Pygame**
- 🎨 **Interfaz moderna** y atractiva
- 🖱️ **Navegación intuitiva** por mouse
- 📊 **Visualización clara** de datos
- 🎯 **Experiencia de usuario** mejorada
- 📱 **Preparado para expansión** (imágenes, animaciones, sonido)

---

## Conceptos Clave Implementados

### 1. Tabla Hash (Hash Table)
- Estructura que mapea claves a valores usando una función hash
- Tiempo medio O(1) para inserción, búsqueda y eliminación
- Función hash: `índice = hash(clave) % tamaño`

### 2. Colisiones
- Ocurren cuando dos claves mapean al mismo índice
- **Solución**: Encadenamiento (Chaining)
  - Cada posición contiene una lista enlazada de nodos
  - Todos los elementos con colisión se almacenan en la misma cadena

### 3. Factor de Carga (Load Factor)
```
Factor de Carga = Elementos / Tamaño
```
- Mide qué tan llena está la tabla
- Cuando > 0.75 → Se dispara un rehash automático

### 4. Rehash (Remapping)
- Duplica el tamaño de la tabla (4 → 8 → 16 → 32...)
- Reinserta todos los elementos en las nuevas posiciones
- Reduce colisiones y mantiene O(1) en operaciones

### 5. Persistencia
- Serializa la tabla hash a JSON para guardar estado
- Reconstruye la tabla al cargar desde archivo
- Permite que los datos de jugadores persistan entre sesiones

---

## Ejemplo de Datos en JSON

**Archivo: player_data.json**
```json
{
  "tamaño": 16,
  "elementos": 2,
  "factor_carga": 0.12,
  "pares": [
    [
      "player_1",
      {
        "nombre": "Juan",
        "nivel": 10,
        "puntuacion": 500,
        "inventario": ["Espada", "Escudo"]
      }
    ],
    [
      "player_2",
      {
        "nombre": "Ana",
        "nivel": 5,
        "puntuacion": 200,
        "inventario": []
      }
    ]
  ]
}
```

---

## Complejidad Algorítmica

| Operación | Casos mejor/promedio | Caso peor |
|-----------|----------------------|-----------|
| Inserción | O(1) | O(n) |
| Búsqueda | O(1) | O(n) |
| Eliminación | O(1) | O(n) |
| Rehash | O(n) | O(n) |

*Nota: El caso peor ocurre cuando todas las claves colisionan (muy raro con buen hash)*

---

## Cómo Funciona la Tabla Hash

### Ejemplo: Inserción con Colisión

```
Tabla inicial (tamaño 4):
┌──────┐
│ null │ índice 0
├──────┤
│ null │ índice 1
├──────┤
│ null │ índice 2
├──────┤
│ null │ índice 3
└──────┘

Insertar ("Juan", {"edad": 25}):
  hash("Juan") % 4 = 2
  
┌──────┐
│ null │ índice 0
├──────┤
│ null │ índice 1
├──────┤
│ "Juan" → {"edad": 25} │ índice 2
├──────┤
│ null │ índice 3
└──────┘

Insertar ("Carlos", {"edad": 30}):
  hash("Carlos") % 4 = 2  // ¡COLISIÓN!
  
  Agregar al inicio de la cadena:
  
┌──────────────────────────────────────┐
│ null                                 │ índice 0
├──────────────────────────────────────┤
│ null                                 │ índice 1
├──────────────────────────────────────┤
│ "Carlos" → {"edad": 30}              │ índice 2
│   ↓ siguiente                        │
│ "Juan" → {"edad": 25}                │
├──────────────────────────────────────┤
│ null                                 │ índice 3
└──────────────────────────────────────┘
```

---

## Validación y Pruebas

Todas las pruebas están automatizadas en **test.py**:

```bash
python test.py
```

**Categorías probadas**:
- ✓ Inserción y búsqueda
- ✓ Eliminación
- ✓ Colisiones y encadenamiento
- ✓ Rehash automático
- ✓ Persistencia en archivos
- ✓ Integración con GameDataManager
- ✓ Casos borde (claves especiales, valores None, etc.)
- ✓ Cálculo de factor de carga

---

## Notas Educativas

Este código está pensado para estudiantes de **Estructura de Datos 1** y mantiene:

✅ **Simplicidad**: Código claro y fácil de seguir
✅ **Comentarios**: Explicaciones en español
✅ **Modularidad**: Separación de responsabilidades
✅ **Documentación**: Docstrings en todas las funciones
✅ **Pruebas**: Suite completa para validar funcionamiento
✅ **Aplicación práctica**: Integración con videojuego real

---

## Posibles Extensiones

1. **Hashing mejorado**: Implementar función hash personalizada
2. **Probing abierto**: Usar direccionamiento abierto en lugar de encadenamiento
3. **Tabla dinámica**: Ajustar factor de carga dinámicamente
4. **Estadísticas**: Contar colisiones, medir rendimiento
5. **Juego mejorado**: Agregar géneros, mecánicas, puntuación basada en tiempo
6. **Base de datos**: Reemplazar JSON con SQLite

---

## Autor

Laboratorio 1 - Manejo de Índices en Archivos  
Estructura de Datos 1  
Universidad del Norte

---

**¡Ahora estás listo para comprender cómo funcionan las tablas hash!** 🚀
