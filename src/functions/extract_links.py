import re

def extract_markdown_images(text):
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_links(text):
    return extract_markdown_images(text)
