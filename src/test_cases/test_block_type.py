import unittest

from functions.block_type import BlockType
from functions.block_to_block_type import block_to_block_type

class TestBlockType(unittest.TestCase):
    def test_block_type_values(self):
        self.assertEqual(BlockType.PARAGRAPH.value, "paragraph")
        self.assertEqual(BlockType.HEADING.value, "heading")
        self.assertEqual(BlockType.CODE.value, "code")
        self.assertEqual(BlockType.QUOTE.value, "quote")
        self.assertEqual(BlockType.UNORDERED_LIST.value, "unordered_list")
        self.assertEqual(BlockType.ORDERED_LIST.value, "ordered_list")

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```code block```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("Regular paragraph text."), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
