import sys

from functions.copy_static import copy_dir, prepare_public
from functions.sitegen import generate_pages_recursive

def _normalize_basepath(path: str) -> str:
    if not path: return "/"
    if not path.startswith("/"):
        path = "/" + path
    if not path.endswith("/"):
        path = path + "/"
    return path


def main():
    static_path = "static"
    public_path = "docs"
    content_dir = "content"
    template = "template.html"

    basepath = _normalize_basepath(sys.argv[1]) if len(sys.argv) > 1 else "/"

    prepare_public(public_path)
    copy_dir(static_path, public_path)
    generate_pages_recursive(content_dir, template, public_path, basepath=basepath)

if __name__ == "__main__":
    main()
