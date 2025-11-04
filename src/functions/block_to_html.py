from .block_type import BlockType
from .block_to_block_type import block_to_block_type
from .html_node import LeafNode, ParentNode
from .markdown_to_blocks import markdown_to_blocks
from .text_to_textnode import text_node_to_text_node
from .text_to_html import text_node_to_html_node


def _text_to_children(text):
    """Convert inline markdown text into a list of HTML child nodes.

    Uses the project's TextNode pipeline, then maps to HTML leaf nodes.
    """
    text_nodes = text_node_to_text_node(text)
    return [text_node_to_html_node(n) for n in text_nodes]


def _strip_leading(line: str, prefix: str) -> str:
    if line.startswith(prefix):
        return line[len(prefix) :]
    return line


def markdown_to_html_node(markdown):
    """Convert a full markdown document into a single parent HTML node.

    - Splits markdown into logical blocks
    - Determines block type for each
    - Builds appropriate HTML nodes with inline parsing (except code blocks)
    - Returns a ParentNode('div', children)
    """
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.CODE:
            # Expect triple backticks fenced block. Keep content verbatim, no inline parsing.
            lines = block.split("\n")
            if (
                len(lines) >= 2
                and lines[0].startswith("```")
                and lines[-1].startswith("```")
            ):
                inner = "\n".join(lines[1:-1])
            else:
                # Fallback: treat whole block as code
                inner = block
            # Ensure trailing newline to match expected rendering in tests
            if not inner.endswith("\n"):
                inner = inner + "\n"
            code_leaf = LeafNode("code", inner)
            children.append(ParentNode("pre", [code_leaf]))
            continue

        if btype == BlockType.HEADING:
            # Count leading # to get level (cap at 6)
            line = block.split("\n")[0]
            hashes = 0
            for ch in line:
                if ch == "#":
                    hashes += 1
                else:
                    break
            level = max(1, min(6, hashes))
            # Remove leading #'s and one optional space
            text = line[level:]
            if text.startswith(" "):
                text = text[1:]
            tag = f"h{level}"
            children.append(ParentNode(tag, _text_to_children(text)))
            continue

        if btype == BlockType.QUOTE:
            # Remove leading '> ' (or just '>') from each line, then inline-parse, joined as space
            lines = block.split("\n")
            stripped = []
            for ln in lines:
                ln = _strip_leading(ln, "> ")
                ln = _strip_leading(ln, ">")
                stripped.append(ln)
            text = " ".join([s for s in stripped if s != ""])  # flatten to one line
            children.append(ParentNode("blockquote", _text_to_children(text)))
            continue

        if btype in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
            lines = block.split("\n")
            li_nodes = []
            if btype == BlockType.UNORDERED_LIST:
                for ln in lines:
                    # handle both '- ' and '* '
                    if ln.startswith("- "):
                        item = ln[2:]
                    elif ln.startswith("* "):
                        item = ln[2:]
                    else:
                        item = ln
                    li_nodes.append(ParentNode("li", _text_to_children(item)))
                children.append(ParentNode("ul", li_nodes))
            else:
                # ordered: strip leading digits, dot, space
                for ln in lines:
                    # Find first occurrence of pattern: digits + '. '
                    i = 0
                    while i < len(ln) and ln[i].isdigit():
                        i += 1
                    if i < len(ln) and i > 0 and ln[i : i + 2] == ". ":
                        item = ln[i + 2 :]
                    else:
                        item = ln
                    li_nodes.append(ParentNode("li", _text_to_children(item)))
                children.append(ParentNode("ol", li_nodes))
            continue

        # Default: paragraph — collapse internal newlines into spaces
        if btype == BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            children.append(ParentNode("p", _text_to_children(text)))
            continue

        # Fallback safety (should not hit with current enum)
        children.append(ParentNode("p", _text_to_children(block)))

    return ParentNode("div", children)
