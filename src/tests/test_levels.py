import pytest
from components.level import Level
from components.levels import Levels

# 预设等级参数
PRESET_LEVELS = [
    ("基础", "grey", "对某种语言或框架有初步了解，能进行简单的编码或操作。"),
    ("了解", "blue", "对其特性和用法有一定认识，能够完成一些基础项目。"),
    ("熟练", "green", "能够独立完成中等复杂度的项目，熟悉其主要特性和最佳实践。"),
    ("高级", "yellow", "在该语言或框架上有较深的理解，能够优化代码和解决复杂问题。"),
    ("精通", "red", "能够深入理解和应用其底层原理，参与框架的设计或贡献开源。"),
    ("专家", "black", "在该领域具有广泛的影响力，能够进行教学或指导他人，解决行业内的复杂挑战。"),
]


@pytest.fixture
def initialized_levels() -> Levels:
    """初始化带有预设等级的 Levels 实例"""
    levels = Levels()
    levels.add_levels_via_list(PRESET_LEVELS)
    return levels


def test_levels_initialization():
    """测试空初始化和带参初始化"""
    # 空初始化
    empty_levels = Levels()
    assert len(empty_levels.list) == 0

    # 带参初始化
    level = Level("测试", "white", "测试描述")
    levels_with_param = Levels([level])
    assert len(levels_with_param.list) == 1
    assert levels_with_param.list[0].name == "测试"


def test_add_level(initialized_levels, capsys):
    """测试添加单个等级（含重复处理）"""
    # 添加新等级
    initialized_levels.add_level(("大师", "purple", "超越专家水平"))
    assert len(initialized_levels.list) == 7
    assert initialized_levels.list[-1].name == "大师"

    # 添加重复等级
    initialized_levels.add_level(("基础", "grey", "重复描述"))
    captured = capsys.readouterr()
    assert "('基础', 'grey'," in captured.out  # 检查重复提示
    assert len(initialized_levels.list) == 7  # 数量不变


def test_add_levels_via_list(initialized_levels, capsys):
    """测试批量添加等级（含重复项）"""
    # 正常批量添加
    new_levels = [("入门", "pink", "入门级技能"), ("资深", "orange", "资深开发者")]
    initialized_levels.add_levels_via_list(new_levels)
    assert len(initialized_levels.list) == 8
    assert initialized_levels.list[-1].name == "资深"

    # 添加包含重复项的列表
    initialized_levels.add_levels_via_list([("基础", "grey", "重复描述")])
    captured = capsys.readouterr()
    assert "('基础', 'grey'," in captured.out  # 检查重复提示
    assert len(initialized_levels.list) == 8  # 数量不变


def test_search_by_name(initialized_levels):
    """测试按名称搜索等级（含异常处理）"""
    # 正常搜索
    advanced = initialized_levels.search_by_name("高级")
    assert advanced.color == "yellow"
    assert "优化代码" in advanced.describe

    # 搜索不存在的等级
    with pytest.raises(KeyError) as exc_info:
        initialized_levels.search_by_name("不存在的等级")
    assert "Level with Name [不存在的等级] not found" in str(exc_info.value)


def test_print_all_levels(initialized_levels):
    """测试生成 Markdown 输出"""
    output = initialized_levels.print_all_levels()

    # 验证总行数和关键内容
    lines = output.split("\n")
    assert len(lines) == 7  # 6个等级 + 最后空行
    assert "-<abbr title=\"能够独立完成中等复杂度的项目" in lines[2]
    assert "<font color=\"green\">熟练</font>" in lines[2]
    assert "<font color=\"black\">专家</font>" in lines[5]