import json

class Node:
    def __init__(self, cancion_data: dict):
        self.cancion = {
            'nombre': cancion_data.get('nombre', ''),
            'artista': cancion_data.get('artista', ''),
            'album': cancion_data.get('album', '')
        }
        self.next = None
        self.prev = None  # Nuevo: referencia al nodo anterior

    def __repr__(self):
        return f"{self.cancion['nombre']} - {self.cancion['artista']} ({self.cancion['album']})"


class LinkedList:
    def __init__(self):
        self.start = None
        self.end = None  # Nuevo: referencia al último nodo

    def __repr__(self):
        nodes = ['INICIO']
        for node in self:
            nodes.append(str(node))
        nodes.append('FIN')
        return '\n' + ' --> '.join(nodes)

    def __iter__(self):
        node = self.start
        while node is not None:
            yield node
            node = node.next

    def __len__(self):
        length = 0
        for _ in self:
            length += 1
        return length

    def traverse_forward(self):
        print("\nLista de Canciones")
        for node in self:
            print(node)

    def traverse_backward(self):
        print("\nLista de Canciones")
        node = self.end
        while node is not None:
            print(node)
            node = node.prev

    def insert_at_beginning(self, element: Node):
        if self.start is None:
            # Lista vacía
            self.start = element
            self.end = element
        else:
            element.next = self.start
            self.start.prev = element
            self.start = element

    def insert_at_end(self, element: Node):
        if self.start is None:
            # Lista vacía
            self.start = element
            self.end = element
        else:
            element.prev = self.end
            self.end.next = element
            self.end = element

    def insert_after_node(self, element: Node, node_reference: any):
        current = self.start
        while current is not None:
            if current.cancion['nombre'] == node_reference:
                # Encontramos el nodo de referencia
                element.next = current.next
                element.prev = current
                
                if current.next is not None:
                    current.next.prev = element
                else:
                    # Si es el último nodo, actualizamos end
                    self.end = element
                
                current.next = element
                return True
            current = current.next
        return False  # No se encontró el nodo de referencia

    def delete_node(self, element_data: any):
        current = self.start
        
        while current is not None:
            if current.cancion['nombre'] == element_data:
                # Ajustar referencias del nodo anterior
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    # Es el primer nodo
                    self.start = current.next
                
                # Ajustar referencias del nodo siguiente
                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    # Es el último nodo
                    self.end = current.prev
                
                return True  # Nodo eliminado
            current = current.next
        
        return False  # No se encontró el nodo

    def search(self, element_data: any):
        current = self.start
        while current is not None:
            if current.cancion['nombre'] == element_data:
                return current
            current = current.next
        return None  # No se encontró

    def search_by_artist(self, artista: str):
        canciones = []
        current = self.start
        while current is not None:
            if current.cancion['artista'].lower() == artista.lower():
                canciones.append(current)
            current = current.next
        return canciones

    def get_playlist_info(self):
        info = {
            'total_canciones': len(self),
            'artistas': set(),
            'albumes': set(),
            'canciones': []
        }
        
        for node in self:
            info['artistas'].add(node.cancion['artista'])
            info['albumes'].add(node.cancion['album'])
            info['canciones'].append(node.cancion['nombre'])
        
        info['artistas'] = list(info['artistas'])
        info['albumes'] = list(info['albumes'])
        
        return info
    
def cargar_canciones_desde_json(ruta, playlist):
    with open(ruta, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        for cancion_data in data:
            nodo = Node(cancion_data)
            playlist.insert_at_end(nodo)

playlist = LinkedList()
cargar_canciones_desde_json('canciones.json', playlist)