from typing import List, Dict, Tuple, Optional, Callable

class Vertex:
    """
    Represents a vertex in a graph.

    Attributes:
        name (str): The label or identifier of the vertex.
        children (Dict[str, Tuple[str, str, float]]): 
            A mapping between child vertex names and edges.
            Each edge is represented as a tuple:
                (source vertex name, child vertex name, edge weight).
    """

    def __init__(self, name: str, children: Optional[Dict[str, Tuple[str, str, float]]] = None):
        """
        Initializes a Vertex.

        Args:
            name (str): The label or identifier of the vertex.
            children (Optional[Dict[str, Tuple[str, str, float]]]): 
                A mapping between child vertex names and edges.
        """
        self.name = name
        self.children: Dict[str, Tuple[str, str, float]] = children if children is not None else {}

    def get_children(self) -> List[Tuple[str, str, float]]:
        """
        Returns all edges from this vertex.

        Returns:
            List[Tuple[str, str, float]]: The list of edges from this vertex.
        """
        # note-to-self: the dictionary method values() returns a iterable of the type dict_values
        return list(self.children.values())

class Graph:
    """
    Represents a graph consisting of multiple vertices.

    Attributes:
        vertices (List[Vertex]): The list of vertices in the graph.
    """

    def __init__(self, vertices: List[Vertex]):
        """
        Initializes a Graph.
    
        Args:
            vertices (List[Vertex]): The list of vertices that make up the graph.
        """
        self.vertices = vertices

    def get_vertices(self) -> List[Vertex]:
        """
        Returns all vertices in the graph.

        Returns:
            List[Vertex]: The list of vertices in the graph.
        """
        return self.vertices

    def is_child(self, u_name: str, v_name: str) -> bool:
        """
        Checks if vertex v_name is a child of vertex u_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the potential child vertex.

        Returns:
            bool: True if the vertex v_name is a child of the vertex u_name, False otherwise.
        """
        u = None
        vertices = self.get_vertices()

        # traverse through the vertices to find the vertex object u
        for vertex in vertices:
            if vertex.name == u_name:
                u = vertex
                break
        if u is None:
            return False

        # check each of the edges in u to look for vertex v
        return v_name in u.children

    def get_edge(self, u_name: str, v_name: str) -> Optional[Tuple[str, str, float]]:
        """
        Retrieves the edge between u_name and v_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the child vertex.

        Returns:
            Optional[Tuple[str, str, float]]: The edge if it exists, 
            or None if no such edge is found.
        """
        u = None
        vertices = self.get_vertices()

        # traverse through the vertices to find the vertex object u
        for vertex in vertices:
            if vertex.name == u_name:
                u = vertex
                break
        
        if u is None:
            return None
        
        return u.children.get(v_name)
        

class Device(Vertex):
    """
    Represents a network device, extending the Vertex class with
    device-specific functionality.

    Attributes:
        name (str): The label or identifier of the device.
        children (Dict[str, Tuple[str, str, float]]): 
            A mapping between child device names and nearby devices.
        network (Graph): A graph representing this device's discovered network.
    """

    def __init__(self, name: str):
        """
        Initializes a Device.

        Args:
            name (str): The label or identifier of the device.
        """
        super().__init__(name)
        self.network = Graph([self])
    
    def find_vertex_helper(self, name: str, vertices: List[Vertex]) -> Optional[Vertex]:
            """Given a list of vertices, return the Vertex with name, or None if it doesn't exist"""
            for vertex in vertices:
                if vertex.name == name:
                    return vertex
            return None

    def discover_network(self, find_devices_fn: Callable[[List[str]], List[Tuple[str, str, float]]]) -> None:
        """
        Discovers the surrounding network starting from this device. Once this 
        function is called, self.network should contain a representation of the 
        device's discovered network.

        Args:
            find_devices_fn (Callable[[List[str]], List[Tuple[str, str, float]]]): 
                A function that takes an ordered list of device names (i.e., a path) 
                and returns the edges from the last device in the path to its immediate children.
        """

        # Build the graph using BFS
        
        queue = [self.name]
        visited = {self.name}
        vertices_dict = {self.name: Vertex(self.name)}  # Map name -> Vertex object
        
        while queue:
            device_name = queue.pop(0)
            device_edges = find_devices_fn([device_name])
            
            # Create or get the parent vertex
            parent_vertex = vertices_dict[device_name]
            
            for edge in device_edges:
                child_name = edge[1]
                
                parent_vertex.children[child_name] = edge
                
                # create a child vertex if not seen before
                if child_name not in visited:
                    vertices_dict[child_name] = Vertex(child_name)
                    queue.append(child_name)
                    visited.add(child_name)
        
        self.network = Graph(list(vertices_dict.values()))

    def find_path(self, d_name: str) -> Optional[List[str]]:
        """
        Finds the cheapest path from this device to the specified target device 
        using the Cheapest-First Search (CFS) algorithm.

        Args:
            d_name (str): The name of the destination device.

        Returns:
            Optional[List[str]]: An ordered list of device names representing the path 
            from this device to the target. If no path exists, returns None.
        """
        pq = [(0, self.name)]
        cheapest_parents = {self.name: (0, None)}

        # pq stores all the next nodes we could check (and the next one to check)
        # if pq is not empty, that means there are still more nodes to check
        # if pq becomes empty before find_path returns, we did not find d_name
        while pq:
            pq.sort(key=lambda x: x[0])  # Sort by cost
            next = pq.pop(0)
            current_vertex_name = next[1]
            if current_vertex_name == d_name:
                path = []
                last_node = d_name
                while last_node is not None:
                    path.append(last_node)
                    last_node = cheapest_parents[last_node][1]
                return path[::-1]
            else:
                current_vertex = self.find_vertex_helper(current_vertex_name, self.network.get_vertices())
                edges = current_vertex.children.values()
                for edge in edges:
                    # edge[2] would be the weight, edge[1] would be the neighbouring vertex name
                    cost_thus_far = edge[2] + cheapest_parents[current_vertex_name][0]
                    neighbour = edge[1]
                    if neighbour in cheapest_parents:
                        if cost_thus_far < cheapest_parents[neighbour][0]:
                            pq.append((cost_thus_far, neighbour))
                            cheapest_parents[neighbour] = (cost_thus_far, current_vertex_name)
                    else:
                        cheapest_parents[neighbour] = (cost_thus_far, current_vertex_name)
                        pq.append((cost_thus_far, neighbour))
        return None


# ----------------------------------------------------------------------
# Mock function for testing
# ----------------------------------------------------------------------
def find_devices_fn(path: List[str]) -> List[Tuple[str, str, float]]:
    """
    A mock function that simulates network discovery.

    Args:
        path (List[str]): The sequence of device names representing the discovery path.

    Returns:
        List[Tuple[str, str, float]]: A list of edges, where each tuple contains:
            - source device name (str),
            - child device name (str),
            - edge weight (float).
    """
    if not path:
        return []

    last_device = path[-1]

    mock_network = {
        "chandra-s25": [
            ("chandra-s25", "router-051797", 1.0),
            ("chandra-s25", "helen-pc", 1.0),
        ],
        "router-051797": [
            ("router-051797", "ws-102", 1.2),
            ("router-051797", "switch-12", 0.8),
            ("router-051797", "srv-07", 1.0),
        ],
        "helen-pc": [
            ("helen-pc", "ws-102", 1.1),
        ],
        "test-pc": [

        ]
    }

    return mock_network.get(last_device, [])