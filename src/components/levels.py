from .level import Level

levels = [
    ("基础", "grey", "对某种语言或框架有初步了解，能进行简单的编码或操作。"),
    ("了解", "blue", "对其特性和用法有一定认识，能够完成一些基础项目。"),
    ("熟练", "green", "能够独立完成中等复杂度的项目，熟悉其主要特性和最佳实践。"),
    ("高级", "yellow", "在该语言或框架上有较深的理解，能够优化代码和解决复杂问题。"),
    ("精通", "red", "能够深入理解和应用其底层原理，参与框架的设计或贡献开源。"),
    ("专家", "black", "在该领域具有广泛的影响力，能够进行教学或指导他人，解决行业内的复杂挑战。"),
]


class Levels:
    def __init__(self, level_list: list[Level] = None):
        self.list = level_list if level_list is not None else []

    def add_level(self, target: tuple):
        new_level = Level(target[0], target[1], target[2])
        if_exist = False
        if self.list:
            for i in self.list:
                if new_level == i:
                    if_exist = True
                    print(f"{target} is existed already.")
                    break

        if not if_exist:
            self.list.append(new_level)
            print(f"{self.list[len(self.list)-1]} created.")

    def add_levels_via_list(self, target_list:list[tuple]):
        for i in target_list:
            self.add_level(i)

    def search_by_name(self, _name):
        for i in self.list:
            if i.name == _name:
                return i

        raise KeyError(f"Level with Name [{_name}] not found.")

    def print_all_levels(self):
        output = ""
        for i in self.list:
            output += f"-{i.generate_markdown()}: {i.describe}\n"

        return output


if __name__ == "__main__":
    test_levels = Levels()
    test_levels.add_levels_via_list(levels)

    from components.markdown_edit import Markdown

    file_name = "../test/example"
    title = "Test 4 Level"
    content = test_levels.print_all_levels()

    generator = Markdown(file_name, title, content)
    generator.generate()
