from hashtable import HashTable
import os


class GameDataManager:
    def __init__(self, archivo_persistencia="player_data.json"):
        self.hash_table = HashTable(tamaño_inicial=16)
        self.archivo_persistencia = archivo_persistencia
        if os.path.exists(archivo_persistencia):
            self.hash_table.load_from_file(archivo_persistencia)
    
    def crear_jugador(self, id_jugador, nombre, nivel=1, puntuacion=0, inventario=None):
        if inventario is None:
            inventario = []
        
        datos_jugador = {
            "nombre": nombre,
            "nivel": nivel,
            "puntuacion": puntuacion,
            "inventario": inventario
        }
        if self.hash_table.search(str(id_jugador)) is not None:
            print(f"⚠ Jugador {id_jugador} ya existe. Use actualizar_jugador() para cambiar datos.")
            return False
        
        self.hash_table.insert(str(id_jugador), datos_jugador)
        print(f"✓ Jugador creado: {id_jugador} ({nombre})")
        self._auto_guardar()
        return True
    
    def obtener_jugador(self, id_jugador):
        return self.hash_table.search(str(id_jugador))
    
    def actualizar_jugador(self, id_jugador, nombre=None, nivel=None, puntuacion=None):
        datos = self.obtener_jugador(id_jugador)
        
        if datos is None:
            print(f"⚠ Jugador {id_jugador} no encontrado.")
            return False
        if nombre is not None:
            datos["nombre"] = nombre
        if nivel is not None:
            datos["nivel"] = nivel
        if puntuacion is not None:
            datos["puntuacion"] = puntuacion
        
        self.hash_table.insert(str(id_jugador), datos)
        print(f"✓ Jugador {id_jugador} actualizado.")
        self._auto_guardar()
        return True
    
    def eliminar_jugador(self, id_jugador):
        if self.hash_table.delete(str(id_jugador)):
            print(f"✓ Jugador {id_jugador} eliminado.")
            self._auto_guardar()
            return True
        else:
            print(f"⚠ Jugador {id_jugador} no encontrado.")
            return False
    
    def obtener_inventario(self, id_jugador):
        datos = self.obtener_jugador(id_jugador)
        if datos is None:
            return None
        return datos.get("inventario", [])
    
    def agregar_item_inventario(self, id_jugador, item):
        datos = self.obtener_jugador(id_jugador)
        
        if datos is None:
            print(f"⚠ Jugador {id_jugador} no encontrado.")
            return False
        
        datos["inventario"].append(item)
        self.hash_table.insert(str(id_jugador), datos)
        print(f"✓ Item '{item}' agregado al inventario de {id_jugador}.")
        self._auto_guardar()
        return True
    
    def remover_item_inventario(self, id_jugador, item):
        datos = self.obtener_jugador(id_jugador)
        
        if datos is None:
            print(f"⚠ Jugador {id_jugador} no encontrado.")
            return False
        
        if item not in datos["inventario"]:
            print(f"⚠ Item '{item}' no encontrado en inventario de {id_jugador}.")
            return False
        
        datos["inventario"].remove(item)
        self.hash_table.insert(str(id_jugador), datos)
        print(f"✓ Item '{item}' removido del inventario de {id_jugador}.")
        self._auto_guardar()
        return True
    
    def listar_todos_jugadores(self):
        return self.hash_table.get_all()
    
    def obtener_estadisticas(self):
        return {
            "tamaño": self.hash_table.tamaño,
            "elementos": self.hash_table.elementos,
            "factor_carga": self.hash_table._calcular_factor_carga(),
            "total_jugadores": self.hash_table.elementos
        }
    
    def _auto_guardar(self):
        self.hash_table.save_to_file(self.archivo_persistencia)
    
    def guardar(self):
        self.hash_table.save_to_file(self.archivo_persistencia)
    
    def cargar(self):
        self.hash_table.load_from_file(self.archivo_persistencia)
