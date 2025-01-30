import pytest
from components.level import Level
from components.tree_component import Field, Aspect, Skill
from components.node import Node


@pytest.fixture
def sample_level():
    """预设等级 fixture"""
    return Level("高级", "yellow", "能够优化代码")


@pytest.fixture
def sample_field():
    """预设领域 fixture"""
    return Field("编程")


# Field 类测试
class TestField:
    def test_valid_initialization(self):
        """测试有效领域初始化"""
        field = Field("编程")
        assert field.name == "编程"
        assert field.parent_node is None
        assert field.node_level == 0

    def test_empty_name_validation(self):
        """测试空名称验证"""
        with pytest.raises(ValueError, match="领域名称不能为空"):
            Field("")


# Aspect 类测试
class TestAspect:
    def test_valid_parent_types(self, sample_field):
        """测试有效父节点类型（Field 和 Aspect）"""
        # Field 作为父节点
        aspect1 = Aspect("语言", sample_field)
        assert aspect1.parent_node == sample_field
        assert aspect1.node_level == 1

        # Aspect 作为父节点
        aspect2 = Aspect("Python", aspect1)
        assert aspect2.parent_node == aspect1
        assert aspect2.node_level == 2

    def test_invalid_parent_type(self):
        """测试无效父节点类型"""
        invalid_parent = Skill("无效", None, Level("test", "red", "test"), "test")
        with pytest.raises(TypeError, match="分支节点的父节点必须是领域或其他分支"):
            Aspect("无效分支", invalid_parent)

    def test_missing_parent(self):
        """测试父节点为空"""
        with pytest.raises(ValueError, match="Twig requires a parent node."):
            Aspect("孤岛分支", None)


# Skill 类测试
class TestSkill:
    def test_valid_skill_creation(self, sample_field, sample_level):
        """测试有效技能节点创建"""
        aspect = Aspect("Python", sample_field)
        skill = Skill("面向对象", aspect, sample_level)

        assert skill.parent_node == aspect
        assert skill.node_level == 2
        assert skill.skill_level == sample_level
        assert skill.describe == sample_level.describe
        assert skill.level_color == "yellow"

    def test_custom_description(self, sample_field, sample_level):
        """测试自定义描述覆盖"""
        aspect = Aspect("Python", sample_field)
        custom_desc = "自定义描述内容"
        skill = Skill("面向对象", aspect, sample_level, describe=custom_desc)
        assert skill.describe == custom_desc

    def test_invalid_parent_type(self, sample_level):
        """测试无效父节点类型"""
        invalid_parent = Field("无效父节点")
        with pytest.raises(TypeError, match="技能节点必须属于分支节点"):
            Skill("无效技能", invalid_parent, sample_level)


# 综合层级测试
class TestHierarchy:
    def test_multi_level_structure(self, sample_level):
        """测试多级结构路径和层级"""
        # 构建结构: Field -> Aspect1 -> Aspect2 -> Skill
        field = Field("编程")
        aspect1 = Aspect("语言", field)
        aspect2 = Aspect("Python", aspect1)
        skill = Skill("装饰器", aspect2, sample_level)

        # 验证层级
        assert field.node_level == 0
        assert aspect1.node_level == 1
        assert aspect2.node_level == 2
        assert skill.node_level == 3

        # 验证路径
        assert skill.get_path() == "编程/语言/Python/装饰器"

    def test_skill_path_generation(self, sample_field, sample_level):
        """测试技能节点路径生成"""
        aspect = Aspect("框架", sample_field)
        skill = Skill("Django", aspect, sample_level)
        assert skill.get_path() == "编程/框架/Django"