from .extract_markdown import extract_title
from .block_to_html import markdown_to_html_node
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} using template {template_path} into {dest_path}")

    # read the content and template files
    with open(from_path, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    # render HTML + extract title
    node = markdown_to_html_node(content)
    html = node.to_html()
    title = extract_title(content)

    # apply template
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:  # only create if not empty
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages recursively from {dir_path_content} using template {template_path} into {dest_dir_path}")
