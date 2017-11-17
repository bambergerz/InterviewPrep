import unittest
from graph import Node
from graph import Edge
from graph import Graph


class TestGraph(unittest.TestCase):

    def test_nodes(self):
        a = Node(1)
        b = Node(2)
        c = Node(3)
        d = Node(4)
        e = Node(5)
        g = Graph()
        g.add_node(a)
        g.add_node(b)
        g.add_node(c)
        g.add_node(d)
        nodes = g.nodes
        self.assertEqual(True, a in nodes)
        self.assertEqual(True, b in nodes)
        self.assertEqual(True, c in nodes)
        self.assertEqual(True, d in nodes)
        self.assertEqual(False, e in nodes)

    def test_edges(self):
        self.fail()

    def test_get_edges_from_node(self):
        self.fail()

    def test_print_properties(self):
        self.fail()

    def test_add_node(self):
        self.fail()

    def test_add_edge(self):
        self.fail()

    def test_get_node_by_id(self):
        self.fail()

    def test_get_edge_by_id(self):
        self.fail()

    def test_bfs(self):
        self.fail()

    def test_dfs(self):
        self.fail()

    def test_bellmen_ford(self):
        self.fail()

    def test_deijkstra(self):
        self.fail()

if __name__ == "__main__":
    unittest.main()