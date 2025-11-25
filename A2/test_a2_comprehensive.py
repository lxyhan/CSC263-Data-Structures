"""
COMPREHENSIVE TEST SUITE for A2: Union-Find, Kruskal's, and Prim's algorithms
Tests edge cases, stress tests, and advanced scenarios
"""

from a2_submission import Vertex, Graph, UnionFind, kruskal_mst, prim_mst
from typing import List, Tuple
import random


# ============================================================================
# GRAPH CREATION HELPERS
# ============================================================================

def create_linear_chain(n: int) -> Graph:
    """Creates a linear chain: A -- B -- C -- D ..."""
    vertices = []
    names = [chr(65 + i) for i in range(n)]  # A, B, C, ...
    
    for i in range(n):
        children = {}
        if i > 0:
            children[names[i-1]] = (names[i], names[i-1], 1.0)
        if i < n - 1:
            children[names[i+1]] = (names[i], names[i+1], 1.0)
        vertices.append(Vertex(names[i], children))
    
    return Graph(vertices)


def create_complete_graph(n: int) -> Graph:
    """Creates a complete graph where every vertex connects to every other"""
    vertices = []
    names = [chr(65 + i) for i in range(n)]
    
    for i in range(n):
        children = {}
        for j in range(n):
            if i != j:
                weight = abs(i - j)  # Weight based on distance
                children[names[j]] = (names[i], names[j], float(weight))
        vertices.append(Vertex(names[i], children))
    
    return Graph(vertices)


def create_star_graph(n: int) -> Graph:
    """Creates a star graph: center connected to all others"""
    vertices = []
    names = ['Center'] + [f'Node{i}' for i in range(n-1)]
    
    # Center vertex
    center_children = {}
    for i in range(1, n):
        center_children[names[i]] = ('Center', names[i], float(i))
    vertices.append(Vertex('Center', center_children))
    
    # Outer vertices
    for i in range(1, n):
        children = {'Center': (names[i], 'Center', float(i))}
        vertices.append(Vertex(names[i], children))
    
    return Graph(vertices)


def create_disconnected_graph() -> Graph:
    """Creates a graph with two disconnected components"""
    # Component 1: A-B
    v_a = Vertex('A', {'B': ('A', 'B', 1.0)})
    v_b = Vertex('B', {'A': ('B', 'A', 1.0)})
    
    # Component 2: C-D
    v_c = Vertex('C', {'D': ('C', 'D', 2.0)})
    v_d = Vertex('D', {'C': ('D', 'C', 2.0)})
    
    return Graph([v_a, v_b, v_c, v_d])


def create_equal_weight_graph() -> Graph:
    """Creates a graph where all edges have equal weight"""
    v_a = Vertex('A', {
        'B': ('A', 'B', 1.0),
        'C': ('A', 'C', 1.0)
    })
    v_b = Vertex('B', {
        'A': ('B', 'A', 1.0),
        'C': ('B', 'C', 1.0),
        'D': ('B', 'D', 1.0)
    })
    v_c = Vertex('C', {
        'A': ('C', 'A', 1.0),
        'B': ('C', 'B', 1.0),
        'D': ('C', 'D', 1.0)
    })
    v_d = Vertex('D', {
        'B': ('D', 'B', 1.0),
        'C': ('D', 'C', 1.0)
    })
    
    return Graph([v_a, v_b, v_c, v_d])


# ============================================================================
# UNION-FIND ADVANCED TESTS
# ============================================================================

def test_unionfind_large_set():
    """Test Union-Find with large number of elements"""
    print("Testing Union-Find with large set (100 elements)...")
    elements = [f"Node{i}" for i in range(100)]
    uf = UnionFind(elements)
    
    # Union in a chain
    for i in range(99):
        result = uf.union(f"Node{i}", f"Node{i+1}")
        assert result == True, f"Union {i} should succeed"
    
    # All should be in same set
    root = uf.find("Node0")
    for i in range(100):
        assert uf.find(f"Node{i}") == root, f"Node{i} should have same root"
    
    print("✓ Large set test passed")


