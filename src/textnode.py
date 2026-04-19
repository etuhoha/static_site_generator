import re

from enum import Enum

class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    result = []

    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            result.append(n)
            continue

        txt = n.text
        while delimiter in txt:
            sp = txt.split(delimiter, maxsplit=1)
            if len(sp[0]) > 0:
                result.append(TextNode(sp[0], TextType.TEXT))
            if delimiter not in sp[1]:
                raise ValueError(f"invalid markup: '{txt}'")
            sp = sp[1].split(delimiter, maxsplit=1)
            result.append(TextNode(sp[0], text_type))
            txt = sp[1]

        if len(txt) > 0:
            result.append(TextNode(txt, TextType.TEXT))


    return result

def split_nodes_image(old_nodes):
    return split_url_nodes_image(old_nodes, r"!\[([^\]]*)\]\(([^\)]*)\)", TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_url_nodes_image(old_nodes, r"\[([^\]]*)\]\(([^\)]*)\)", TextType.LINK)

def split_url_nodes_image(old_nodes, regex, text_type):
    result = []

    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            result.append(n)
            continue

        text = n.text
        start = 0
        matches = re.finditer(regex, text)
        for m in matches:
            pref = text[start:m.start()]
            if len(pref) > 0:
                result.append(TextNode(pref, TextType.TEXT))
            alt = m[1]
            url = m[2]
            result.append(TextNode(alt, text_type, url))
            start = m.end()

        if start < len(text):
            result.append(TextNode(text[start:], TextType.TEXT))

    return result


def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]*)\]\(([^\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[([^\]]*)\]\(([^\)]*)\)", text)

def text_to_textnodes(text):
    res= [TextNode(text, TextType.TEXT)]
    res = split_nodes_image(res)
    res = split_nodes_link(res)
    res = split_nodes_delimiter(res, "**", TextType.BOLD)
    res = split_nodes_delimiter(res, "_", TextType.ITALIC)
    res = split_nodes_delimiter(res, "`", TextType.CODE)
    return res
