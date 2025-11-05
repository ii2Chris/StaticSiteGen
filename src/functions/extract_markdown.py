import re

def extract_markdown(text: str) -> str:
    if not text:
        raise Exception("Input text is empty")
    return text

def extract_title(markdown: str) -> str:
    if markdown is None:
        raise ValueError("Input markdown is None")

    # Look for a line that starts with a single '#' (not '##' or more)
    for raw_line in markdown.splitlines():
        line = raw_line.lstrip()
        m = re.match(r"^#(?!#)\s*(.*\S.*|)\s*$", line)
        if m:
            title = m.group(1) or ""
            return title.strip()

    raise ValueError("No H1 header found in markdown")
