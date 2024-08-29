import unittest
import data_constants as tt
from block_markdown import markdown_to_blocks, block_to_blocktype, markdown_to_html_node
from htmlnode import HTMLNode, ParentNode

block_types = [
            tt.markdown_paragraph,
            (tt.markdown_heading, 1),
            (tt.markdown_heading, 2),
            (tt.markdown_heading, 3),
            (tt.markdown_heading, 4),
            (tt.markdown_heading, 5),
            (tt.markdown_heading, 6),
            tt.markdown_code,
            tt.markdown_quote,
            tt.markdown_un_list,
            tt.markdown_ord_list,
            ]

blocks = [
    '# This is the main header',
    '## This is another header',
    'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
    '* This is the first list item in a list block\n* This is a list item\n* This is another list item',
    '###### This is a Header for the list',
    '1. This is another list item in a list block\n2. This is a list item\n3. This is another list item',
    ]

class TestBlockMarkdown(unittest.TestCase):

    def setUp(self):
        with open("./static/markdown.md", "r", encoding="UTF-8") as block_list:
            self.markdown_content = block_list.read()
        
    """Test that markdown content is correctly split into blocks."""
    def test_markdown_to_blocks(self):
        self.assertEqual(markdown_to_blocks(self.markdown_content), blocks)

    """Test that each block is correctly identified with its type."""
    def test_markdown_to_block_to_types(self):
        for block in blocks:
            self.assertIn(block_to_blocktype(block), block_types)
    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_blocktype(block), (tt.markdown_heading, 1))
        block = "```\ncode\n```"
        self.assertEqual(block_to_blocktype(block), tt.markdown_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_blocktype(block), tt.markdown_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_blocktype(block), tt.markdown_un_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_blocktype(block), tt.markdown_ord_list)
        block = "paragraph"
        self.assertEqual(block_to_blocktype(block), tt.markdown_paragraph)

    def test_markdown_to_html_node(self):
        html_node = markdown_to_html_node(self.markdown_content)        
        self.assertTrue(markdown_to_html_node(self.markdown_content))
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "div")
        self.assertGreater(len(html_node.children), 0)
        for child in html_node.children:
            self.assertIsInstance(child, HTMLNode)

    def test_empty_markdown(self):
        self.assertEqual(markdown_to_blocks(""),[])

    def test_single_line_markdown(self):
        self.assertEqual(markdown_to_blocks("# Single line heading"), ["# Single line heading"])

if __name__ == "__main__":
    unittest.main()