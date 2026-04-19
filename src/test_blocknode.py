import unittest

from blocknode import BlockType, block_to_block_type, markdown_to_blocks

class TestBlockNode(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("### Foo Bar"), BlockType.HEADING)

        code = """```
        def foo():
            pass
        ```"""
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

        quote = """> quote 1
> quote 2
> quote 3"""
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

        ulist = """- list item
- list item 2
- list item 3"""
        self.assertEqual(block_to_block_type(ulist), BlockType.U_LIST)

        olist = """1. list item
2. list item 2
3. list item 3"""
        self.assertEqual(block_to_block_type(olist), BlockType.O_LIST)
