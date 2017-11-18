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
        """
        
        :return: the root of this tree
        """
        return self._root

    @property
    def children(self):
        """
        
        :return: the children of the root of this tree.
        """
        return self._children

    def add_child(self, child):
        """
        
        :param child: The node we are adding as a child of this root
        :return: None
        """
        assert isinstance(child, Node), "child is not a Node instance"
        self._children.append(Tree(child))
        edge = Edge(self.root, child, child.value - self.root.value)
        self.add_edge(edge)
        self.add_node(child)

    def dfs(self, start_node, target_node, to_print=1):
        """
        
        :param start_node: the id of the starting node of the DFS
        :param target_node: the id of the target node of the DFS
        :param to_print: True if the user wants to print the progression of the DFS. False otherwise. 
        :return: the node we are looking for. 
        """
        return super(Tree, self).dfs(start_node, target_node, to_print)

    def bfs(self, start_node, target_node, to_print=1):
        return super(Tree, self).bfs(start_node, target_node, to_print)


class BinaryTree(object):

    def __init__(self, root):
        """
        
        :param root: the root of this tree object
        """
        assert isinstance(root, Node)
        self._root = root
        self._lc = None
        self._rc = None

    @property
    def root(self):
        """
        
        :return: the root of this tree
        """
        return self._root

    @property
    def left_child(self):
        """
        
        :return: the left child of the root. Either a Node object or None.
        """
        return self._lc

    @property
    def right_child(self):
        """
        
        :return: the right child of the root. Either a node object or None. 
        """
        return self._rc

    def insert(self, node):
        """
        
        :param node: insert node into the tree in its proper spot
        :return: None
        """
        if node.value < self.root.value:
            if self.left_child is not None:
                self.left_child.insert(node)
            else:
                self._lc = BinaryTree(node)
        else:
            if self.right_child is not None:
                self.right_child.insert(node)
            else:
                self._rc = BinaryTree(node)

    def binary_search(self, target_value):
        """
        
        :param target_value: the value of the node we are searching for in the tree. 
        :return: the node which contains that value. 
        """
        if self.root.value == target_value:
            return self.root
        else:
            if target_value < self.root.value:
                lc = self.left_child
                return lc.binary_search(target_value)
            else:
                rc = self.right_child
                return rc.binary_search(target_value)

    def in_order(self):
        """
        Print the in-order traversal of this tree. 
        
        :return: Mothing.
        """
        has_left = self.left_child is not None
        has_right = self.right_child is not None
        if has_left:
            self.left_child.in_order()
        print(self.root.value)
        if has_right:
            self.right_child.in_order()

    def pre_order(self):
        """
        print the pre-order traversal of this tree.
        
        :return: None
        """
        has_left = self.left_child is not None
        has_right = self.right_child is not None
        print(self.root.value)
        if has_left:
            self.left_child.pre_order()
        if has_right:
            self.right_child.pre_order()

    def post_order(self):
        """
        print the post-order traversal of this tree.
        
        :return: None 
        """
        has_left = self.left_child is not None
        has_right = self.right_child is not None
        if has_right:
            self.right_child.post_order()
        print(self.root.value)
        if has_left:
            self.left_child.post_order()

if __name__ == "__main__":
    a = Node(1)
    b = Node(2)
    c = Node(3)
    d = Node(4)
    e = Node(5)
    f = Node(6)
    g = Node(7)
    tree = Tree(a)
    binary_tree = BinaryTree(d)
    binary_tree.insert(f)
    binary_tree.insert(c)
    binary_tree.insert(b)
    binary_tree.insert(a)
    binary_tree.insert(e)
    binary_tree.insert(g)

    print(binary_tree.in_order())
    print("\n" * 3)
    print(binary_tree.pre_order())
