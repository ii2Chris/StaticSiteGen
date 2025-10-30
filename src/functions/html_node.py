class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")

    def props_to_html(self):
        if self.props is None:
            return ""
        #  href="https://www.google.com" target="_blank"
        return ' '.join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return f"HTMLNode ({self.tag}, {self.value}, {self.children}, {self.props})"



class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")

        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag is None:
            return self.value

        props_str = ""
        if self.props:
            props_str = " "+ self.props_to_html()

        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None or children is None:
            raise ValueError("ParentNode must have a tag and children")

        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.children is None:
            raise ValueError("ParentNode must have children to convert to HTML")
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")

        props_str = ""
        if self.props:
            props_str = " "+ self.props_to_html()

        # Recursively convert children to HTML
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
