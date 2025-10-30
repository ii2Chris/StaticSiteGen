import re

def markdown_to_blocks(markdown):
    # Normalize newlines to \n to handle Windows (\r\n) and old Mac (\r)
    normalized = markdown.replace("\r\n", "\n").replace("\r", "\n")

    # Split on one or more blank-line separators, allowing whitespace-only lines
    raw_blocks = re.split(r"\n\s*\n+", normalized)

    blocks = []
    for block in raw_blocks:
        if block.strip() == "":
            continue

        lines = block.splitlines()
        stripped_lines = [line.strip() for line in lines if line.strip()]
        cleaned_block = "\n".join(stripped_lines)
        blocks.append(cleaned_block)

    return blocks
