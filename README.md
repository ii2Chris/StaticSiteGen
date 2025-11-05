# StaticSiteGen

StaticSiteGen is a small, dependency-free static site generator written in Python.
It converts a simple markdown content tree into a static website in the `docs/`
folder and is intended to be published (for example) with GitHub Pages.

Live demo (deployed via GitHub Pages):

    https://ii2chris.github.io/StaticSiteGen/

## Features

- Convert a directory tree of Markdown files under `content/` into HTML pages
- Uses a simple HTML template (`template.html`) and injects generated HTML
- Copies static assets from `static/` into the output `docs/` directory
- Supports basic markdown blocks, headings, lists, quotes, code fences, links, and images
- GitHub Pages friendly: supports an optional base path when generating pages

## Quick start

Requirements: Python 3.x (3.8+ recommended)

1. Clone the repo.
2. Edit or add markdown files under `content/`. Each `index.md` becomes an `index.html` in the corresponding output folder.
3. Run the generator:

```bash
# Use this when you want generated paths to use a non-root base (useful for GitHub Pages)
python3 src/main.py "/REPO_NAME_HERE/"

# or just generate with default basepath '/'
python3 src/main.py
```

4. The generated website will be in `docs/` — you can serve it locally from that folder.

```bash
cd docs && python3 -m http.server 8888
```

There are convenience scripts in the repo:

- `build.sh` — runs the generator (uses the project `src/main.py` helper).
- `main.sh` — an example script to generate and then serve the site locally (localhost:8888).
- `test.sh` — runs the unit tests for the text/markdown pipeline.

## Project layout

- `content/` — source markdown files arranged in directories (mirrors to `docs/`).
- `template.html` — HTML template. Contains `{{ Title }}` and `{{ Content }}` placeholders.
- `static/` — static assets (CSS, images, etc.) copied into `docs/` verbatim.
- `docs/` — generated site (output). This folder is removed and recreated on each build.
- `src/` — Python implementation. Key modules:
  - `src/main.py` — CLI entry: prepares `docs/`, copies static files, invokes page generation.
  - `src/functions/sitegen.py` — core generation: reads markdown, converts to HTML, applies template, writes files. Supports an optional `basepath` replacement for GitHub Pages.
  - `src/functions/markdown_to_blocks.py` — splits raw markdown into logical blocks.
  - `src/functions/block_to_html.py` — maps blocks to HTML nodes and composes the final HTML node tree.
  - `src/functions/text_to_html.py` — converts inline TextNode objects into HTML nodes (bold, italics, links, images, code, etc.).
  - `src/functions/copy_static.py` — copies static assets into `docs/` and handles `docs/` directory recreation.
  - `src/functions/extract_markdown.py` — helpers to extract titles (H1) from markdown.
  - `src/test_cases/` — unit tests for the parsing/rendering pipeline.

## How it works (high level)

1. `src/main.py` normalizes an optional `basepath` and prepares the output directory (`docs/`).
2. Static assets under `static/` are copied to `docs/`.
3. The generator walks `content/` recursively. For each `*.md` file it:
   - reads the markdown source
   - splits source into blocks (`markdown_to_blocks`)
   - classifies each block and converts it to an HTML node tree (`block_to_html` and `text_to_html`)
   - renders the node tree to HTML and extracts the page title (first H1)
   - injects the content and title into `template.html`
   - writes the resulting page as `index.html` (or `name.html` for non-index files) into the mirrored `docs/` path
4. If a non-root `basepath` is passed to the generator, `href="/..."` and `src="/..."` occurrences in the generated HTML are rewritten to be relative to the basepath to support GitHub Pages hosting under a project path.

## Template

`template.html` is a simple HTML skeleton with two placeholders:

- `{{ Title }}` — replaced with the page title (first H1 in the markdown)
- `{{ Content }}` — replaced with the generated HTML body for the markdown

Example template:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ Title }}</title>
    <link href="/index.css" rel="stylesheet" />
  </head>
  <body>
    <article>{{ Content }}</article>
  </body>
</html>
```

## Tests

Unit tests for the parsing & rendering pipeline live in `src/test_cases/`.

Run them with:

```bash
python3 -m unittest discover -s src/test_cases -t src
```

## Deployment / GitHub Pages

This repository can be deployed to GitHub Pages by committing the generated `docs/` folder to the `gh-pages` branch or configuring GitHub Pages to serve from the `docs/` folder on the default branch.

If your project is served from a project path (e.g. `https://<user>.github.io/StaticSiteGen/`), pass the same path as a basepath to the generator. Example used by `build.sh`:

```bash
python3 src/main.py "/StaticSiteGen/"
```

Notes about `basepath` handling:

- When `basepath` is not `/`, the generator performs a simple textual rewrite of `href="/` and `src="/` to include the basepath (safe for typical templates and static asset references). This is intentionally lightweight and does not attempt advanced URL rewriting.

## Contract / API (concise)

- Input: a directory `content/` containing markdown files, a `template.html`, and `static/` assets
- Output: a fully generated static site in `docs/`
- Error modes: missing `static/` raises `FileNotFoundError` from `copy_static.py`; missing `content/` is raised by `sitegen.generate_pages_recursive` if not a directory; missing H1 title in a page raises `ValueError` from `extract_markdown.py` (the generator expects a top-level title).

## Edge cases & limitations

- Markdown support is intentionally small; it's a custom simple pipeline (not CommonMark full spec).
- Code fences are preserved verbatim but do not do syntax highlighting.
- Basepath rewriting is a simple string replace and may not cover every template edge case.
- Images and links are supported when represented as TextNode types in the pipeline.

## Contributing

Contributions welcome — small improvements, tests, or feature requests. If you add/change behavior, please add or update unit tests under `src/test_cases/`.

## Contact

If you need help, open an issue or pull request in the repo, I'll make sure to get back to it..

---

Project was built in collaboration with boot.dev Static Site Generator guide-project. Feel free to check them out for more information.
