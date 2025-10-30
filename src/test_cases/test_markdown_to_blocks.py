import unittest

from functions.markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items

            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_trims_and_ignores_leading_trailing_blank_blocks(self):
        md = """


            First paragraph with leading/trailing spaces


            Second paragraph


            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph with leading/trailing spaces",
                "Second paragraph",
            ],
        )

    def test_windows_line_endings(self):
        md = "Line A\r\n\r\n- item1\r\n- item2\r\n\r\nTail\r\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Line A",
                "- item1\n- item2",
                "Tail",
            ],
        )

    def test_multiple_blank_separators(self):
        md = """
            Para 1



            Para 2



            - a
            - b
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Para 1",
                "Para 2",
                "- a\n- b",
            ],
        )

    def test_single_block_no_double_newline(self):
        md = "  Single block with spaces and\ninternal new line  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Single block with spaces and\ninternal new line",
            ],
        )

    def test_spaces_only_lines_within_block_are_removed(self):
        # After initial split, intra-block lines that are spaces should be dropped
        md = """
            Para with

            spaces-only line kept out
            """
        blocks = markdown_to_blocks(md)
        # A blank line (even with spaces) separates blocks
        self.assertEqual(
            blocks,
            [
                "Para with",
                "spaces-only line kept out",
            ],
        )

    def test_tabs_and_spaces_indentation(self):
        md = "\t\t- tabbed\n    - spaced"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- tabbed\n- spaced",
            ],
        )

    def test_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_blank_lines(self):
        self.assertEqual(markdown_to_blocks("\n\n  \n\n"), [])


if __name__ == "__main__":
    unittest.main()
