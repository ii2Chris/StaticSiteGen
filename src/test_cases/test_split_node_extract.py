import unittest

from functions.split_node_extract import split_nodes_image, split_nodes_link
from functions.text_node import TextNode, TextType


class TestNodeExtract(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_single_image_at_start_and_end(self):
        node = TextNode("![a](u1) middle ![b](u2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "u1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "u2"),
            ],
            new_nodes,
        )

    def test_image_adjacent(self):
        node = TextNode("start ![i1](u1)![i2](u2) end", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start ", TextType.TEXT),
                TextNode("i1", TextType.IMAGE, "u1"),
                TextNode("i2", TextType.IMAGE, "u2"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_empty_alt(self):
        node = TextNode("before ![](http://img) after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "http://img"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_images_returns_same_node(self):
        node = TextNode("no images here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_basic(self):
        node = TextNode("click [here](http://x) now", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "http://x"),
                TextNode(" now", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_adjacent(self):
        node = TextNode("a [one](u1)[two](u2) b", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("one", TextType.LINK, "u1"),
                TextNode("two", TextType.LINK, "u2"),
                TextNode(" b", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_non_text_nodes_ignored(self):
        image_node = TextNode("img", TextType.IMAGE, url="u")
        text_node = TextNode("before [x](u2) after", TextType.TEXT)
        new_nodes = split_nodes_link([image_node, text_node])
        self.assertListEqual(
            [
                image_node,
                TextNode("before ", TextType.TEXT),
                TextNode("x", TextType.LINK, "u2"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_chain_image_then_link(self):
        node = TextNode("a ![i](iu) and [l](lu) end", TextType.TEXT)
        # apply image splitter first, then link splitter to remaining text nodes
        after_images = split_nodes_image([node])
        # apply link splitter to the result
        final = split_nodes_link(after_images)
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("i", TextType.IMAGE, "iu"),
                TextNode(" and ", TextType.TEXT),
                TextNode("l", TextType.LINK, "lu"),
                TextNode(" end", TextType.TEXT),
            ],
            final,
        )


if __name__ == "__main__":
    unittest.main()
