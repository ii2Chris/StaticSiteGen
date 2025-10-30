import re

from .block_type import BlockType

def block_to_block_type(block):
     # Assume leading/trailing whitespace already stripped
    if not block:
        return BlockType.PARAGRAPH

    if block.startswith("#"):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        return BlockType.QUOTE

    if block.startswith("- ") or block.startswith("* "):
        return BlockType.UNORDERED_LIST

    # if first non-space characters are digits followed by a dot and space
    if re.match(r"^\d+\. ", block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
