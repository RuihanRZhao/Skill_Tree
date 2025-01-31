import re
from typing import List, Optional, Union
from components.node import Node
from components.tree_component import Field, Aspect, Skill
from components.level import Level


class Skill_List:
    def __init__(self, levels: List[Level]):
        """
        初始化技能列表解析器。
        :param levels: 预定义的等级配置系统，存储为字典，键为等级名称，值为 Level 实例。
        """
        self.levels = {level.name: level for level in levels}
        # 使用连字符（-）计数来计算深度
        # 不再使用固定的缩进单位

        # 新的正则表达式：
        # 1. ^([-]*)         捕获开头的零个或多个横杠，表示层级
        # 2. (\+?)           捕获可选的加号，表示技能
        # 3. \s*             跳过空格
        # 4. ([^,]+?)        捕获节点名称（非逗号直到第一个逗号或行结束）
        # 5. 接下来可选地捕获等级和描述，形如 , 等级 , 描述
        self._line_regex = re.compile(
            r"^([-]*)(\+?)\s*"       # 层级(横杠)和可选的+号
            r"([^,]+?)\s*"          # 节点名称
            r"(?:,\s*([^,]+?)\s*"   # 可选的等级
            r"(?:,\s*(.+?)\s*)?)?$" # 可选的描述
        )

    def parse_file(self, file_path: str) -> List[Node]:
        """
        从文件解析完整技能树。
        :param file_path: 技能树文件路径
        :return: 解析后的节点列表
        """
        nodes = []  # 存储解析的节点
        parent_stack = []  # 用于管理层级结构的父节点栈

        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip('\n')
                if not line.strip():  # 跳过空行
                    continue

                node = self._parse_line(line, line_num, parent_stack)
                nodes.append(node)

        return nodes

    def _parse_line(self, line: str, line_num: int, parent_stack: list) -> Node:
        """
        解析技能树文件中的单行。
        :param line: 当前行文本
        :param line_num: 当前行号（用于错误提示）
        :param parent_stack: 父节点栈
        :return: 解析出的节点
        """
        match = self._line_regex.match(line)
        if not match:
            raise ValueError(f"格式错误（第{line_num}行）: {line}")

        dash_part, plus_part, name, level_name, describe = match.groups()
        # 根据横杠数量计算深度
        depth = len(dash_part) if dash_part else 0

        # 根据是否存在 plus_part 来判断是不是技能
        # 如果 plus_part 非空则是技能，否则如果 dash_part 非空则是分支，否则是领域
        node_type = self._determine_node_type(dash_part, plus_part)

        # 确保层级结构正确
        # self._validate_hierarchy(depth, parent_stack, line_num)

        # 根据不同节点类型创建对应的节点
        if node_type == "field":
            return self._create_field(name, parent_stack)
        elif node_type == "aspect":
            return self._create_aspect(name, depth, parent_stack, line_num)
        else:
            return self._create_skill(name, level_name, describe, parent_stack, line_num)

    def _determine_node_type(self, dash_part: str, plus_part: str) -> str:
        """
        根据横杠和加号确定节点类型。
        :param dash_part: 横杠部分字符串
        :param plus_part: '+' 或空字符串
        :return: "field" | "aspect" | "skill"
        """
        if plus_part:  # 如果包含 plus_part，说明是技能
            return "skill"
        elif dash_part:  # 有横杠但无 plus_part，即分支
            return "aspect"
        else:  # 没有横杠，也没有 plus_part
            return "field"

    def _validate_hierarchy(self, depth: int, parent_stack: list, line_num: int):
        """
        确保层级结构正确。
        :param depth: 由横杠数量得到的层级深度
        :param parent_stack: 父节点栈
        :param line_num: 当前行号
        """
        # 如果 depth == 0 则应当是根节点（领域）
        if depth == 0:
            # 如果栈已经有内容，说明已经定义过一个根节点
            # 根据需求，这里可以决定是否允许多个根节点
            if parent_stack:
                # 如果允许多个根节点，可以注释掉或移除该异常
                raise ValueError(f"根节点重复定义（第{line_num}行）")
        # 如果 depth > len(parent_stack) + 1，说明层级跳跃
        elif depth > len(parent_stack):
            raise ValueError(f"层级跳跃错误（第{line_num}行）")
        else:
            # 如果 depth <= len(parent_stack)，需要回退到指定层级
            while depth < len(parent_stack):
                parent_stack.pop()

    def _create_field(self, name: str, parent_stack: list) -> Field:
        """
        创建领域（根节点）。
        :param name: 领域名称
        :param parent_stack: 父节点栈
        :return: Field 实例
        """
        field = Field(name)
        # 清空栈并压入这个新的根节点
        parent_stack.clear()
        parent_stack.append(field)
        return field

    def _create_aspect(self, name: str, depth: int, parent_stack: list, line_num: int) -> Aspect:
        """
        创建分支节点。
        :param name: 分支名称
        :param depth: 当前层级
        :param parent_stack: 父节点栈
        :param line_num: 当前行号
        :return: Aspect 实例
        """
        # 如果当前深度与栈大小相同，说明是同级分支，需要获取上一级的父亲
        # 如果 depth < len(parent_stack)，前面 _validate_hierarchy 已经弹出了不需要的父节点
        # 因此此时 parent_stack[-1] 就是当前需要挂载的父节点
        if depth == 1:
            parent = None
            for i in parent_stack:
                if isinstance(i, Field):
                    parent = i
        if depth > 1:
            parent = parent_stack[-1]

        # 如果 depth == 1，则父节点应该是 Field；如果 depth > 1，则父节点可以是 Aspect
        if depth == 1 and not isinstance(parent, Field):
            raise TypeError(f"一级分支必须属于Field（第{line_num}行）")
        if depth > 1 and not isinstance(parent, Aspect):
            raise TypeError(f"更深层次的分支必须属于分支（第{line_num}行）")

        aspect = Aspect(name, parent)
        parent_stack.append(aspect)
        return aspect

    def _create_skill(self, name: str, level_name: str, describe: str, parent_stack: list, line_num: int) -> Skill:
        """
        创建技能节点。
        :param name: 技能名称
        :param level_name: 技能等级
        :param describe: 技能描述
        :param parent_stack: 父节点栈
        :param line_num: 当前行号
        :return: Skill 实例
        """
        parent = parent_stack[-1]
        if not isinstance(parent, Aspect):
            raise TypeError(f"技能必须属于分支（第{line_num}行）")

        # 如果未提供 level_name，则默认使用 \"基础\" 等级
        level_key = level_name or "基础"
        if level_key not in self.levels:
            raise ValueError(f"未定义的等级: {level_key}（第{line_num}行")
        level = self.levels[level_key]

        return Skill(
            name=name,
            parent=parent,
            skill_level=level,
            describe=describe
        )