def test_unionfind_alternating_unions():
    """Test Union-Find with alternating union pattern"""
    print("Testing Union-Find with alternating unions...")
    uf = UnionFind(['A', 'B', 'C', 'D', 'E', 'F'])
    
    # Union pairs: (A,B), (C,D), (E,F)
    uf.union('A', 'B')
    uf.union('C', 'D')
    uf.union('E', 'F')
    
    # Verify three separate sets
    assert uf.find('A') == uf.find('B')
    assert uf.find('C') == uf.find('D')
    assert uf.find('E') == uf.find('F')
    assert uf.find('A') != uf.find('C')
    assert uf.find('A') != uf.find('E')
    assert uf.find('C') != uf.find('E')
    
    # Merge all
    uf.union('A', 'C')
    uf.union('C', 'E')
    
    # All should be in same set now
    root = uf.find('A')
    for elem in ['B', 'C', 'D', 'E', 'F']:
        assert uf.find(elem) == root
    
    print("✓ Alternating unions test passed")


def test_unionfind_reverse_order():
    """Test Union-Find with reverse order unions"""
    print("Testing Union-Find with reverse order...")
    uf = UnionFind(['A', 'B', 'C', 'D', 'E'])
    
    # Union from end to start
    uf.union('E', 'D')
    uf.union('D', 'C')
    uf.union('C', 'B')
    uf.union('B', 'A')
    
    # All should be connected
    root = uf.find('A')
    for elem in ['B', 'C', 'D', 'E']:
        assert uf.find(elem) == root
    
    print("✓ Reverse order test passed")


def test_unionfind_single_element():
    """Test Union-Find with single element"""
    print("Testing Union-Find with single element...")
    uf = UnionFind(['A'])
    
    assert uf.find('A') == 'A'
    assert uf.rank['A'] == 0
    
    # Can't union with itself (should return False)
    result = uf.union('A', 'A')
    assert result == False, "Unioning element with itself should return False"
    
    print("✓ Single element test passed")


def test_unionfind_star_pattern():
    """Test Union-Find with star pattern (all connect to center)"""
    print("Testing Union-Find with star pattern...")
    elements = ['Center'] + [f'Node{i}' for i in range(10)]
    uf = UnionFind(elements)
    
    # Connect all to center
    for i in range(10):
        uf.union('Center', f'Node{i}')
    
    # All should have same root
    root = uf.find('Center')
    for i in range(10):
        assert uf.find(f'Node{i}') == root
    
    # Center should have high rank
    assert uf.rank[root] >= 1
    
    print("✓ Star pattern test passed")


# ============================================================================
# KRUSKAL'S ADVANCED TESTS
# ============================================================================

def test_kruskal_linear_chain():
    """Test Kruskal's on linear chain graph"""
    print("Testing Kruskal's on linear chain...")
    graph = create_linear_chain(5)
    mst = kruskal_mst(graph)
    
    # Linear chain MST should have n-1 edges
    assert len(mst) == 4, f"Expected 4 edges, got {len(mst)}"
    
    # All edges should have weight 1.0
    for edge in mst:
        assert edge[2] == 1.0, f"Expected weight 1.0, got {edge[2]}"
    
    print("✓ Linear chain test passed")


def test_kruskal_complete_graph():
    """Test Kruskal's on complete graph"""
    print("Testing Kruskal's on complete graph...")
    graph = create_complete_graph(5)
    mst = kruskal_mst(graph)
    
    # MST should have n-1 edges
    assert len(mst) == 4, f"Expected 4 edges, got {len(mst)}"
    
    # Verify all vertices are included
    vertices_in_mst = set()
    for u, v, _ in mst:
        vertices_in_mst.add(u)
        vertices_in_mst.add(v)
    assert len(vertices_in_mst) == 5, "All vertices should be in MST"
    
    print("✓ Complete graph test passed")


