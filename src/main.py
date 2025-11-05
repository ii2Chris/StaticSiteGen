import os
from functions.copy_static import copy_dir, prepare_public
from functions.sitegen import generate_page, generate_pages_recursive

def main():
    static_path = "static"
    public_path = "public"
    content_md = "content/index.md"
    template_path = "template.html"

    prepare_public(public_path)
    copy_dir(static_path, public_path)

    dest_html = os.path.join(public_path, "index.html")
    generate_page(content_md, template_path, dest_html)

if __name__ == "__main__":
    main()
