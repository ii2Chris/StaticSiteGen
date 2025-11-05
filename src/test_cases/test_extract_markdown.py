import unittest
from functions.extract_markdown import extract_markdown, extract_title

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_empty_input(self):
        with self.assertRaises(Exception) as context:
            extract_markdown("")
        self.assertEqual(str(context.exception), "Input text is empty")

    def test_extract_title_none_input(self):
        with self.assertRaises(ValueError) as context:
            extract_title(None)
        self.assertEqual(str(context.exception), "Input markdown is None")

    def test_extract_title_no_h1(self):
        markdown = "## This is a subtitle\nSome content here."
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 header found in markdown")

    def test_extract_title_valid_h1(self):
        markdown = "# This is the Title\nSome content here."
        title = extract_title(markdown)
        self.assertEqual(title, "This is the Title")

    def test_extract_title_h1_with_whitespace(self):
        markdown = "   #    Title with spaces    \nContent."
        title = extract_title(markdown)
        self.assertEqual(title, "Title with spaces")

    def test_extract_title_h1_empty(self):
        markdown = "#   \nContent."
        title = extract_title(markdown)
        self.assertEqual(title, "")

if __name__ == '__main__':
    unittest.main()
