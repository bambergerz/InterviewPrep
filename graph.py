from Queue import Queue


class Node:
    node_ID = 0

    def __init__(self, value):
        """
        
        :param value: an int. This Node instance will take this value
        """
        assert isinstance(value, int)
        self._id = Node.node_ID
        self._value = value
        self._neighbors = set()
        Node.node_ID += 1

    def __repr__(self):
        return str(self.value)

    @property
    def node_id(self):
        return self._id

    @property
    def value(self):
        return self._value

    @property
    def neighbors(self):
        return self._neighbors

    def add_neighbor(self, neighbor):
        """
        
        :param neighbor: a neighbor node of this Node instance
        :return: True once "neighbor" has been appended to this node's list of neighbors. 
        """
        assert isinstance(neighbor, Node)
        self._neighbors.add(neighbor)


class Edge:
    edge_ID = 0

    def __init__(self, source, target, weight=None):
        assert isinstance(source, Node)
        assert isinstance(target, Node)
        self._id = Edge.edge_ID
        self._source = source
        self._target = target
        self._weight = weight
        Edge.edge_ID += 1

    def __repr__(self):
        return "(" + str(self._source) + ", " + str(self._target) + ")"

    @property
    def edge_id(self):
        return self._id

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def weight(self):
        return self._weight


class Graph:
    def __init__(self):
        self._nodes = []
        self._edges = []

    def __str__(self):
        msg = ""
        msg += "Nodes are: " + str(self._nodes) + "\n"
        msg += "Edges are: " + str(self._edges)
        return msg

    def add_node(self, node):
        assert isinstance(node, Node), "node is not a Node instance"
        self._nodes.append(node)
        return True

    def add_edge(self, edge):
        assert isinstance(edge, Edge), "edge is not an Edge instance"
        self._edges.append(edge)
        source = edge.source
        target = edge.target
        source.add_neighbor(target)
        target.add_neighbor(source)
        return True

    def get_node_by_id(self, node_id):
        """
        
        :param node_id: the id of the node we are trying to return 
        :return: either the node with the ID we are looking for or None if that 
        node does not currently exist in our graph.
        """
        assert isinstance(node_id, int), "node_id must be an int"
        for i in self._nodes:
            if i.node_id == node_id:
                return i
        else:
            print("cannot find node with this ID in the grap")
            return

    def bfs(self, start_node, target_node, to_print=0):
        """
        
        :param start_node: the ID of the node from which we are starting
        :param target_node: the ID of the node we are trying to reach
        :param to_print: true if the user wants to print the traversal. false otherwise. 
        :return: the node we are trying to reach or None if it cannot be found
        """

        assert isinstance(start_node, int), "start_node must be an int"
        assert isinstance(target_node, int), "target_node must be an int"

        node = self.get_node_by_id(start_node)
        val = node.value
        if val == target_node:
            return node

        explored = set()
        frontier = Queue()
        frontier.put(node)
        found = False

        while not found:
            if frontier.empty():
                if to_print:
                    print "failed"
                return
            node = frontier.get()
            if to_print:
                print("visiting " + str(node))
            explored.add(node)
            children = node.neighbors
            for child in children:
                if child.value == target_node:
                    if to_print:
                        print("visiting " + str(child))
                    return child
                frontier.put(child)


if __name__ == "__main__":
    a = Node(1)
    b = Node(2)
    c = Node(3)
    d = Node(4)
    ab = Edge(a, b)
    bc = Edge(b, c)
    cd = Edge(c, d)
    g = Graph()
    g.add_node(a)
    g.add_node(b)
    g.add_node(c)
    g.add_node(d)
    g.add_edge(ab)
    g.add_edge(bc)
    g.add_edge(cd)
    g.bfs(0, 4, to_print=True)
    print(g)