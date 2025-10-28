from platform import node
import unittest

from functions.text_node import TextNode, TextType
from functions.split_node_delimiter import split_nodes_delimiter

BASE = getattr(TextType, "PLAIN", None) or getattr(TextType, "TEXT", None)

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_code_simple(self):
        node = TextNode("This has a `code` word", BASE)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("This has a ", BASE), ("code", TextType.CODE), (" word", BASE)],
        )

    def test_bold_double_asterisks(self):
        node = TextNode("A **bolded phrase** here", BASE)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("A ", BASE), ("bolded phrase", TextType.BOLD), (" here", BASE)],
        )

    def test_italic_underscore(self):
        node = TextNode("Start _mid_ end", BASE)
        out = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("Start ", BASE), ("mid", TextType.ITALIC), (" end", BASE)],
        )

    def test_multiple_occurrences(self):
        node = TextNode("a **b** c **d** e", BASE)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("a ", BASE), ("b", TextType.BOLD), (" c ", BASE), ("d", TextType.BOLD), (" e", BASE)],
        )

    def test_non_text_nodes_ignored(self):
        non_text = TextNode("Already bold", TextType.BOLD)
        out = split_nodes_delimiter([non_text], "**", TextType.BOLD)
        # unchanged
        self.assertEqual(len(out), 1)
        self.assertIs(out[0], non_text)

    def test_no_delimiter_in_text(self):
        node = TextNode("nothing special here", BASE)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].text, "nothing special here")
        self.assertEqual(out[0].text_type, BASE)

    def test_unbalanced_raises(self):
        node = TextNode("oops **unbalanced", BASE)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_skips_empties(self):
        node = TextNode("x `` y", BASE)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("x ", BASE), ("", TextType.CODE), (" y", BASE)],  # Note: empty code segment stays if between two backticks
        )

if __name__ == "__main__":
    unittest.main()
