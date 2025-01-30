from .node import Root, Twig, Leaf, Node
from .level import Level
from typing import Optional, Union


class Field(Root):
    """领域/根节点"""

    def __init__(self, name: str):
        super().__init__(name)
        self._validate_name(name)

    def _validate_name(self, name: str):
        if not name.strip():
            raise ValueError("领域名称不能为空")


class Aspect(Twig):
    """技能分支节点"""
    def __init__(self, name: str, parent: Union[Field, 'Aspect']):
        if not isinstance(parent, (Field, Aspect)):
            raise TypeError("分支节点的父节点必须是领域或其他分支")
        super().__init__(name, parent)


class Skill(Leaf):
    """技能叶节点"""

    def __init__(self,
                 name: str,
                 parent: Aspect,
                 skill_level: Level,
                 describe: Optional[str] = None):
        if not isinstance(parent, Aspect):
            raise TypeError("技能节点必须属于分支节点")

        super().__init__(name, parent)
        self.skill_level = skill_level
        self.describe = describe or skill_level.describe

    @property
    def level_color(self) -> str:
        return self.skill_level.color