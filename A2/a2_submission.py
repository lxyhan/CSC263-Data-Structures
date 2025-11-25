from typing import List, Dict, Tuple, Optional, Callable

################ CODE FROM A1 ################
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

################ CODE FROM A1 ################

# Union-Find (Disjoint Set) data structure
class UnionFind:
    def __init__(self, elements: List[str]):
        """
        Initializes the Union-Find data structure for n elements.
        Initially, each element is in its own set (its parent is itself).
        The rank (or size) of each set is initialized to 0.

        Parameters:
        elements (List[str]): The list of elements in the Union-Find data structure.
        """
        self.parent = {elem: elem for elem in elements}  
        self.rank = {elem: 0 for elem in elements}       
    
    def find(self, x: str) -> str:
        """
        Find the root (or representative) of the set containing the element x.
        
        Args:
        x (str): The element whose root we want to find.

        Returns:
        str: The root of the set that contains x.
        """
        if self.parent[x] == x:
            return x
        else:
            # recurses up the parent tree until we locate the elem whose parent is itself
            self.parent[x] = self.find(self.parent[x])
            return self.parent[x]        
    
    def union(self, x: int, y: int) -> bool:
        """Union (or merge) the sets containing elements x and y. 
        Return True if union was successful.
        If x and y are already in the same set, do nothing (return False).

        Args:
            x (str): The first element (set to be united).
            y (str): The second element (set to be united).
        
        Returns:
        bool: True if x and y are successfully unioned.
              False if x and y are already in the same set (no union nedded).
        """
        root_x = self.find(x)
        root_y = self.find(y)

        # case 1: x and y are already int he same set
        if root_x == root_y:
            return False
        # case 2: x and y are in different sets, merge them
        if self.rank[root_x] > self.rank[root_y]:
            # attach y to x
            self.parent[root_y] = root_x
        elif self.rank[root_x] < self.rank[root_y]:
            # attach x to y
            self.parent[root_x] = root_y
        else:
            # attach y to x but increase rank
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True

        
# Function to implement Kruskal's algorithm
def kruskal_mst(graph: Graph) -> List[Tuple[str, str, float]]:
    """
    Kruskal's Algorithm for Minimum Spanning Tree (MST).

    Args:
        graph (Graph): The graph for which we compute the MST.

    Returns:
        List[Tuple[str, str, float]]: A list of edges in the MST. 
        Each edge is represented as a tuple (source vertex, destination vertex, weight).
    """
    
    result = []  # The final MST

    # Suggested steps 
    # Step 1: Get edge list
    edges = set()
    vertices = graph.get_vertices()
    for vertex in vertices:
        for u, v, weight in vertex.get_children():
            edge = (min(u, v), max(u, v), weight)
            edges.add(edge)
    edges = list(edges)
    # Step 2: Sort edges by weight
    edges.sort(key=lambda edge: edge[2])
    # Step 3: Initialize Union-Find data structures
    vertex_names = [v.name if hasattr(v, 'name') else v for v in vertices]
    uf = UnionFind(vertex_names)
    # (to track the connected sets of vertices as we add edges to the MST)
    # Step 4: Iterate over the sorted edges to build MST 
    for u, v, weight in edges:
        if uf.find(u) != uf.find(v):
            result.append((u, v, weight))
            uf.union(u, v)
    return result  


# Function to implement Prim's algorithm
def prim_mst(graph: Graph) -> List[Tuple[str, str, float]]:
    """
    Prim's Algorithm for Minimum Spanning Tree (MST).

    Args:
        graph (Graph): The graph for which we compute the MST.

    Returns:
        List[Tuple[str, str, float]]: A list of edges in the MST. 
            Each edge is represented as a tuple (source vertex, destination vertex, weight).
    """
    
    result = []  # The final MST

    # Handle empty graph
    vertices = graph.get_vertices()
    if len(vertices) == 0:
        return result

    # Pick starting vertex (chosen to match the test cases)
    start_vertex = vertices[0]

    # Get starting node edges 
    visited = {start_vertex.name}

    while len(visited) < len(graph.get_vertices()):
        outer_edges = []

        # Loop over edges in the graph 
        for vertex in graph.get_vertices():
            if vertex.name in visited:
                for edge in vertex.get_children():
                    if edge[1] not in visited:
                        outer_edges.append(edge)

        # Pick the vertex with the minimum weight edge (and add it to MST)
        min_edge = min(outer_edges, key=lambda edge: edge[2])
        result.append(min_edge)
        visited.add(min_edge[1])
    
    return result  