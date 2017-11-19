from Queue import Queue, PriorityQueue
import heapq
import logging
import os
import sys


class Node(object):
    node_ID = 0

    def __init__(self, value):
        """
        
        :param value: an int. This Node instance will take this value
        """
        assert isinstance(value, int)
        self._id = Node.node_ID
        self._value = value
        self._neighbors = set()
        self._edges = {}
        Node.node_ID += 1

    def __repr__(self):
        return str(self.value)

    def __gt__(self, other):
        assert isinstance(other, Node)
        return self.value > other.value

    def __lt__(self, other):
        assert isinstance(other, Node)
        return self.value < other.value

    def __eq__(self, other):
        print(type(self))
        print(type(other))
        assert isinstance(other, Node)
        return self._value == other.value

    def __copy__(self):
        cp = Node(self.value)
        for n in self.neighbors:
            cp.add_neighbor(n)
        return cp

    @property
    def node_id(self):
        return self._id

    @property
    def value(self):
        return self._value

    @property
    def neighbors(self):
        return self._neighbors

    @property
    def edges(self):
        return self._edges

    def set_value(self, value):
        self._value = value

    def add_neighbor(self, neighbor, weight=0):
        """
        
        :param neighbor: a neighbor node of this Node instance
        :param weight: the weight of the edge from the current node to its neighbor
        :return: True once "neighbor" has been appended to this node's list of neighbors. 
        """
        assert isinstance(neighbor, Node)
        self._neighbors.add(neighbor)
        edge = Edge(self, neighbor, weight)
        self._edges[neighbor] = edge

    def get_edge(self, target):
        """
        
        :param target: return the edge between the current node and the target node if it exists. 
        If this edge does not exist, return None.
        :return: 
        """
        if target in self.neighbors:
            return self.edges[target]
        else:
            print "This node does not share an edge with node: " + str(target)
            return None


class Edge(object):
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


