from .text_node import TextNode, TextType
from .extract_links import extract_links, extract_markdown_images


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        s = node.text
        matches = extract_markdown_images(s)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        for match in matches:
            sections = s.split(f"![{match[0]}]({match[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed properly.")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            s = sections[1]
        if s != "":
            new_nodes.append(TextNode(s, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        s = node.text
        matches = extract_links(s)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        for match in matches:
            sections = s.split(f"[{match[0]}]({match[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed properly.")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            s = sections[1]
        if s != "":
            new_nodes.append(TextNode(s, TextType.TEXT))

    return new_nodes
