import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile
from components.level import Level
from components.tree_component import Field, Aspect, Skill
from components.skill_list import Skill_List

# 预设等级
PRESET_LEVELS = [
    Level("基础", "grey", "初步了解"),
    Level("了解", "blue", "对其特性和用法有一定认识"),
    Level("熟练", "green", "能够独立完成中等复杂度的项目"),
    Level("高级", "yellow", "能够优化代码和解决复杂问题"),
]


@pytest.fixture
def skill_list():
    """初始化 Skill_List 实例"""
    return Skill_List(PRESET_LEVELS)


def test_parse_sample_file(skill_list):
    """测试解析提供的测试文本"""
    content = """
Programming
- Languages
-- Python
---+ 变量操作, 基础, 掌握基本变量声明和使用
---+ 面向对象, 熟练, 理解类与继承机制
-- Java
---+ 集合框架, 了解, 熟悉常用集合类型
- Tools
-- IDE
---+ PyCharm, 高级, 熟练使用调试和重构功能
Other
- Git
--+ 拉取更新, 熟练, 真的会拉
"""
    with NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(content.strip())
        file_path = f.name

    nodes = skill_list.parse_file(file_path)

    # 验证节点总数
    assert len(nodes) == 13

    # 验证根节点 Programming
    assert isinstance(nodes[0], Field)
    assert nodes[0].name == "Programming"
    assert nodes[0].node_level == 0

    # 验证 Languages 分支
    assert isinstance(nodes[1], Aspect)
    assert nodes[1].name == "Languages"
    assert nodes[1].node_level == 1

    # 验证 Python 分支
    assert isinstance(nodes[2], Aspect)
    assert nodes[2].name == "Python"
    assert nodes[2].node_level == 2

    # 验证 变量操作 技能
    assert isinstance(nodes[3], Skill)
    assert nodes[3].name == "变量操作"
    assert nodes[3].skill_level.name == "基础"
    assert nodes[3].describe == "掌握基本变量声明和使用"
    assert nodes[3].node_level == 3

    # 验证 面向对象 技能
    assert isinstance(nodes[4], Skill)
    assert nodes[4].name == "面向对象"
    assert nodes[4].skill_level.name == "熟练"
    assert nodes[4].describe == "理解类与继承机制"
    assert nodes[4].node_level == 3

    # 验证 Java 分支
    assert isinstance(nodes[5], Aspect)
    assert nodes[5].name == "Java"
    assert nodes[5].node_level == 2

    # 验证 集合框架 技能
    assert isinstance(nodes[6], Skill)
    assert nodes[6].name == "集合框架"
    assert nodes[6].skill_level.name == "了解"
    assert nodes[6].describe == "熟悉常用集合类型"
    assert nodes[6].node_level == 3

    # 验证 Tools 分支
    assert isinstance(nodes[7], Aspect)
    assert nodes[7].name == "Tools"
    assert nodes[7].node_level == 1

    # 验证 IDE 分支
    assert isinstance(nodes[8], Aspect)
    assert nodes[8].name == "IDE"
    assert nodes[8].node_level == 2

    # 验证 PyCharm 技能
    assert isinstance(nodes[9], Skill)
    assert nodes[9].name == "PyCharm"
    assert nodes[9].skill_level.name == "高级"
    assert nodes[9].describe == "熟练使用调试和重构功能"
    assert nodes[9].node_level == 3

    # 验证 Other 根节点
    assert isinstance(nodes[10], Field)
    assert nodes[10].name == "Other"
    assert nodes[10].node_level == 0

    # 验证 Git 分支
    assert isinstance(nodes[11], Aspect)
    assert nodes[11].name == "Git"
    assert nodes[11].node_level == 1

    # 验证 拉取更新 技能
    assert isinstance(nodes[12], Skill)
    assert nodes[12].name == "拉取更新"
    assert nodes[12].skill_level.name == "熟练"
    assert nodes[12].describe == "真的会拉"
    assert nodes[12].node_level == 2


def test_invalid_indent(skill_list):
    """测试非常规缩进"""
    content = """
Programming
   - Languages  # 3空格缩进（非常规）
"""
    with NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(content.strip())
        file_path = f.name

    with pytest.raises(ValueError, match="非常规缩进"):
        skill_list.parse_file(file_path)


def test_missing_parent(skill_list):
    """测试缺失父节点"""
    content = """
Programming
    - Languages
      ---+ 变量操作  # 缺少中间层级
"""
    with NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(content.strip())
        file_path = f.name

    with pytest.raises(ValueError, match="层级跳跃错误"):
        skill_list.parse_file(file_path)


def test_invalid_skill_prefix(skill_list):
    """测试无效技能前缀"""
    content = """
Programming
    - Languages
      --+ Python  # 无效前缀
"""
    with NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(content.strip())
        file_path = f.name

    with pytest.raises(ValueError, match="无效的技能前缀"):
        skill_list.parse_file(file_path)


def test_undefined_level(skill_list):
    """测试未定义等级"""
    content = """
Programming
    - Languages
      -- Python
        ---+ 变量操作, 未知等级
"""
    with NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(content.strip())
        file_path = f.name

    with pytest.raises(ValueError, match="未定义的等级"):
        skill_list.parse_file(file_path)


def test_empty_file(skill_list):
    """测试空文件"""
    with NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        file_path = f.name

    nodes = skill_list.parse_file(file_path)
    assert len(nodes) == 0