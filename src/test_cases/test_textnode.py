import unittest

from functions.textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    # I thank gpt-4 for the following test cases even though I should've written them myself teehee
    def test_neq_different_text(self):
        # Different text should make nodes unequal
        n1 = TextNode("First", TextType.PLAIN)
        n2 = TextNode("Second", TextType.PLAIN)
        self.assertNotEqual(n1, n2)

    def test_neq_different_text_type(self):
        # Same text but different text_type should be unequal
        n1 = TextNode("Same text", TextType.PLAIN)
        n2 = TextNode("Same text", TextType.BOLD)
        self.assertNotEqual(n1, n2)

    def test_url_none_vs_value(self):
        # url None vs a concrete value should be unequal
        n1 = TextNode("Link text", TextType.LINK, url=None)
        n2 = TextNode("Link text", TextType.LINK, url="http://example.com")
        self.assertNotEqual(n1, n2)

        # when both urls are None they should be equal
        n3 = TextNode("Link text", TextType.LINK)
        n4 = TextNode("Link text", TextType.LINK, url=None)
        self.assertEqual(n3, n4)

    def test_compare_with_non_textnode(self):
        # Comparing with a non-TextNode should return False (not equal)
        n = TextNode("X", TextType.PLAIN)
        self.assertNotEqual(n, "not a node")


if __name__ == "__main__":
    unittest.main()
