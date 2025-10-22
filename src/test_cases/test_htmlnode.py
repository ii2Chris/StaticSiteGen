import unittest

from functions.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    # Testing HTMLNode class
    def test_ToHtml(self):
        testNode = HTMLNode(tag="div", value="X", props={"class": "container"})
        with self.assertRaises(NotImplementedError):
            testNode.to_html()

    def test_propsToHtml_no_props(self):
        testNode = HTMLNode(tag="div", value="X")
        self.assertEqual(testNode.props_to_html(), "")

    def test_propsToHtml_with_props(self):
        testNode = HTMLNode(tag="div", value="X", props={"class": "container"})
        self.assertEqual(testNode.props_to_html(), 'class="container"')

    def test_repr(self):
        testNode = HTMLNode(tag="div", value="X", props={"class": "container"})
        self.assertEqual(
            repr(testNode),
            'HTMLNode (div, X, None, {\'class\': \'container\'})'
        )

class testLeafNode(unittest.TestCase):
    # Testing LeafNode Class
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        testNode = LeafNode("a", "The goat, Lebonbon")
        self.assertEqual(testNode.to_html(), "<a>The goat, Lebonbon</a>")

class testParentNode(unittest.TestCase):
    # Testing ParentNode Class
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_renders_nested(self):
        node = ParentNode("p", [LeafNode("b", "B"), LeafNode(None, "x")])
        self.assertEqual(node.to_html(), "<p><b>B</b>x</p>")

    def test_empty_children_list_ok(self):
        node = ParentNode("div", [], {"id": "root"})
        self.assertEqual(node.to_html(), '<div id="root"></div>')

    def test_missing_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [])

    def test_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("section", None)

    def test_deeply_nested(self):
        inner = ParentNode("span", [LeafNode(None, "hi")])
        outer = ParentNode("div", [inner])
        self.assertEqual(outer.to_html(), "<div><span>hi</span></div>")

if __name__ == "__main__":
    unittest.main()
