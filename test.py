import os
from hashtable import HashTable, Node
from game_data_manager import GameDataManager


class TestSuite:
    def __init__(self):
        self.pruebas_ejecutadas = 0
        self.pruebas_pasadas = 0
        self.archivo_test = "test_data.json"
    
    def limpiar_archivos(self):
        #elimina archivos de prueba si existen
        if os.path.exists(self.archivo_test):
            os.remove(self.archivo_test)
    
    def assert_igual(self, actual, esperado, mensaje=""):
        #verifica que dos valores sean iguales
        self.pruebas_ejecutadas += 1
        if actual == esperado:
            self.pruebas_pasadas += 1
            print(f"  ✓ {mensaje}")
            return True
        else:
            print(f"  ✗ {mensaje}")
            print(f"    Esperado: {esperado}")
            print(f"    Actual: {actual}")
            return False
    
    def assert_verdadero(self, condicion, mensaje=""):
        #verifica que una condición sea verdadera
        self.pruebas_ejecutadas += 1
        if condicion:
            self.pruebas_pasadas += 1
            print(f"  ✓ {mensaje}")
            return True
        else:
            print(f"  ✗ {mensaje}")
            return False
    
    def test_insercion_basica(self):
        #prueba insercion básica en tabla hash
        print("\n[TEST 1] Inserción Básica")
        
        hash_table = HashTable(tamaño_inicial=4)
        hash_table.insert("nombre", "Juan")
        hash_table.insert("edad", 25)
        hash_table.insert("ciudad", "Barranquilla")
        
        self.assert_igual(hash_table.elementos, 3, "Debe haber 3 elementos")
        self.assert_igual(hash_table.search("nombre"), "Juan", "Buscar 'nombre' debe retornar 'Juan'")
        self.assert_igual(hash_table.search("edad"), 25, "Buscar 'edad' debe retornar 25")
        self.assert_igual(hash_table.search("ciudad"), "Barranquilla", "Buscar 'ciudad' debe retornar 'Barranquilla'")
    
    def test_busqueda_fallida(self):
        #prueba búsqueda de claves inexistentes
        print("\n[TEST 2] Búsqueda Fallida")
        
        hash_table = HashTable(tamaño_inicial=4)
        hash_table.insert("clave1", "valor1")
        
        self.assert_igual(hash_table.search("clave_inexistente"), None, "Buscar clave inexistente debe retornar None")
        self.assert_igual(hash_table.search(""), None, "Buscar clave vacía debe retornar None")
    
    def test_actualizacion_valor(self):
        #prueba actualización de valores para claves existentes
        print("\n[TEST 3] Actualización de Valor")
        
        hash_table = HashTable(tamaño_inicial=4)
        hash_table.insert("jugador", {"nombre": "Ana", "puntos": 100})
        self.assert_igual(hash_table.search("jugador")["puntos"], 100, "Puntos iniciales: 100")
        
        datos = hash_table.search("jugador")
        datos["puntos"] = 150
        hash_table.insert("jugador", datos)
        
        self.assert_igual(hash_table.search("jugador")["puntos"], 150, "Puntos actualizados: 150")
        self.assert_igual(hash_table.elementos, 1, "Debe seguir habiendo 1 elemento")
    
    def test_eliminacion(self):
        #prueba eliminación de elementos
        print("\n[TEST 4] Eliminación")
        
        hash_table = HashTable(tamaño_inicial=4)
        hash_table.insert("item1", "valor1")
        hash_table.insert("item2", "valor2")
        hash_table.insert("item3", "valor3")
        
        self.assert_igual(hash_table.elementos, 3, "Debe haber 3 elementos")
        
        resultado = hash_table.delete("item2")
        self.assert_verdadero(resultado, "Eliminación de 'item2' debe retornar True")
        self.assert_igual(hash_table.elementos, 2, "Debe haber 2 elementos después de eliminar")
        self.assert_igual(hash_table.search("item2"), None, "'item2' no debe encontrarse")
        
        resultado_falso = hash_table.delete("item_inexistente")
        self.assert_verdadero(not resultado_falso, "Eliminar elemento inexistente debe retornar False")
    
    def test_colisiones(self):
        #prueba manejo de colisiones por encadenamiento
        print("\n[TEST 5] Manejo de Colisiones")
        hash_table = HashTable(tamaño_inicial=4)
        
        for i in range(10):
            hash_table.insert(f"clave_{i}", f"valor_{i}")

        for i in range(10):
            valor = hash_table.search(f"clave_{i}")
            self.assert_igual(valor, f"valor_{i}", f"Buscar clave_{i} con colisiones")
    
    def test_rehash(self):
        #prueba que el rehash ocurra automáticamente
        print("\n[TEST 6] Rehash Automático")
        
        hash_table = HashTable(tamaño_inicial=4)
        tamaño_inicial = hash_table.tamaño
        
        print(f"\n  Tamaño inicial: {tamaño_inicial}")
        elementos_necesarios = int(tamaño_inicial * 0.75) + 1
        for i in range(elementos_necesarios + 5):
            hash_table.insert(f"elemento_{i}", f"valor_{i}")
        
        print(f"  Tamaño después de {hash_table.elementos} insertiones: {hash_table.tamaño}")
        
        self.assert_verdadero(hash_table.tamaño > tamaño_inicial, "Tamaño debe ser mayor después de rehash")
        todos_encontrados = True
        for i in range(hash_table.elementos):
            if hash_table.search(f"elemento_{i}") is None:
                todos_encontrados = False
                break
        
        self.assert_verdadero(todos_encontrados, "Todos los elementos deben encontrarse después de rehash")
    
    def test_persistencia(self):
    #prueba guardar y cargar desde archivo
        print("\n[TEST 7] Persistencia en Archivo")
        
        self.limpiar_archivos()
        hash_table_1 = HashTable(tamaño_inicial=8)
        for i in range(5):
            hash_table_1.insert(f"dato_{i}", {"valor": i * 10})
        
        print(f"\n  Guardando tabla con {hash_table_1.elementos} elementos...")
        hash_table_1.save_to_file(self.archivo_test)
        hash_table_2 = HashTable(tamaño_inicial=16)
        hash_table_2.load_from_file(self.archivo_test)
        
        self.assert_igual(hash_table_2.elementos, hash_table_1.elementos, "Elementos después de cargar")
        self.assert_igual(hash_table_2.tamaño, hash_table_1.tamaño, "Tamaño después de cargar")
        for i in range(5):
            valor_guardado = hash_table_1.search(f"dato_{i}")
            valor_cargado = hash_table_2.search(f"dato_{i}")
            self.assert_igual(valor_cargado, valor_guardado, f"Dato {i} debe ser igual después de cargar")
        
        self.limpiar_archivos()
    
    def test_game_data_manager(self):
        #prueba el gestor de datos del jueo
        print("\n[TEST 8] GameDataManager")
        
        self.limpiar_archivos()
        
        manager = GameDataManager(self.archivo_test)
        manager.crear_jugador("p1", "Player 1", nivel=10, puntuacion=500)
        manager.crear_jugador("p2", "Player 2", nivel=5, puntuacion=200)
        
        self.assert_igual(len(manager.listar_todos_jugadores()), 2, "Debe haber 2 jugadores")
        manager.agregar_item_inventario("p1", "Espada")
        manager.agregar_item_inventario("p1", "Escudo")
        
        inventario = manager.obtener_inventario("p1")
        self.assert_igual(len(inventario), 2, "Inventario debe tener 2 items")
        self.assert_verdadero("Espada" in inventario, "Inventario debe contener 'Espada'")
        manager.remover_item_inventario("p1", "Espada")
        inventario = manager.obtener_inventario("p1")
        self.assert_igual(len(inventario), 1, "Inventario debe tener 1 item después de remover")
        manager.actualizar_jugador("p1", puntuacion=1000)
        datos = manager.obtener_jugador("p1")
        self.assert_igual(datos["puntuacion"], 1000, "Puntuación debe ser actualizada")
        manager.eliminar_jugador("p2")
        self.assert_igual(len(manager.listar_todos_jugadores()), 1, "Debe quedar 1 jugador después de eliminar")
        
        self.limpiar_archivos()
    
    def test_casos_borde(self):
        #prueba casos borde y situaciones especiales
        print("\n[TEST 9] Casos Borde")
        
        hash_table = HashTable(tamaño_inicial=4)
        hash_table.insert("", "valor_vacio")
        self.assert_igual(hash_table.search(""), "valor_vacio", "Debe permitir clave vacía")
        hash_table.insert("clave_none", None)
        self.assert_igual(hash_table.search("clave_none"), None, "Debe permitir valor None")
        hash_table.insert("clave#especial@2025", {"tipo": "especial"})
        self.assert_igual(hash_table.search("clave#especial@2025")["tipo"], "especial", 
                          "Debe manejar caracteres especiales en claves")
        valor_complejo = {
            "lista": [1, 2, 3],
            "anidado": {"nivel2": "valor"},
            "numeros": [1.5, 2.5, 3.5]
        }
        hash_table.insert("valor_complejo", valor_complejo)
        self.assert_igual(hash_table.search("valor_complejo"), valor_complejo, 
                          "Debe manejar estructuras complejas")
    
    def test_factor_carga(self):
        #prueba cálculo del factor de carga
        print("\n[TEST 10] Factor de Carga")
        
        hash_table = HashTable(tamaño_inicial=10)
        
        self.assert_igual(hash_table._calcular_factor_carga(), 0.0, "Factor inicial debe ser 0")
        
        for i in range(5):
            hash_table.insert(f"elemento_{i}", i)
        
        factor = hash_table._calcular_factor_carga()
        self.assert_igual(factor, 0.5, "Factor debe ser 0.5 con 5 elementos en tabla de 10")
        
        print(f"  Factor de carga calculado: {factor:.2f}")
    
    def ejecutar_todas_las_pruebas(self):
        #ejecuta todas las pruebas
        print("\n" + "="*60)
        print("  SUITE DE PRUEBAS - TABLA HASH Y VIDEOJUEGO")
        print("="*60)
        
        self.test_insercion_basica()
        self.test_busqueda_fallida()
        self.test_actualizacion_valor()
        self.test_eliminacion()
        self.test_colisiones()
        self.test_rehash()
        self.test_persistencia()
        self.test_game_data_manager()
        self.test_casos_borde()
        self.test_factor_carga()
        
        print("\n" + "="*60)
        print(f"  RESUMEN: {self.pruebas_pasadas}/{self.pruebas_ejecutadas} pruebas pasadas")
        print("="*60 + "\n")
        
        if self.pruebas_pasadas == self.pruebas_ejecutadas:
            print("✓ ¡TODAS LAS PRUEBAS PASARON! 🎉\n")
            return True
        else:
            fallos = self.pruebas_ejecutadas - self.pruebas_pasadas
            print(f"✗ {fallos} prueba(s) fallaron.\n")
            return False


if __name__ == "__main__":
    suite = TestSuite()
    exito = suite.ejecutar_todas_las_pruebas()
    exit(0 if exito else 1)
