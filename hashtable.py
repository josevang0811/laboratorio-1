import json

class Node:
    
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None
    
    def __repr__(self):
        return f"Node({self.clave}: {self.valor})"


class HashTable:
    def __init__(self, tamaño_inicial=16):
        self.tamaño = tamaño_inicial
        self.tabla = [None] * self.tamaño
        self.elementos = 0
        self.factor_carga_limite = 0.75
    
    def _hash(self, clave):
        return hash(clave) % self.tamaño
    
    def _calcular_factor_carga(self):
        return self.elementos / self.tamaño
    
    def _rehash(self):
        print(f"  [REHASH] Factor de carga {self._calcular_factor_carga():.2f} > {self.factor_carga_limite}")
        print(f"  [REHASH] Duplicando tabla: {self.tamaño} -> {self.tamaño * 2}")

        tabla_antigua = self.tabla
        tamaño_antiguo = self.tamaño

        self.tamaño = self.tamaño * 2
        self.tabla = [None] * self.tamaño
        self.elementos = 0

        for indice in range(tamaño_antiguo):
            nodo_actual = tabla_antigua[indice]
            while nodo_actual is not None:
                self._insertar_sin_rehash(nodo_actual.clave, nodo_actual.valor)
                nodo_actual = nodo_actual.siguiente
        
        print(f"  [REHASH] Rehash completado. Nuevo tamaño: {self.tamaño}")
    
    def _insertar_sin_rehash(self, clave, valor):
        indice = self._hash(clave)

        if self.tabla[indice] is None:
            self.tabla[indice] = Node(clave, valor)
            self.elementos += 1
        else:
            nodo_actual = self.tabla[indice]
            while nodo_actual is not None:
                if nodo_actual.clave == clave:
                    nodo_actual.valor = valor
                    return
                nodo_actual = nodo_actual.siguiente
            nuevo_nodo = Node(clave, valor)
            nuevo_nodo.siguiente = self.tabla[indice]
            self.tabla[indice] = nuevo_nodo
            self.elementos += 1
    
    def insert(self, clave, valor):
        self._insertar_sin_rehash(clave, valor)
        if self._calcular_factor_carga() > self.factor_carga_limite:
            self._rehash()
    
    def search(self, clave):
        indice = self._hash(clave)
        
        nodo_actual = self.tabla[indice]
        while nodo_actual is not None:
            if nodo_actual.clave == clave:
                return nodo_actual.valor
            nodo_actual = nodo_actual.siguiente
        
        return None
    
    def delete(self, clave):
        indice = self._hash(clave)
        
        if self.tabla[indice] is None:
            return False
        if self.tabla[indice].clave == clave:
            self.tabla[indice] = self.tabla[indice].siguiente
            self.elementos -= 1
            return True
        nodo_anterior = self.tabla[indice]
        nodo_actual = nodo_anterior.siguiente
        
        while nodo_actual is not None:
            if nodo_actual.clave == clave:
                nodo_anterior.siguiente = nodo_actual.siguiente
                self.elementos -= 1
                return True
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente
        
        return False
    
    def get_all(self):
        resultado = []
        for indice in range(self.tamaño):
            nodo_actual = self.tabla[indice]
            while nodo_actual is not None:
                resultado.append((nodo_actual.clave, nodo_actual.valor))
                nodo_actual = nodo_actual.siguiente
        return resultado
    
    def save_to_file(self, ruta_archivo):
        datos = {
            "tamaño": self.tamaño,
            "elementos": self.elementos,
            "factor_carga": self._calcular_factor_carga(),
            "pares": self.get_all()
        }
        
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Tabla hash guardada en: {ruta_archivo}")
    
    def load_from_file(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            self.tamaño = datos["tamaño"]
            self.tabla = [None] * self.tamaño
            self.elementos = 0
            for clave, valor in datos["pares"]:
                self._insertar_sin_rehash(clave, valor)
            
            print(f"✓ Tabla hash cargada desde: {ruta_archivo}")
            print(f"  - Tamaño: {self.tamaño}")
            print(f"  - Elementos: {self.elementos}")
            print(f"  - Factor de carga: {self._calcular_factor_carga():.2f}")
        
        except FileNotFoundError:
            print(f"⚠ Archivo no encontrado: {ruta_archivo}. Iniciando tabla vacía.")
    
    def __repr__(self):
        return (f"HashTable(tamaño={self.tamaño}, elementos={self.elementos}, "
                f"factor_carga={self._calcular_factor_carga():.2f})")