# 预设等级
PRESET_LEVELS = [
    Level("基础", "grey", "初步了解"),
    Level("了解", "blue", "对其特性和用法有一定认识"),
    Level("熟练", "green", "能够独立完成中等复杂度的项目"),
    Level("高级", "yellow", "能够优化代码和解决复杂问题"),
    Level("精通", "red", "能够深入理解和应用其底层原理"),
    Level("专家", "black", "在该领域具有广泛的影响力"),
]

if __name__ == "__main__":
    # 初始化 Skill_List
    skill_list = Skill_List(PRESET_LEVELS)

    # 技能树文件内容
    skill_tree_content = """
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

    # 将内容写入临时文件
    with open("skill_tree.skilltree", "w", encoding="utf-8") as f:
        f.write(skill_tree_content.strip())

    # 解析技能树文件
    nodes = skill_list.parse_file("skill_tree.skilltree")

    # 打印节点信息
    print("=== 解析结果 ===")
    for node in nodes:
        indent = "  " * node.node_level
        node_type = type(node).__name__
        print(f"{indent}{node.name} ({node_type})")

    # 生成 Markdown 文件
    markdown_content = "# 技能树\n\n"
    for node in nodes:
        indent = "  " * node.node_level
        if isinstance(node, Field):
            markdown_content += f"{indent}## {node.name}\n"
        elif isinstance(node, Aspect):
            markdown_content += f"{indent}### {node.name}\n"
        elif isinstance(node, Skill):
            markdown_content += f"{indent}- **{node.name}** ({node.skill_level.name}): {node.describe}\n"

    with open("skill_tree.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print("\n=== Markdown 文件已生成 ===")
    print("文件路径: skill_tree.md")