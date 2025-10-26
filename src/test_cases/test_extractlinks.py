import unittest

from functions.extract_links import extract_markdown_images, extract_links

class TestTextToHtml(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_links(self):
        matches = extract_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "Images: ![img1](http://example.com/1.png) and ![img2](http://example.com/2.jpg)"
        )
        self.assertListEqual(
            [("img1", "http://example.com/1.png"), ("img2", "http://example.com/2.jpg")],
            matches,
        )

    def test_none_found(self):
        self.assertListEqual(extract_markdown_images("no imgs here"), [])
        self.assertListEqual(extract_links("no links here"), [])

if __name__ == "__main__":
    unittest.main()
