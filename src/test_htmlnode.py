import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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



if __name__ == "__main__":
    unittest.main()
