from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "**bold**"
    ITALIC = "_italic_"
    UNDERLINE = "<u>underline</u>"
    STRIKETHROUGH = "~~strikethrough~~"
    CODE = "`code`"
    LINK = "[link](http://example.com)"
    IMAGE = "![alt text](image.jpg)"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (self.text, self.text_type, self.url) == (
                other.text,
                other.text_type,
                other.url,
            )
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
