import os
from pathlib import Path
from typing import Optional


class Markdown:
    """
    A class to generate Markdown files with specified title and content.
    Handles directory creation and file extension validation.
    """

    def __init__(self, file_name: str, title: str, content: str):
        """
        Initialize the Markdown generator.

        :param file_name: Output filename (with or without .md extension)
        :param title: Document title (will be rendered as # Heading)
        :param content: Main content body
        """
        self.file_path = Path(file_name).with_suffix(".md")
        self.title = title.strip()
        self.content = content.strip()

    def generate(self) -> None:
        """
        Generate the Markdown file with proper directory structure.
        Raises OSError if file cannot be written.
        """
        try:
            # Create parent directories if needed
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Compose full content
            full_content = f"# {self.title}\n\n{self.content}"

            # Write to file
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(full_content)

            print(f"Successfully generated: {self.file_path.resolve()}")

        except (OSError, IOError) as e:
            raise RuntimeError(f"Failed to generate Markdown file: {str(e)}") from e


if __name__ == "__main__":
    # Example usage
    test_file = "../../test/example"
    test_title = "My Markdown Example"
    test_content = """\
    ## Section 1
    Here is some content in section 1.

    ## Section 2
    Here is some more content in section 2.

    - Bullet Point 1
    - Bullet Point 2
    """

    try:
        md = Markdown(test_file, test_title, test_content)
        md.generate()
    except RuntimeError as e:
        print(f"Error: {str(e)}")