import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class Testhtmlnode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode("a", "https://www.google.com", None, {"href":"https://www.google.com"})
        valid_tags = ["a", "b", "i", "q", "code", "href", "p", "h1"]
        self.assertIn(node.tag, valid_tags, "[!] Missing tag")
    
    def test_value(self):
        node = HTMLNode("a", None, None, {"href":"https://www.google.com"})
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
    
    def test_prop(self):
        node = HTMLNode("a", "https://www.google.com", None, None)
        self.assertEqual(node.props, {}, "[!] missing props")

    def test_props_to_html(self):
        node = HTMLNode("a", "https://www.google.com", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_leaf_notag(self):
        node = LeafNode(None, "This is plain text.", None)
        self.assertEqual(node.to_html(), "This is plain text.")
    
    def test_no_children(self):
        node = LeafNode("p", "Single paragraph.")
        self.assertEqual(node.to_html(), "<p>Single paragraph.</p>")

    def test_leaf_link(self):
        node = LeafNode("a", "This is a link to www.google.com.", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">This is a link to www.google.com.</a>')

    def test_leaf_code(self):
        node = LeafNode("code", "for slice in cake:", None)
        self.assertEqual(node.to_html(), '<code>for slice in cake:</code>')
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span","child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span",[grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_multi_children(self):
        node = ParentNode(
            "p",
             [
                 LeafNode("b","Bold text"),
                 LeafNode(None,"Normal text"),
                 LeafNode("code","Code text"),
                 LeafNode("i","italic text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<code>Code text</code><i>italic text</i></p>")

    def test_to_html_headings(self):
        node = ParentNode(
            "h1",
             [
                 LeafNode("b","Bold text"),
                 LeafNode(None,"Normal text"),
                 LeafNode("code","Code text"),
                 LeafNode("i","italic text"),
            ],
        )
        self.assertEqual(node.to_html(), "<h1><b>Bold text</b>Normal text<code>Code text</code><i>italic text</i></h1>")

if __name__ == "__main__":
    unittest.main()