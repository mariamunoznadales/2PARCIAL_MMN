import heapq
import json
from datetime import datetime

class GestorTareas:
    def __init__(self, archivo_persistencia="tareas.json"):
        """
        Inicializa el gestor de tareas.
        Carga las tareas desde un archivo de persistencia si existe.
        """
        self.heap = []  # Lista que actuará como un heap para gestionar tareas
        self.tareas_completadas = set()  # Conjunto para almacenar tareas completadas
        self.archivo_persistencia = archivo_persistencia  # Archivo para persistencia
        self.cargar_tareas()  # Carga las tareas desde el archivo

    def guardar_tareas(self):
        """
        Guarda las tareas actuales en un archivo JSON.
        """
        with open(self.archivo_persistencia, "w") as archivo:
            json.dump(self.heap, archivo)

    def cargar_tareas(self):
        """
        Carga las tareas desde un archivo JSON si existe.
        """
        try:
            with open(self.archivo_persistencia, "r") as archivo:
                self.heap = json.load(archivo)
            heapq.heapify(self.heap)  # Convierte la lista cargada en un heap válido
        except FileNotFoundError:
            self.heap = []  # Si el archivo no existe, inicializamos una lista vacía

    def añadir_tarea(self, nombre, prioridad, fecha_vencimiento, dependencias=[]):
        """
        Añade una nueva tarea al sistema.
        - nombre: Nombre de la tarea (cadena no vacía).
        - prioridad: Número entero (menor significa mayor prioridad).
        - fecha_vencimiento: Fecha en formato 'YYYY-MM-DD'.
        - dependencias: Lista de nombres de tareas de las que depende.
        """
        if not nombre.strip():
            raise ValueError("El nombre de la tarea no puede estar vacío.")
        if not isinstance(prioridad, int):
            raise ValueError("La prioridad debe ser un número entero.")
        
        # Convertimos la fecha a un formato estándar ISO 8601
        fecha = datetime.strptime(fecha_vencimiento, "%Y-%m-%d").isoformat()
        tarea = (prioridad, fecha, nombre, dependencias)  # Creamos una tupla para la tarea
        heapq.heappush(self.heap, tarea)  # Añadimos la tarea al heap
        self.guardar_tareas()  # Guardamos los cambios en el archivo

    def mostrar_tareas_pendientes(self):
        """
        Muestra todas las tareas pendientes ordenadas por prioridad y fecha de vencimiento.
        Utiliza Merge Sort para realizar la ordenación.
        """
        # Ordenamos la lista usando Merge Sort
        tareas_ordenadas = self.merge_sort(self.heap)
        print("Tareas pendientes (ordenadas por prioridad y fecha):")
        for tarea in tareas_ordenadas:
            prioridad, fecha, nombre, dependencias = tarea
            print(f"Nombre: {nombre}, Prioridad: {prioridad}, Fecha: {fecha}, Dependencias: {dependencias}")

    def merge_sort(self, lista):
        """
        Implementa el algoritmo Merge Sort para ordenar tareas.
        - Divide la lista en mitades, las ordena recursivamente y luego las combina.
        - Ordena por prioridad (primero) y fecha de vencimiento (segundo).
        """
        if len(lista) <= 1:
            return lista  # Una lista de tamaño 1 ya está ordenada
        
        # Dividimos la lista en dos mitades
        mitad = len(lista) // 2
        izquierda = self.merge_sort(lista[:mitad])  # Ordenamos recursivamente la mitad izquierda
        derecha = self.merge_sort(lista[mitad:])  # Ordenamos recursivamente la mitad derecha
        
        # Mezclamos ambas mitades ordenadas
        return self.mezclar(izquierda, derecha)

    def mezclar(self, izquierda, derecha):
        """
        Mezcla dos listas ordenadas en una sola lista ordenada.
        - Compara elementos de ambas listas para mantener el orden.
        """
        resultado = []  # Lista para almacenar el resultado de la mezcla
        while izquierda and derecha:
            # Comparamos las tareas por prioridad y luego por fecha
            if (izquierda[0][0], izquierda[0][1]) <= (derecha[0][0], derecha[0][1]):
                resultado.append(izquierda.pop(0))  # Añadimos el menor de la izquierda
            else:
                resultado.append(derecha.pop(0))  # Añadimos el menor de la derecha
        
        # Añadimos los elementos restantes de ambas listas
        resultado.extend(izquierda or derecha)
        return resultado

    def completar_tarea(self, nombre):
        """
        Marca una tarea como completada y la elimina del sistema.
        - nombre: Nombre de la tarea a completar.
        """
        tarea_encontrada = False
        nuevas_tareas = []
        
        # Procesamos todas las tareas del heap
        while self.heap:
            prioridad, fecha, nombre_tarea, dependencias = heapq.heappop(self.heap)
            if nombre_tarea == nombre:
                tarea_encontrada = True
                self.tareas_completadas.add(nombre)  # Añadimos la tarea al conjunto de completadas
            else:
                nuevas_tareas.append((prioridad, fecha, nombre_tarea, dependencias))
        
        # Reconstruimos el heap con las tareas restantes
        self.heap = nuevas_tareas
        heapq.heapify(self.heap)
        self.guardar_tareas()  # Guardamos los cambios en el archivo

        if not tarea_encontrada:
            print(f"No se encontró ninguna tarea con el nombre: {nombre}.")
        else:
            print(f"Tarea '{nombre}' completada y eliminada del sistema.")

    def obtener_tarea_mayor_prioridad(self):
        """
        Obtiene la siguiente tarea de mayor prioridad sin eliminarla.
        - Verifica que todas las dependencias estén completadas.
        """
        while self.heap:
            prioridad, fecha, nombre, dependencias = self.heap[0]
            # Verificamos si todas las dependencias están completadas
            if all(dep in self.tareas_completadas for dep in dependencias):
                print(f"Siguiente tarea de mayor prioridad: {nombre}, Prioridad: {prioridad}, Fecha: {fecha}")
                return
            else:
                # Si no se puede ejecutar debido a dependencias, la retiramos temporalmente
                heapq.heappop(self.heap)
        
        print("No hay tareas disponibles o ejecutables en este momento.")

# SISTEMA DE GESTIÓN DE TAREAS 
if __name__ == "__main__":
    gestor = GestorTareas()

    while True:
        print("")
        print("GESTOR DE TAREAS CON PRIORIDADES")
        print("")
        print("\nOPCIONES:")
        print("1. Añadir tarea")
        print("2. Mostrar tareas pendientes")
        print("3. Completar tarea")
        print("4. Obtener tarea de mayor prioridad")
        print("5. Salir")
        print("")

        opcion = input("Elige una opción: ")
        try:
            if opcion == "1":
                nombre = input("Ingrese el nombre de la tarea: ")
                prioridad = int(input("Ingrese la prioridad de la tarea (número entero, menor = mayor prioridad): "))
                fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY-MM-DD): ")
                dependencias = input("Ingrese las dependencias (separadas por coma, o deje vacío): ").split(",")
                dependencias = [dep.strip() for dep in dependencias if dep.strip()]
                gestor.añadir_tarea(nombre, prioridad, fecha_vencimiento, dependencias)
            elif opcion == "2":
                gestor.mostrar_tareas_pendientes()
            elif opcion == "3":
                nombre = input("Ingrese el nombre de la tarea a completar: ")
                gestor.completar_tarea(nombre)
            elif opcion == "4":
                gestor.obtener_tarea_mayor_prioridad()
            elif opcion == "5":
                print("Saliendo del gestor de tareas. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
