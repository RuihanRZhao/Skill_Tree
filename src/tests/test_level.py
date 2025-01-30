import pytest
from ..components.level import Level


def test_level_initialization():
    """测试等级对象初始化"""
    level = Level("基础", "grey", "初步了解")
    assert level.name == "基础"
    assert level.color == "grey"
    assert level.describe == "初步了解"


def test_level_str_representation():
    """测试等级对象的字符串表示"""
    level = Level("高级", "yellow", "深入理解")
    assert str(level) == "[Level: 高级, Color: yellow, Describe: 深入理解]"


def test_level_equality():
    """测试等级对象相等性"""
    level1 = Level("基础", "grey", "初步了解")
    level2 = Level("基础", "grey", "初步了解")
    level3 = Level("高级", "yellow", "深入理解")

    # 相同对象
    assert level1 == level2
    # 不同对象
    assert level1 != level3
    # 与非等级对象比较
    assert level1 != "非等级对象"


def test_generate_markdown():
    """测试生成 Markdown"""
    level = Level("高级", "yellow", "深入理解")
    markdown = level.generate_markdown()

    # 验证 Markdown 格式
    assert markdown == (
        '<abbr title="深入理解">'
        '<font color="yellow">高级</font>'
        '</abbr>'
    )
    # 验证包含关键内容
    assert "yellow" in markdown
    assert "高级" in markdown
    assert "深入理解" in markdown