class Node:
    """Abstract class for Root, Twig, and Leaf"""

    def __init__(self, name: str = "", parent: 'Node' = None):
        self.name = name
        self.parent_node = parent
        self.level = parent.level + 1 if parent else 0

    def get_path(self):
        """Return the full path from the root to this node."""
        path = []
        node = self
        while node:
            path.append(node.name)
            node = node.parent_node
        return "/".join(reversed(path))


class Root(Node):
    """The Root of a tree"""

    def __init__(self, name: str = "Root"):
        super().__init__(name)
        self.level = 0  # Root is always level 0
        self.parent_node = None  # Root has no parent


class Twig(Node):
    """The branches for a tree, which can have multiple levels."""

    def __init__(self, name: str, parent: Node):
        if parent is None:
            raise ValueError("Twig's parent node cannot be None.")
        super().__init__(name, parent)


class Leaf(Node):
    """The final nodes (leaves) of a tree, which do not have children."""

    def __init__(self, name: str, parent: Node):
        if parent is None:
            raise ValueError("Leaf's parent node cannot be None.")
        super().__init__(name, parent)


