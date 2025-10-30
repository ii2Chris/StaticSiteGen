from .text_node import TextNode, TextType
from .split_node_delimiter import split_nodes_delimiter
from .split_node_extract import split_nodes_image, split_nodes_link


def text_node_to_text_node(text):
    new_node = [TextNode(text, TextType.TEXT)]

    new_node = split_nodes_image(new_node)
    new_node = split_nodes_link(new_node)
    new_node = split_nodes_delimiter(new_node, "`", TextType.CODE)
    new_node = split_nodes_delimiter(new_node, "**", TextType.BOLD)
    new_node = split_nodes_delimiter(new_node, "_", TextType.ITALIC)

    return new_node