class Graph(object):
    graph_ID = 0

    def __init__(self, bidirectional=False):
        """
        
        :param bidirectional: whether or not the graph is bidirectional
        if the graph is bidirectional, the weight from a to b must be the weight from b to a. 
        """
        self._nodes = []
        self._edges = {}  # map a source node to all the edges which leave from it.
        self._bidirectional = bidirectional
        self._id = Graph.graph_ID
        self.set_up_logger()

    def __str__(self):
        msg = ""
        msg += "Nodes are: " + str(self._nodes) + "\n"
        msg += "Edges are: " + str(self._edges.values())
        return msg

    def set_up_logger(self):
        # set up the logger
        filename = "graph%d.log" % self._id
        cur_dir = os.getcwd()
        if filename in os.listdir(cur_dir):
            os.remove(filename)
        logging.basicConfig(filename="graph%d.log" % self._id,
                            level=logging.INFO,
                            format='%(asctime)s:\n%(message)s\n\n',
                            datefmt='%m/%d/%Y %I:%M:%S %p')


    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        """
        
        :return: the list of the edges in this graph.
        """
        return self._edges.values()

    def get_edges_from_node(self, node_id):
        node = self.get_node_by_id(node_id)
        return self._edges[node]

    def print_properties(self):
        msg = "Bidirectional? " + str(self._bidirectional)
        print msg

    def add_node(self, node):
        """
        
        :param node: the node object we are adding to the graph.
        :return: True once the node has been added to the graph.
        """
        assert isinstance(node, Node), "node is not a Node instance"
        self._nodes.append(node)
        return True

    def add_edge(self, edge):
        """
        
        :param edge: An edge object to add to this graph
        :return: True once an edge has been added to this graph
        """
        assert isinstance(edge, Edge), "edge is not an Edge instance"

        source = edge.source
        target = edge.target
        self._edges[edge.source.node_id] = edge
        source.add_neighbor(target)

        if self._bidirectional:
            potential_hazards = self._edges[target.node_id]
            for edge in potential_hazards:
                if edge.source.node_id == target.node_id and edge.target.node_id == source.node_id:
                    print("This is bidirectional graph and an edge between these nodes already exists")
                    return False

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
        print("cannot find node with this ID in the graph")
        logging.debug("Cannot find a node with id \"" + str(node_id) + "\"")
        return

    def get_edge_by_id(self, edge_id):
        """
        
        :param edge_id: the id of the edge we are trying to return
        :return: either the edge with the ID we are looking for or None if
        that edge does not currently exist in our graph.
        """

        assert isinstance(edge_id, int), "edge_id must be an int"
        for i in self._edges.values():
            if i.edge_id == edge_id:
                return i
        print("Cannot find the edge with this ID in the graph")
        logging.debug("Cannot find an edge with the id \"" + str(edge_id) + "\"")

    def bfs(self, start_node, target_node, to_print=1):
        """
        
        :param start_node: the ID of the node from which we are starting
        :param target_node: the ID of the node we are trying to reach
        :param to_print: true if the user wants to print the traversal. false otherwise. 
        :return: the node we are trying to reach or None if it cannot be found
        """

        assert isinstance(start_node, int), "start_node must be an int"
        assert isinstance(target_node, int), "target_node must be an int"

        msg = "BFS path: "
        node = self.get_node_by_id(start_node)
        val = node.node_id
        if val == target_node:
            msg += str(val)

            return node

        explored = set()
        frontier = Queue()
        frontier.put(node)

        while True:
            if frontier.empty():
                msg += "failed\n"
                logging.info(msg)
                if to_print:
                    print msg
                return
            node = frontier.get()
            msg += str(node) + " -> "
            explored.add(node)
            children = node.neighbors
            for child in children:
                if child.node_id == target_node:
                    msg += str(child) + "\n"
                    logging.info(msg)
                    if to_print:
                        print msg
                    return child
                frontier.put(child)

    def dfs(self, start_node, target_node, to_print=1):
        """

        :param start_node: the ID of the node from which we are starting
        :param target_node: the ID of the node we are trying to reach
        :param to_print: true if the user wants to print the traversal. false otherwise. 
        :return: the node we are trying to reach or None if it cannot be found
        """

        assert isinstance(start_node, int), "start_node must be an int"
        assert isinstance(target_node, int), "target_node must be an int"

        msg = "DFS path: "
        node = self.get_node_by_id(start_node)
        val = node.node_id
        if val == target_node:
            msg += str(val)
            if to_print:
                print(msg)
            logging.info(msg)
            return node

        explored = set()
        frontier = []
        frontier.append(node)
        found = False

        while not found:
            if len(frontier) == 0:
                msg += "failed\n"
                logging.info(msg)
                if to_print:
                    print msg
                return
            node = frontier.pop()
            msg += str(node) + " -> "
            explored.add(node)
            children = node.neighbors
            for child in children:
                if child.node_id == target_node:
                    msg += str(child) + "\n"
                    logging.info(msg)
                    if to_print:
                        print msg
                    return child
                frontier.append(child)

    def bellmen_ford(self, source, to_print=1):
        """
        
        :param source: the source of the propagation for Bellman Ford algorithm.
        an int which represents a valid node id.
        :return: a tuple consisting of distances 
        """
        assert isinstance(source, int)

        # TODO: optimize for loop such that if no values change
        #  between two iterations, return immediately

        msg = "Bellman Ford:\n"
        distances = {}
        predecessors = {}
        for node in self.nodes:
            distances[node.node_id] = sys.maxint
            predecessors[node.node_id] = None

        origin = self.get_node_by_id(source)
        distances[origin.node_id] = 0
        msg += ("Upon initialization, distances are: " + str(distances) + "\n")
        msg += ("Upon initialization, predecessors are: " + str(predecessors) + "\n")

        # relax stage of BF:

        for i in range(len(self.nodes) - 1):
            for e in self.edges:
                if distances[e.target.node_id] > distances[e.source.node_id] + e.weight:
                    distances[e.target.node_id] = distances[e.source.node_id] + e.weight
                    predecessors[e.target.node_id] = e.source.node_id

            msg += "\nUpdated distances: " + str(distances) + "\n"
            msg += "Updated predecessors: " + str(predecessors) + "\n"

        # check for negative weight cycle:

        for e in self.edges:
            assert isinstance(e, Edge)
            if distances[e.source.node_id] + e.weight < distances[e.target.node_id]:
                print("Graph contains a negative weight cycle!")
                return None, None

        msg += ("\nFinal distances are: " + str(distances) + '\n')
        msg += ("Final predecessors are: " + str(predecessors) + "\n")
        if to_print: print msg
        logging.info(msg)

        return distances, predecessors

    def deijkstra(self, source, to_print=1):
        """
        
        :param source: the source of the propagation Deisjkstra's algorithm.
        an int which represents a valid node id.
        :param to_print: True if you wish to print the progression of the algorithm. False otherwise. 
        :return: a tuple consisting of (distances, predecessors)
        distances is an array of nodes
        predecessors is an array of nodes.
        """
        distances = {}
        predecessors = {}
        Q = []
        source_node = self.get_node_by_id(source)
        for x in self.nodes:
            distances[x] = sys.maxint
            predecessors[x] = None
            Q.append(x)
        distances[source_node] = 0

        if to_print:
            print("Initial distances are " + str(distances))
            print("Initial predecessors are " + str(predecessors) + "\n")

        while len(Q) > 0:
            min_dist = sys.maxint
            min_node = None
            for node, dist in distances.items():
                if dist < min_dist:
                    min_node = node
                    min_dist = dist

            Q.remove(min_node)

            for v in min_node.neighbors:
                assert isinstance(v, Node)
                alternative = distances[min_node] + min_node.get_edge(v).weight
                if alternative < distances[v]:
                    distances[v] = alternative
                    predecessors[v] = min_node

            if to_print:
                print("Updated distances are: " + str(distances))
                print("Updated predecessors are: " + str(predecessors) + "\n")

        if to_print:
            print("Final distances are: " + str(distances))
            print("Updated predecessors are: " + str(predecessors))

        return distances, predecessors


if __name__ == "__main__":
    a = Node(1)
    b = Node(2)
    c = Node(3)
    d = Node(4)
    ab = Edge(a, b, 2)
    bc = Edge(b, c, -1)
    cd = Edge(c, d, 5)
    g = Graph()
    g.add_node(a)
    g.add_node(b)
    g.add_node(c)
    g.add_node(d)
    g.add_edge(ab)
    g.add_edge(bc)
    g.add_edge(cd)
    g.bfs(0, 3, to_print=True)
    g.dfs(0, 3, to_print=True)
    distances, predecessors = g.bellmen_ford(0, to_print=True)
    distances, predecessors = g.deijkstra(0, to_print=True)
