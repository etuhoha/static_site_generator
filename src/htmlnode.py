class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""

        return "".join([f' {k}="{v}"' for k, v in self.props.items()])

    def __repr__(self) -> str:
        return f"HTMLNode(<{self.tag}> '{self.value}' {self.children} {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("no value")

        if self.tag == None:
            return self.value

        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(<{self.tag}> '{self.value}' {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag")
        if self.children == None:
            raise ValueError("no children")

        result = f"<{self.tag}>"
        for c in self.children:
            result += c.to_html()
        result += f"</{self.tag}>"
        return result
