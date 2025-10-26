from functions.textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    BASE = TextType.PLAIN

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        s = node.text
        if delimiter not in s:
            new_nodes.append(node)
            continue

        if s.count(delimiter) % 2 != 0:
            raise ValueError(f"Unbalanced delimiter: {delimiter}")

        parts = s.split(delimiter)
        last = len(parts) - 1

        for i, part in enumerate(parts):
            if i % 2 == 0:
                # even: plain text
                # skip empty at boundaries (leading/trailing delimiter)
                if part == "" and (i == 0 or i == last):
                    continue
                if part != "":
                    new_nodes.append(TextNode(part, BASE))
            else:
                # odd: target type — allow empty (adjacent delimiters)
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