def test_kruskal_star_graph():
    """Test Kruskal's on star graph"""
    print("Testing Kruskal's on star graph...")
    graph = create_star_graph(6)
    mst = kruskal_mst(graph)
    
    # MST should have 5 edges
    assert len(mst) == 5, f"Expected 5 edges, got {len(mst)}"
    
    # All edges should connect to center
    center_count = sum(1 for u, v, _ in mst if u == 'Center' or v == 'Center')
    assert center_count == 5, "All edges should connect to center in star graph MST"
    
    print("✓ Star graph test passed")


def test_kruskal_equal_weights():
    """Test Kruskal's with all equal edge weights"""
    print("Testing Kruskal's with equal weights...")
    graph = create_equal_weight_graph()
    mst = kruskal_mst(graph)
    
    # MST should have 3 edges (4 vertices)
    assert len(mst) == 3, f"Expected 3 edges, got {len(mst)}"
    
    # Total weight should be 3.0
    total_weight = sum(edge[2] for edge in mst)
    assert total_weight == 3.0, f"Expected weight 3.0, got {total_weight}"
    
    print("✓ Equal weights test passed")


def test_kruskal_disconnected():
    """Test Kruskal's on disconnected graph (produces forest)"""
    print("Testing Kruskal's on disconnected graph...")
    graph = create_disconnected_graph()
    mst = kruskal_mst(graph)
    
    # Should have 2 edges (one per component)
    assert len(mst) == 2, f"Expected 2 edges, got {len(mst)}"
    
    print("✓ Disconnected graph test passed")


def test_kruskal_large_graph():
    """Test Kruskal's on larger graph"""
    print("Testing Kruskal's on large graph (10 vertices)...")
    graph = create_linear_chain(10)
    mst = kruskal_mst(graph)
    
    # Should have 9 edges
    assert len(mst) == 9, f"Expected 9 edges, got {len(mst)}"
    
    print("✓ Large graph test passed")


# ============================================================================
# PRIM'S ADVANCED TESTS
# ============================================================================

def test_prim_linear_chain():
    """Test Prim's on linear chain graph"""
    print("Testing Prim's on linear chain...")
    graph = create_linear_chain(5)
    mst = prim_mst(graph)
    
    assert len(mst) == 4, f"Expected 4 edges, got {len(mst)}"
    
    # All edges should have weight 1.0
    for edge in mst:
        assert edge[2] == 1.0, f"Expected weight 1.0, got {edge[2]}"
    
    print("✓ Linear chain test passed")


def test_prim_complete_graph():
    """Test Prim's on complete graph"""
    print("Testing Prim's on complete graph...")
    graph = create_complete_graph(5)
    mst = prim_mst(graph)
    
    assert len(mst) == 4, f"Expected 4 edges, got {len(mst)}"
    
    # Verify all vertices are included
    vertices_in_mst = set()
    for u, v, _ in mst:
        vertices_in_mst.add(u)
        vertices_in_mst.add(v)
    assert len(vertices_in_mst) == 5, "All vertices should be in MST"
    
    print("✓ Complete graph test passed")


def test_prim_star_graph():
    """Test Prim's on star graph"""
    print("Testing Prim's on star graph...")
    graph = create_star_graph(6)
    mst = prim_mst(graph)
    
    assert len(mst) == 5, f"Expected 5 edges, got {len(mst)}"
    
    print("✓ Star graph test passed")


def test_prim_equal_weights():
    """Test Prim's with all equal edge weights"""
    print("Testing Prim's with equal weights...")
    graph = create_equal_weight_graph()
    mst = prim_mst(graph)
    
    assert len(mst) == 3, f"Expected 3 edges, got {len(mst)}"
    
    total_weight = sum(edge[2] for edge in mst)
    assert total_weight == 3.0, f"Expected weight 3.0, got {total_weight}"
    
    print("✓ Equal weights test passed")


