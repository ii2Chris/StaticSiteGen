from functions.htmlnode import HTMLNode, LeafNode, ParentNode
from functions.textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise Exception("Input must be a TextNode instance")

    # Basic mapping from TextNode to HTMLNode
    if text_node.text_type == TextType.PLAIN: return LeafNode(None, text_node.text)

    if text_node.text_type == TextType.BOLD: return LeafNode("b", text_node.text)

    if text_node.text_type == TextType.ITALIC: return LeafNode("i", text_node.text)

    if text_node.text_type == TextType.CODE: return LeafNode("code", text_node.text)

    if text_node.text_type == TextType.STRIKETHROUGH: return LeafNode("s", text_node.text)

    if text_node.text_type == TextType.UNDERLINE: return LeafNode("u", text_node.text)

    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url} if text_node.url else None)

    if text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("IMAGE TextNode requires a url")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    # If we reach here, the TextType is unsupported
    raise ValueError(f"Unsupported TextType: {text_node.text_type}")
