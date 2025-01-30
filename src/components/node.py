from abc import ABC, abstractmethod


class Node(ABC):
    """Abstract base class for tree nodes."""
    def __init__(self, name: str = "", parent: 'Node' = None):
        self.name = name
        self.parent_node = parent

    @property
    def node_level(self) -> int:
        """Dynamically calculate level based on parent."""
        return self.parent_node.node_level + 1 if self.parent_node else 0

    @property
    @abstractmethod
    def is_leaf(self) -> bool:
        """Whether the node is a leaf (no children)."""
        pass

    def get_path(self) -> str:
        """Generate the node's path from root."""
        path = []
        current = self
        while current:
            path.append(current.name)
            current = current.parent_node
        return "/".join(reversed(path))


class Root(Node):
    """Root node of the tree."""
    def __init__(self, name: str):
        super().__init__(name)

    @property
    def is_leaf(self) -> bool:
        return False


class Twig(Node):
    """Non-leaf branch node."""
    def __init__(self, name: str, parent: Node):
        if parent is None:
            raise ValueError("Twig requires a parent node.")
        super().__init__(name, parent)

    @property
    def is_leaf(self) -> bool:
        return False


class Leaf(Node):
    """Leaf node with no children."""
    def __init__(self, name: str, parent: Node):
        if parent is None:
            raise ValueError("Leaf requires a parent node.")
        super().__init__(name, parent)

    @property
    def is_leaf(self) -> bool:
        return True