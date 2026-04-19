import unittest

from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


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

    def test_extract_markdown_images(self):
        nodes = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        n1 = nodes[0]
        self.assertEqual(n1[0], "rick roll")
        self.assertEqual(n1[1], "https://i.imgur.com/aKaOqIh.gif")

        n2 = nodes[1]
        self.assertEqual(n2[0], "obi wan")
        self.assertEqual(n2[1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_extract_markdown_links(self):
        nodes = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(2, len(nodes))
        n1 = nodes[0]
        self.assertEqual(n1[0], "to boot dev")
        self.assertEqual(n1[1], "https://www.boot.dev")

        n2 = nodes[1]
        self.assertEqual(n2[0], "to youtube")
        self.assertEqual(n2[1], "https://www.youtube.com/@bootdotdev")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link text](https://foo.bar/index.html) and another [second text](https://bar.baz/order/2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://foo.bar/index.html"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second text", TextType.LINK, "https://bar.baz/order/2"
                ),
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()
