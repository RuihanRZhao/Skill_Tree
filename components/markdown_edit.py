import os


class Markdown:
    """
    A class to generate Markdown files with specified title and content.
    """

    def __init__(self, file_name, title, content):
        """
        Initialize the MarkdownGenerator with file name, title, and content.

        :param file_name: Name of the Markdown file to create (e.g., "output.md")
        :param title: The title of the Markdown file
        :param content: The content of the Markdown file
        """
        self.file_name = file_name if file_name.endswith(".md") else file_name + ".md"
        self.title = title
        self.content = content

    def generate(self):
        """
        Generates the Markdown file.
        """
        markdown_content = f"# {self.title}\n" \
                           f"{self.content}"

        # Write the content to the file
        with open(self.file_name, "w", encoding="utf-8") as file:
            file.write(markdown_content)

        print(f"Markdown file '{self.file_name}' has been created successfully.")


if __name__ == "__main__":
    file_name = "../test/example"
    title = "My Markdown Example"
    content = (
        "This is a sample Markdown file generated using a Python script.\n\n"
        "## Section 1\n"
        "Here is some content in section 1.\n\n"
        "## Section 2\n"
        "Here is some more content in section 2.\n\n"
        "- Bullet Point 1\n"
        "- Bullet Point 2\n"
    )

    # Create an instance of MarkdownGenerator and generate the file
    generator = Markdown(file_name, title, content)
    generator.generate()
