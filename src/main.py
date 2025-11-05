from functions.copy_static import copy_dir, prepare_public
from functions.sitegen import generate_pages_recursive

def main():
    static_path = "static"
    public_path = "public"
    content_dir = "content"
    template = "template.html"

    prepare_public(public_path)
    copy_dir(static_path, public_path)
    generate_pages_recursive(content_dir, template, public_path)

if __name__ == "__main__":
    main()
