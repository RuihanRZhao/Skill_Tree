import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from markdown_edit import Markdown

SAMPLE_TITLE = "Test Document"
SAMPLE_CONTENT = "## Test Section\nSample content"


def test_file_extension_handling():
    """测试自动添加.md扩展名"""
    with TemporaryDirectory() as tmpdir:
        # 测试无扩展名
        md = Markdown(Path(tmpdir) / "test", SAMPLE_TITLE, SAMPLE_CONTENT)
        assert md.file_path.suffix == ".md"

        # 测试已有扩展名
        md = Markdown(Path(tmpdir) / "test.txt", SAMPLE_TITLE, SAMPLE_CONTENT)
        assert md.file_path.suffix == ".md"


def test_directory_creation():
    """测试自动创建目录"""
    with TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "new_dir/sub_dir/document"
        Markdown(target, SAMPLE_TITLE, SAMPLE_CONTENT).generate()
        assert target.with_suffix(".md").exists()


def test_content_generation():
    """测试内容生成正确性"""
    with TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "test.md"
        expected = f"# {SAMPLE_TITLE}\n\n{SAMPLE_CONTENT}"

        Markdown(target, SAMPLE_TITLE, SAMPLE_CONTENT).generate()

        with open(target, "r", encoding="utf-8") as f:
            assert f.read() == expected


def test_error_handling():
    """测试异常处理"""
    with TemporaryDirectory() as tmpdir:
        # 创建只读目录
        read_only_dir = Path(tmpdir) / "readonly"
        read_only_dir.mkdir()
        read_only_dir.chmod(0o444)

        target = read_only_dir / "test.md"

        with pytest.raises(RuntimeError):
            Markdown(target, SAMPLE_TITLE, SAMPLE_CONTENT).generate()