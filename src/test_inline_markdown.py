import unittest
import data_constants as tt
from textnode import TextNode
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_links, text_to_textnode

class TestMarkdown(unittest.TestCase):
    def test_bold(self):
        node0 = TextNode("This is text with a **bold words** word tag.", tt.text_type_text)
        splitnode = split_nodes_delimiter([node0], tt.delimiter_bold, tt.text_type_bold)
        self.assertEqual(str(splitnode), "[Textnode This is text with a , text, None, Textnode bold words, bold, None, Textnode  word tag., text, None]" )

    def test_text(self):
        node1 = TextNode("This is text without tags.", tt.text_type_text)
        splitnode = split_nodes_delimiter([node1], tt.delimiter_bold, tt.text_type_text)
        self.assertEqual(str(splitnode), "[Textnode This is text without tags., text, None]")
    
    def test_italic(self):
        node2 = TextNode("This is text with *italic* tags.", tt.text_type_text)
        splitnode = split_nodes_delimiter([node2], tt.delimiter_italics, tt.text_type_italic)
        self.assertEqual(str(splitnode), "[Textnode This is text with , text, None, Textnode italic, italic, None, Textnode  tags., text, None]")

    def test_code(self):
        node3 = TextNode("New is text with `code` tags.", tt.text_type_text)
        splitnode = split_nodes_delimiter([node3], tt.delimiter_code, tt.text_type_code)
        self.assertEqual(str(splitnode), "[Textnode New is text with , text, None, Textnode code, code, None, Textnode  tags., text, None]")

    def test_missing_markdown(self):
        node3 = TextNode("This * isn't a tag.", tt.text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node3], tt.delimiter_italics, tt.text_type_italic)
    
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(extract_markdown_images(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(extract_markdown_links(text), [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')])

    def test_split_nodes_image(self):
        nodes = [TextNode("This is text with some images ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", tt.text_type_text),]
        result = [
            TextNode("This is text with some images ", tt.text_type_text),
            TextNode("rick roll", tt.text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", tt.text_type_text),
            TextNode("obi wan", tt.text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(split_nodes_image(nodes) , result)

    def test_split_nodes_links(self):
        nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", tt.text_type_text),]
        result = [
            TextNode("This is text with a link ", tt.text_type_text),
            TextNode("to boot dev", tt.text_type_link, "https://www.boot.dev"),
            TextNode(" and ", tt.text_type_text),
            TextNode("to youtube", tt.text_type_link, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(split_nodes_links(nodes) , result)

    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("This text directs you to Google [to Google](https://www.google.com) all roads go to Google", tt.text_type_text),
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", tt.text_type_text),
        ]
        result = [
            TextNode("This text directs you to Google ", tt.text_type_text),
            TextNode("to Google", tt.text_type_link, "https://www.google.com"),
            TextNode(" all roads go to Google", tt.text_type_text),
            TextNode("This is text with a link ", tt.text_type_text),
            TextNode("to boot dev", tt.text_type_link, "https://www.boot.dev"),
            TextNode(" and ",tt.text_type_text),
            TextNode("to youtube", tt.text_type_link, "https://www.youtube.com/@bootdotdev"),

        ]
        self.assertListEqual(split_nodes_links(nodes), result)
    
    def test_split_multiple_images(self):
        nodes = [
            TextNode("This is an image ![Deadpool](https://imgur.com/gallery/deadpool-icon-Psrh9jM) Oh noes![-_-]", tt.text_type_text),
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", tt.text_type_text)
        ]
        results = [
            TextNode("This is an image ", tt.text_type_text),
            TextNode("Deadpool", tt.text_type_image, "https://imgur.com/gallery/deadpool-icon-Psrh9jM"),
            TextNode(" Oh noes![-_-]", tt.text_type_text),
            TextNode("This is text with a ", tt.text_type_text),
            TextNode("rick roll", tt.text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", tt.text_type_text),
            TextNode("obi wan", tt.text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(split_nodes_image(nodes), results)

    def test_text_to_textnodes(self):
        raw_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        results = [
            TextNode("This is ", tt.text_type_text),
            TextNode("text", tt.text_type_bold),
            TextNode(" with an ", tt.text_type_text),
            TextNode("italic", tt.text_type_italic),
            TextNode(" word and a ", tt.text_type_text),
            TextNode("code block", tt.text_type_code),
            TextNode(" and an ", tt.text_type_text),
            TextNode("obi wan image", tt.text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", tt.text_type_text),
            TextNode("link", tt.text_type_link, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnode(raw_text), results)

if __name__ == "__main__":
    unittest.main()