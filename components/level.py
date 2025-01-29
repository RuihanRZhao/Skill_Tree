class Level:
    def __init__(self, level_name: str = "", color: str = "", describe: str = ""):
        self.name = level_name
        self.color = color
        self.describe = describe

        print(self)

    def __str__(self):
        return (
            f"[Level: {self.name}, Color: {self.color}, Describe: {self.describe}]"
        )

    def __eq__(self, other):
        if isinstance(other, Level):
            if self.name != other.name:
                # print(f"Name different!")
                return False
            if self.color != other.color:
                # print(f"Color different!")
                return False
            if self.describe != other.describe:
                # print(f"Describe different!")
                return False

            return True

        return False

    def generate_text(self) -> str:
        output = (
            f"<abbr title=\"{self.describe}\"><font color=\"{self.color}\">{self.name}</font></abbr>"
        )

        return output


if __name__ == "__main__":
    test_obj = Level("test", "red", "test descriptions")

    from markdown_edit import Markdown

    file_name = "../test/example"
    title = "Test 4 Level"
    content = test_obj.generate_text()

    generator = Markdown(file_name, title, content)
    generator.generate()
