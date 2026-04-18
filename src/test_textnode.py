import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        self.assertNotEqual(node, TextNode(node.text, TextType.ITALIC, node.url))
        self.assertNotEqual(node, TextNode("foo", node.text_type, node.url))
        self.assertNotEqual(node, TextNode(node.text, node.text_type, "foo.com"))


if __name__ == "__main__":
    unittest.main()
