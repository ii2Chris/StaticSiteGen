import unittest

from functions.text_to_textnode import text_node_to_text_node
from functions.text_node import TextNode, TextType


class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_node_to_text_node(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_plain_text_only(self):
        text = "Just plain text"
        result = text_node_to_text_node(text)
        self.assertEqual(result, [TextNode("Just plain text", TextType.TEXT)])

    def test_only_image(self):
        text = "![alt](http://img)"
        result = text_node_to_text_node(text)
        self.assertEqual(result, [TextNode("alt", TextType.IMAGE, "http://img")])

    def test_only_link(self):
        text = "[name](http://x)"
        result = text_node_to_text_node(text)
        self.assertEqual(result, [TextNode("name", TextType.LINK, "http://x")])

    def test_adjacent_images(self):
        text = "![a](u1)![b](u2)"
        result = text_node_to_text_node(text)
        self.assertEqual(
            result,
            [TextNode("a", TextType.IMAGE, "u1"), TextNode("b", TextType.IMAGE, "u2")],
        )

    def test_code_contains_bold_markers(self):
        text = "before `**bold**` after"
        result = text_node_to_text_node(text)
        self.assertEqual(
            result,
            [
                TextNode("before ", TextType.TEXT),
                TextNode("**bold**", TextType.CODE),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_bold_italic_code_combination(self):
        text = "A **bold** _italic_ and `code` together"
        result = text_node_to_text_node(text)
        self.assertEqual(
            result,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" together", TextType.TEXT),
            ],
        )

    def test_link_and_italic(self):
        text = "See [docs](http://d) _now_"
        result = text_node_to_text_node(text)
        self.assertEqual(
            result,
            [
                TextNode("See ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "http://d"),
                TextNode(" ", TextType.TEXT),
                TextNode("now", TextType.ITALIC),
            ],
        )

    def test_unbalanced_bold_raises(self):
        text = "This has **unbalanced bold*"
        with self.assertRaises(ValueError):
            text_node_to_text_node(text)

    def test_unbalanced_italic_raises(self):
        text = "This has _unbalanced italic"
        with self.assertRaises(ValueError):
            text_node_to_text_node(text)

    def test_unbalanced_code_raises(self):
        text = "This has `unbalanced code"
        with self.assertRaises(ValueError):
            text_node_to_text_node(text)


if __name__ == "__main__":
    unittest.main()