def test_prim_large_graph():
    """Test Prim's on larger graph"""
    print("Testing Prim's on large graph (10 vertices)...")
    graph = create_linear_chain(10)
    mst = prim_mst(graph)
    
    assert len(mst) == 9, f"Expected 9 edges, got {len(mst)}"
    
    print("✓ Large graph test passed")


# ============================================================================
# ALGORITHM COMPARISON TESTS
# ============================================================================

def test_algorithms_produce_same_weight():
    """Test that both algorithms produce MSTs with same total weight"""
    print("Testing algorithm weight equivalence on various graphs...")
    
    test_graphs = [
        ("Linear 5", create_linear_chain(5)),
        ("Complete 4", create_complete_graph(4)),
        ("Star 7", create_star_graph(7)),
        ("Equal weights", create_equal_weight_graph()),
    ]
    
    for name, graph in test_graphs:
        kruskal_mst_edges = kruskal_mst(graph)
        prim_mst_edges = prim_mst(graph)
        
        kruskal_weight = sum(e[2] for e in kruskal_mst_edges)
        prim_weight = sum(e[2] for e in prim_mst_edges)
        
        assert abs(kruskal_weight - prim_weight) < 0.001, \
            f"{name}: Kruskal {kruskal_weight} != Prim {prim_weight}"
        
        assert len(kruskal_mst_edges) == len(prim_mst_edges), \
            f"{name}: Different edge counts"
    
    print("✓ Algorithm weight equivalence test passed")


def test_mst_properties():
    """Test that MSTs satisfy required properties"""
    print("Testing MST properties...")
    
    graph = create_complete_graph(6)
    mst = kruskal_mst(graph)
    
    # Property 1: n-1 edges
    n = len(graph.get_vertices())
    assert len(mst) == n - 1, f"MST should have {n-1} edges"
    
    # Property 2: All vertices included
    vertices_in_mst = set()
    for u, v, _ in mst:
        vertices_in_mst.add(u)
        vertices_in_mst.add(v)
    assert len(vertices_in_mst) == n, "All vertices should be in MST"
    
    # Property 3: Connected (using Union-Find)
    vertex_names = [v.name if hasattr(v, 'name') else v for v in graph.get_vertices()]
    uf = UnionFind(vertex_names)
    for u, v, _ in mst:
        uf.union(u, v)
    
    # All vertices should be in same set
    root = uf.find(vertex_names[0])
    for v_name in vertex_names:
        assert uf.find(v_name) == root, "MST should be connected"
    
    print("✓ MST properties test passed")


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

def test_empty_graph():
    """Test with empty graph"""
    print("Testing empty graph...")
    graph = Graph([])
    
    kruskal_result = kruskal_mst(graph)
    prim_result = prim_mst(graph)
    
    assert len(kruskal_result) == 0, "Empty graph should have no edges"
    assert len(prim_result) == 0, "Empty graph should have no edges"
    
    print("✓ Empty graph test passed")


def test_single_vertex_no_edges():
    """Test single vertex with no edges"""
    print("Testing single vertex with no edges...")
    v = Vertex('Alone', {})
    graph = Graph([v])
    
    kruskal_result = kruskal_mst(graph)
    prim_result = prim_mst(graph)
    
    assert len(kruskal_result) == 0
    assert len(prim_result) == 0
    
    print("✓ Single vertex test passed")


def test_very_large_weights():
    """Test with very large edge weights"""
    print("Testing with very large weights...")
    v_a = Vertex('A', {'B': ('A', 'B', 1000000.0)})
    v_b = Vertex('B', {'A': ('B', 'A', 1000000.0)})
    graph = Graph([v_a, v_b])
    
    mst = kruskal_mst(graph)
    assert len(mst) == 1
    assert mst[0][2] == 1000000.0
    
    print("✓ Large weights test passed")


