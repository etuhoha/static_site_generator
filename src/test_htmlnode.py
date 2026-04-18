import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        self.assertEqual(HTMLNode("p", "foo", [], {}).props_to_html(), '')
        self.assertEqual(HTMLNode("p", "foo", [], {"id": "foo"}).props_to_html(), ' id="foo"')
        self.assertEqual(HTMLNode("p", "foo", [], {"id": "foo", "class": "bar"}).props_to_html(),
                          ' id="foo" class="bar"')


    def test_leaf_to_html_p(self):
        self.assertEqual(LeafNode(None, "Hello, world!").to_html(), "Hello, world!")
        self.assertEqual(LeafNode("p", "Hello, world!").to_html(), "<p>Hello, world!</p>")
        self.assertEqual(LeafNode("b", "Hello, world!").to_html(), "<b>Hello, world!</b>")


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        self.assertEqual(text_node_to_html_node(TextNode("This is a bold node", TextType.BOLD)).to_html(),
                         "<b>This is a bold node</b>")

        self.assertEqual(text_node_to_html_node(TextNode("This is a link node", TextType.LINK, "foo.com")).to_html(),
                         '<a href="foo.com">This is a link node</a>')

        self.assertEqual(text_node_to_html_node(TextNode("This is an image node", TextType.IMAGE, "foo.com")).to_html(),
                         '<img src="foo.com" alt="This is an image node"></img>')


if __name__ == "__main__":
    unittest.main()
