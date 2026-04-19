from blocknode import block_to_block_type, markdown_to_blocks, BlockType
from textnode import TextType, TextNode, text_to_textnodes

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

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

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

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node is None:
        raise ValueError("node required")

    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise ValueError("unknown type")

def mdtext_to_html_nodes(text):
    return list(map(text_node_to_html_node, text_to_textnodes(text)))

def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                children.append(ParentNode("pre", [LeafNode("code", block.strip("`").lstrip("\n"))]))
            case BlockType.PARA:
                ch = mdtext_to_html_nodes(block.replace("\n", " "))
                children.append(ParentNode("p", ch))
            case BlockType.HEADING:
                head_level = len(block)
                block = block.lstrip("#")
                head_level -= len(block)
                children.append(LeafNode(f"h{head_level}", block.strip()))
            case BlockType.QUOTE:
                lines = map(lambda s: s.lstrip(">").lstrip(), block.split("\n"))
                ch = map(lambda l: LeafNode(None, l + "<br>"), lines)
                children.append(ParentNode("blockquote", list(ch)))
            case BlockType.U_LIST:
                lines = map(lambda s: s.lstrip("-").lstrip(), block.split("\n"))
                ch = map(lambda l: LeafNode("li", l), lines)
                children.append(ParentNode("ul", ch))
            case BlockType.O_LIST:
                lines = map(lambda s: s.split(".", maxsplit=1)[1].lstrip(), block.split("\n"))
                ch = map(lambda l: LeafNode("li", l), lines)
                children.append(ParentNode("ol", ch))

    return ParentNode("div", children)
