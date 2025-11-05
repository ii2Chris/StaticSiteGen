from functions.copy_static import copy_dir, prepare_public
from functions.sitegen import generate_page

def main():
    static_path = "static"
    public_path = "public"
    content_md = "content/index.md"
    template_path = "templates/index.html"

    prepare_public(public_path)
    copy_dir(static_path, public_path)
    generate_page(content_md, template_path, public_path)

if __name__ == "__main__":
    main()
