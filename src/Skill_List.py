import re
import tempfile
from typing import List, Optional, Union
from components.node import Node
from components.tree_component import Field, Aspect, Skill
from components.level import Level


class Skill_List:
    def __init__(self, levels: List[Level]):
        """
        :param levels: 预定义的等级配置系统
        """
        self.levels = {level.name: level for level in levels}
        self._indent_unit = 2  # 缩进单位（空格数）
        self._line_regex = re.compile(
            r"^(\s*)(-*)\+?\s*"  # 缩进和前缀
            r"([^,]+?)\s*"  # 节点名称
            r"(?:,\s*([^,]+?)\s*"  # 等级名称（可选）
            r"(?:,\s*(.+?)\s*)?)?$"  # 描述（可选）
        )

    def parse_file(self, file_path: str) -> List[Node]:
        """从文件解析完整技能树"""
        nodes = []
        parent_stack = []

        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip('\n')
                if not line.strip():
                    continue

                node = self._parse_line(line, line_num, parent_stack)
                nodes.append(node)

        return nodes

    def _parse_line(self, line: str, line_num: int, parent_stack: list) -> Node:
        """解析单行内容"""
        match = self._line_regex.match(line)
        if not match:
            raise ValueError(f"格式错误（第{line_num}行）: {line}")

        indent, prefix, name, level_name, describe = match.groups()
        depth = self._calc_depth(indent, line_num)
        node_type = self._determine_node_type(prefix, line_num)

        self._validate_hierarchy(depth, parent_stack, line_num)

        if node_type == "field":
            return self._create_field(name, parent_stack)
        elif node_type == "aspect":
            return self._create_aspect(name, depth, parent_stack, line_num)
        else:
            return self._create_skill(
                name, level_name, describe, parent_stack, line_num
            )

    def _calc_depth(self, indent: str, line_num: int) -> int:
        """计算缩进层级"""
        if len(indent) % self._indent_unit != 0:
            raise ValueError(f"非常规缩进（第{line_num}行）")
        return len(indent) // self._indent_unit

    def _determine_node_type(self, prefix: str, line_num: int) -> str:
        """判断节点类型"""
        if '+' in prefix:
            if not prefix.endswith('+'):
                raise ValueError(f"无效的技能前缀（第{line_num}行）")
            return "skill"
        return "aspect" if prefix else "field"

    def _validate_hierarchy(self, depth: int, parent_stack: list, line_num: int):
        """验证层级关系"""
        if depth == 0 and parent_stack:
            raise ValueError(f"根节点重复定义（第{line_num}行）")
        if depth > len(parent_stack):
            raise ValueError(f"层级跳跃错误（第{line_num}行）")

    def _create_field(self, name: str, parent_stack: list) -> 'Field':
        """创建领域节点"""
        field = Field(name)
        parent_stack.clear()
        parent_stack.append(field)
        return field

    def _create_aspect(self, name: str, depth: int,
                       parent_stack: list, line_num: int) -> 'Aspect':
        """创建分支节点"""
        parent = parent_stack[depth - 1]
        if depth == 1 and not isinstance(parent, Field):
            raise TypeError(f"一级分支必须属于领域（第{line_num}行）")

        aspect = Aspect(name, parent)
        parent_stack.append(aspect)
        return aspect

    def _create_skill(self, name: str, level_name: str, describe: str,
                      parent_stack: list, line_num: int) -> 'Skill':
        """创建技能节点"""
        parent = parent_stack[-1]
        if not isinstance(parent, Aspect):
            raise TypeError(f"技能必须属于分支（第{line_num}行）")

        try:
            level = self.levels[level_name or "基础"]
        except KeyError:
            raise ValueError(f"未定义的等级: {level_name}（第{line_num}行）")

        return Skill(
            name=name,
            parent=parent,
            skill_level=level,
            describe=describe
        )