def test_fractional_weights():
    """Test with fractional edge weights"""
    print("Testing with fractional weights...")
    v_a = Vertex('A', {
        'B': ('A', 'B', 0.1),
        'C': ('A', 'C', 0.2)
    })
    v_b = Vertex('B', {
        'A': ('B', 'A', 0.1),
        'C': ('B', 'C', 0.3)
    })
    v_c = Vertex('C', {
        'A': ('C', 'A', 0.2),
        'B': ('C', 'B', 0.3)
    })
    graph = Graph([v_a, v_b, v_c])
    
    mst = kruskal_mst(graph)
    total_weight = sum(e[2] for e in mst)
    assert abs(total_weight - 0.3) < 0.001, f"Expected 0.3, got {total_weight}"
    
    print("✓ Fractional weights test passed")


# ============================================================================
# STRESS TESTS
# ============================================================================

def test_stress_union_find():
    """Stress test Union-Find with many operations"""
    print("Stress testing Union-Find (1000 elements, 5000 operations)...")
    
    n = 1000
    elements = [f"E{i}" for i in range(n)]
    uf = UnionFind(elements)
    
    # Perform many random unions
    random.seed(42)
    for _ in range(5000):
        i = random.randint(0, n-1)
        j = random.randint(0, n-1)
        uf.union(f"E{i}", f"E{j}")
    
    # Verify find works
    for i in range(100):  # Sample check
        root = uf.find(f"E{i}")
        assert root is not None
    
    print("✓ Stress test passed")


def test_stress_kruskal():
    """Stress test Kruskal's with larger graph"""
    print("Stress testing Kruskal's (20 vertex complete graph)...")
    
    graph = create_complete_graph(20)
    mst = kruskal_mst(graph)
    
    assert len(mst) == 19, f"Expected 19 edges, got {len(mst)}"
    
    print("✓ Kruskal stress test passed")


def test_stress_prim():
    """Stress test Prim's with larger graph"""
    print("Stress testing Prim's (20 vertex complete graph)...")
    
    graph = create_complete_graph(20)
    mst = prim_mst(graph)
    
    assert len(mst) == 19, f"Expected 19 edges, got {len(mst)}"
    
    print("✓ Prim stress test passed")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_comprehensive_tests():
    """Run all comprehensive test cases"""
    print("=" * 80)
    print("RUNNING COMPREHENSIVE TEST SUITE FOR A2")
    print("=" * 80)
    print()
    
    # Union-Find advanced tests
    print("--- UNION-FIND ADVANCED TESTS ---")
    test_unionfind_large_set()
    test_unionfind_alternating_unions()
    test_unionfind_reverse_order()
    test_unionfind_single_element()
    test_unionfind_star_pattern()
    print()
    
    # Kruskal's advanced tests
    print("--- KRUSKAL'S ADVANCED TESTS ---")
    test_kruskal_linear_chain()
    test_kruskal_complete_graph()
    test_kruskal_star_graph()
    test_kruskal_equal_weights()
    test_kruskal_disconnected()
    test_kruskal_large_graph()
    print()
    
    # Prim's advanced tests
    print("--- PRIM'S ADVANCED TESTS ---")
    test_prim_linear_chain()
    test_prim_complete_graph()
    test_prim_star_graph()
    test_prim_equal_weights()
    test_prim_large_graph()
    print()
    
    # Algorithm comparison
    print("--- ALGORITHM COMPARISON TESTS ---")
    test_algorithms_produce_same_weight()
    test_mst_properties()
    print()
    
    # Edge cases
    print("--- EDGE CASE TESTS ---")
    test_empty_graph()
    test_single_vertex_no_edges()
    test_very_large_weights()
    test_fractional_weights()
    print()
    
    # Stress tests
    print("--- STRESS TESTS ---")
    test_stress_union_find()
    test_stress_kruskal()
    test_stress_prim()
    print()
    
    print("=" * 80)
    print("ALL COMPREHENSIVE TESTS PASSED! ✓")
    print("Total: 29 additional tests")
    print("=" * 80)


if __name__ == "__main__":
    run_all_comprehensive_tests()
