import unittest
from blocks import markdown_to_blocks, BlockType, block_to_block_type


class TestBlocks(unittest.TestCase):
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
    def test_markdown_to_blocks_trims_and_ignores_empty(self):
        md = """


   First block with spaces   

Second block


Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block with spaces",
                "Second block",
                "Third block",
            ],
        )

    def test_markdown_to_blocks_multiple_lists_and_paragraphs(self):
        md = """Intro paragraph

- item one
- item two

Another paragraph

1. first
2. second"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Intro paragraph",
                "- item one\n- item two",
                "Another paragraph",
                "1. first\n2. second",
            ],
        )

    def test_heading_block_to_block(self):
        text = """## Heading"""
        result = block_to_block_type(text)

        expected_result = BlockType.HEADING

        self.assertEqual(result, expected_result)

    def test_paragraph_block_to_block(self):
        text = """This is a paragraph example on markdown."""
        result = block_to_block_type(text)

        expected_result = BlockType.PARAGRAPH

        self.assertEqual(result, expected_result)

    def test_quote_block_to_block(self):
        text = """> This is a quote block."""
        result = block_to_block_type(text)

        expected_result = BlockType.QUOTE

        self.assertEqual(result, expected_result)

    def test_code_block_to_block(self):
        text = """```\n<html>\n<head>\n</head>\n</html>```"""
        result = block_to_block_type(text)

        expected_result = BlockType.CODE

        self.assertEqual(result, expected_result)

    def test_unordered_block_to_block(self):
        text = """- This is one item on a list\n- This is another item on a list"""
        result = block_to_block_type(text)

        expected_result = BlockType.UNORDERED_LIST

        self.assertEqual(result, expected_result)

    def test_ordered_block_to_block(self):
        text = """1. This is first item on a list\n2. This is second item on a list"""
        result = block_to_block_type(text)

        expected_result = BlockType.ORDERED_LIST

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
