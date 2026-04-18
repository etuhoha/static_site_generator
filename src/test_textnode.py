import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        self.assertNotEqual(node, TextNode(node.text, TextType.ITALIC, node.url))
        self.assertNotEqual(node, TextNode("foo", node.text_type, node.url))
        self.assertNotEqual(node, TextNode(node.text, node.text_type, "foo.com"))

    def assertSplit(self, text, delimiter, text_type, expected):
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_delimiter([node], delimiter, text_type)

        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            r = result[i]
            e = expected[i]
            self.assertEqual(r.text, e[0])
            self.assertEqual(r.text_type, e[1])

    def test_split_nodes_delimiter(self):
        self.assertSplit("Hello **world**!", "**", TextType.BOLD, [
            ("Hello ", TextType.TEXT),
            ("world", TextType.BOLD),
            ("!", TextType.TEXT),
        ])
        self.assertSplit("_world_", "_", TextType.ITALIC, [
            ("world", TextType.ITALIC),
        ])
        self.assertSplit("This `code` is worse than `code2`.", "`", TextType.CODE, [
            ("This ", TextType.TEXT),
            ("code", TextType.CODE),
            (" is worse than ", TextType.TEXT),
            ("code2", TextType.CODE),
            (".", TextType.TEXT),
        ])

        self.assertRaisesRegex(ValueError, "invalid.*foo bar", lambda: split_nodes_delimiter([TextNode("*foo bar", TextType.TEXT)], "*", TextType.BOLD))


if __name__ == "__main__":
    unittest.main()
