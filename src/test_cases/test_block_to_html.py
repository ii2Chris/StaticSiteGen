import unittest

from functions.block_to_html import (
    markdown_to_html_node,
    _text_to_children,
    _strip_leading,
)


class TestBlockToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
            ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_levels(self):
        md = """
# Heading 1

## Heading 2

### Heading 3 with **bold**

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3 with <b>bold</b></h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )

    def test_blockquote(self):
        md = """
> This is a quote
> with multiple lines
> and **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and <b>bold</b> text</blockquote></div>",
        )

    def test_blockquote_single_line(self):
        md = "> A single line quote with _italics_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>A single line quote with <i>italics</i></blockquote></div>",
        )

    def test_unordered_list_dash(self):
        md = """
- First item
- Second item with **bold**
- Third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <code>code</code></li></ul></div>",
        )

    def test_unordered_list_asterisk(self):
        md = """
* Apple
* Banana with _emphasis_
* Cherry
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Apple</li><li>Banana with <i>emphasis</i></li><li>Cherry</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with **bold**
3. Third item with [link](https://example.com)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ol><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <a href="https://example.com">link</a></li></ol></div>',
        )

    def test_mixed_content(self):
        md = """
# Welcome

This is a paragraph with **bold** text.

## Features

- Feature one
- Feature two

> Important note here

```
code block
no parsing
```

Final paragraph.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Welcome</h1><p>This is a paragraph with <b>bold</b> text.</p><h2>Features</h2><ul><li>Feature one</li><li>Feature two</li></ul><blockquote>Important note here</blockquote><pre><code>code block\nno parsing\n</code></pre><p>Final paragraph.</p></div>",
        )

    def test_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_only_whitespace(self):
        md = "   \n\n   "
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Should result in empty div as whitespace-only blocks are typically filtered
        self.assertEqual(html, "<div></div>")

    def test_paragraph_multiline_collapse(self):
        md = """This is
a paragraph
that spans
multiple lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph that spans multiple lines</p></div>",
        )

    def test_code_block_multiline(self):
        md = """```
def hello():
    print("world")
    return True
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Code blocks preserve their content exactly as written
        self.assertIn("<pre><code>", html)
        self.assertIn("def hello():", html)
        self.assertIn('print("world")', html)
        self.assertIn("return True", html)

    def test_heading_with_inline_markdown(self):
        md = "### This has **bold** and _italic_ and `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This has <b>bold</b> and <i>italic</i> and <code>code</code></h3></div>",
        )

    def test_list_with_links(self):
        md = """
- [Google](https://google.com)
- [GitHub](https://github.com)
- Plain text item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li><a href="https://google.com">Google</a></li><li><a href="https://github.com">GitHub</a></li><li>Plain text item</li></ul></div>',
        )

    def test_ordered_list_multi_digit(self):
        md = """
10. Tenth item
11. Eleventh item
99. Ninety-ninth item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Tenth item</li><li>Eleventh item</li><li>Ninety-ninth item</li></ol></div>",
        )

    def test_complex_inline_in_paragraph(self):
        md = "This has **bold text** and _italic_ and `code` and [a link](https://test.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        # The exact output depends on your text parsing implementation
        # This test verifies that inline parsing happens correctly
        self.assertIn("<b>bold", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn("<code>code</code>", html)
        self.assertIn('<a href="https://test.com">a link</a>', html)


class TestTextToChildren(unittest.TestCase):
    def test_plain_text(self):
        children = _text_to_children("Hello world")
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].to_html(), "Hello world")

    def test_bold_text(self):
        children = _text_to_children("This is **bold** text")
        html = "".join([c.to_html() for c in children])
        self.assertEqual(html, "This is <b>bold</b> text")

    def test_italic_text(self):
        children = _text_to_children("This is _italic_ text")
        html = "".join([c.to_html() for c in children])
        self.assertEqual(html, "This is <i>italic</i> text")

    def test_code_text(self):
        children = _text_to_children("This is `code` text")
        html = "".join([c.to_html() for c in children])
        self.assertEqual(html, "This is <code>code</code> text")

    def test_link_text(self):
        children = _text_to_children("Click [here](https://example.com)")
        html = "".join([c.to_html() for c in children])
        self.assertEqual(html, 'Click <a href="https://example.com">here</a>')

    def test_image_text(self):
        children = _text_to_children("An image: ![alt](https://example.com/img.png)")
        html = "".join([c.to_html() for c in children])
        self.assertEqual(
            html, 'An image: <img src="https://example.com/img.png" alt="alt"></img>'
        )

    def test_multiple_inline_elements(self):
        children = _text_to_children("**bold** and _italic_ and `code`")
        html = "".join([c.to_html() for c in children])
        self.assertEqual(html, "<b>bold</b> and <i>italic</i> and <code>code</code>")


class TestStripLeading(unittest.TestCase):
    def test_strip_present(self):
        result = _strip_leading("> Hello", "> ")
        self.assertEqual(result, "Hello")

    def test_strip_not_present(self):
        result = _strip_leading("Hello", "> ")
        self.assertEqual(result, "Hello")

    def test_strip_partial_match(self):
        result = _strip_leading(">Hello", "> ")
        self.assertEqual(result, ">Hello")

    def test_strip_exact_prefix(self):
        result = _strip_leading("- Item", "- ")
        self.assertEqual(result, "Item")

    def test_strip_empty_string(self):
        result = _strip_leading("", "> ")
        self.assertEqual(result, "")

    def test_strip_prefix_longer_than_string(self):
        result = _strip_leading("Hi", "Hello ")
        self.assertEqual(result, "Hi")


if __name__ == "__main__":
    unittest.main()
