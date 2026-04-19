import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, extract_title, markdown_to_html_node, text_node_to_html_node
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

    def test_heading(self):
        md = "### Foo Bar"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Foo Bar</h3></div>",
        )

    def test_quote(self):
        md = """
> The quarterly results look great!
>
> Revenue was off the chart.
> Profits were higher than ever.
>
> Everything is going according to plan.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>The quarterly results look great!<br><br>Revenue was off the chart.<br>Profits were higher than ever.<br><br>Everything is going according to plan.<br></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- first
- second
- third
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first</li><li>second</li><li>third</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first
2. second
3. third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_extract_title(self):
        self.assertEqual(extract_title("# Foo Bar"), "Foo Bar")
        self.assertRaises(Exception, lambda: extract_title("#Foo Bar"))
        self.assertRaises(Exception, lambda: extract_title("Foo Bar"))

if __name__ == "__main__":
    unittest.main()
