from .extract_markdown import extract_title
from .block_to_html import markdown_to_html_node
import os

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str = "/") -> None:
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

    # Apply basepath
    # optional GitHub Pages-friendly basepath handling (safe no-op if '/')
    if basepath != "/":
        page = page.replace('href="/', f'href="{basepath}')
        page = page.replace('src="/',  f'src="{basepath}')

    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:  # only create if not empty
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath="/") -> None:
    print(f"Generating pages recursively from {dir_path_content} using template {template_path} into {dest_dir_path}")

    if not os.path.isdir(dir_path_content):
        raise NotADirectoryError(f"Error: {dir_path_content} is not a directory")

    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)
        dst_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(src_path):
            # ensure mirror directory exists in dest, then recurse
            os.makedirs(dst_path, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dst_path, basepath)
            continue

        if not entry.lower().endswith(".md"):
            # skip non-markdown files in content
            continue

        # map *.md → *.html (index.md → index.html)
        if entry.lower() == "index.md":
            out_path = os.path.join(dest_dir_path, "index.html")
        else:
            name, _ = os.path.splitext(entry)
            out_path = os.path.join(dest_dir_path, f"{name}.html")

        generate_page(src_path, template_path, out_path, basepath)
