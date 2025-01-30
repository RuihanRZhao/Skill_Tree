class Level:
    def __init__(self, level_name: str = "", color: str = "", describe: str = ""):
        self.name = level_name
        self.color = color
        self.describe = describe

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

    def generate_markdown(self) -> str:
        output = (
            f"<abbr title=\"{self.describe}\"><font color=\"{self.color}\">{self.name}</font></abbr>"
        )
        return output
