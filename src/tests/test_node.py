import pytest
from ..components.node import Node, Root, Twig, Leaf


def test_root_node():
    """测试根节点"""
    root = Root("Programming")
    assert root.name == "Programming"
    assert root.parent_node is None
    assert root.node_level == 0
    assert root.is_leaf is False
    assert root.get_path() == "Programming"


def test_twig_node():
    """测试分支节点"""
    root = Root("Programming")
    twig = Twig("Languages", root)

    # 验证属性
    assert twig.name == "Languages"
    assert twig.parent_node == root
    assert twig.node_level == 1
    assert twig.is_leaf is False
    assert twig.get_path() == "Programming/Languages"

    # 验证父节点为空的异常
    with pytest.raises(ValueError, match="Twig requires a parent node."):
        Twig("Invalid", None)


def test_leaf_node():
    """测试叶节点"""
    root = Root("Programming")
    twig = Twig("Languages", root)
    leaf = Leaf("Python", twig)

    # 验证属性
    assert leaf.name == "Python"
    assert leaf.parent_node == twig
    assert leaf.node_level == 2
    assert leaf.is_leaf is True
    assert leaf.get_path() == "Programming/Languages/Python"

    # 验证父节点为空的异常
    with pytest.raises(ValueError, match="Leaf requires a parent node."):
        Leaf("Invalid", None)


def test_node_hierarchy():
    """测试多层级节点关系"""
    root = Root("Programming")
    twig1 = Twig("Languages", root)
    twig2 = Twig("Frameworks", root)
    leaf1 = Leaf("Python", twig1)
    leaf2 = Leaf("Django", twig2)

    # 验证层级
    assert root.node_level == 0
    assert twig1.node_level == 1
    assert twig2.node_level == 1
    assert leaf1.node_level == 2
    assert leaf2.node_level == 2

    # 验证路径
    assert leaf1.get_path() == "Programming/Languages/Python"
    assert leaf2.get_path() == "Programming/Frameworks/Django"


def test_abstract_node():
    """测试抽象基类 Node 无法实例化"""
    with pytest.raises(TypeError):
        Node("AbstractNode")