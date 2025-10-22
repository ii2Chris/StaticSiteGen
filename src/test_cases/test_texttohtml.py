import unittest

from functions.text_to_html import text_node_to_html_node
from functions.textnode import TextNode, TextType

class TestTextToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_underline(self):
        node = TextNode("Underline text", TextType.UNDERLINE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "u")
        self.assertEqual(html_node.value, "Underline text")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_strikethrough(self):
        node = TextNode("Strikethrough text", TextType.STRIKETHROUGH)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "s")
        self.assertEqual(html_node.value, "Strikethrough text")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_code(self):
        node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_link(self):
        node = TextNode("Link text", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_image(self):
        node = TextNode("Image alt text", TextType.IMAGE, url="http://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "http://example.com/image.jpg", "alt": "Image alt text"})
        self.assertEqual(html_node.value, "")

    def test_unsupported_text_raises(self):
        class FakeType:
            pass
        fake = FakeType()
        node = TextNode("Unsupported", fake)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_invalid_input(self):

        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
