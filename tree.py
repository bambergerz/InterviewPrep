from graph import Node
from graph import Graph
from graph import Edge


class Tree(Graph):
    def __init__(self, root):
        assert isinstance(root, Node), "root is not a Node instance"
        super(Tree, self).__init__()
        self._root = root
        self._children = []

    @property
    def root(self):
        return self._root

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        """
        
        :param child: The node we are adding as a child of this root
        :return: None
        """
        assert isinstance(child, Node), "child is not a Node instance"
        self._children.append(child)
        edge = Edge(self.root, child, child.value - self.root.value)
        self.add_edge(edge)
        self.add_node(child)

    def dfs(self, start_node, target_node, to_print=1):
        return super(Tree, self).dfs(start_node, target_node, to_print)

    def bfs(self, start_node, target_node, to_print=1):
        return super(Tree, self).bfs(start_node, target_node, to_print)


class BinaryTree(object):

    def __init__(self, root):
        assert isinstance(root, Node)
        self._root = root
        self._lc = None
        self._rc = None

    @property
    def root(self):
        return self._root

    @property
    def left_child(self):
        return self._lc

    @property
    def right_child(self):
        return self._rc

    def add_left_child(self, child):
        assert isinstance(child, Node)
        assert self.left_child is None, "left child already exists"
        assert child.value < self.root.value, \
            "left child's value must be smaller than " + str(self.root.value)
        self._lc = child

    def add_right_child(self, child):
        assert isinstance(child, Node)
        assert self.right_child is None, "right child already exists"
        assert child.value >= self.root.value,\
            "right child's value must be greater than or equal to " + str(self.root.value)
        self._rc = child

    def binary_search(self, target_value):
        if self.root.value == target_value:
            return self.root
        else:
            if target_value < self.root.value:
                lc = self.left_child
                return lc.binary_search(target_value)
            else:
                rc = self.right_child
                return rc.binary_search(target_value)

if __name__ == "__main__":
    a = Node(1)
    t = Tree(a)
