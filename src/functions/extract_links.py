import re

def extract_markdown_images(text):
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_links(text):
    pattern = r"\[([^\[\]]*)\]\(([^()]+)\)"
    return re.findall(pattern, text)
