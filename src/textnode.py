from htmlnode import LeafNode
import data_constants as tt

# Most basic text node created based on a string, a provided type and/or url
class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"Textnode {self.text}, {self.text_type}, {self.url}"

 # Convert a text node to an HTML LeafNode
def text_node_to_html_node(text_node):
    if text_node.text_type == tt.text_type_text:
        return LeafNode(tt.text_type_text, text_node.text, None)
    if text_node.text_type == tt.text_type_bold:
        return LeafNode(tt.text_type_bold, text_node.text, None)
    if text_node.text_type == tt.text_type_italic:
        return LeafNode(tt.text_type_italic, text_node.text, None)
    if text_node.text_type == tt.text_type_code:
        return LeafNode(tt.text_type_code, text_node.text, None)
    if text_node.text_type == tt.text_type_link:
        return LeafNode(tt.text_type_link, text_node.text, {"href":text_node.url})
    if text_node.text_type == tt.text_type_image:
        return LeafNode(tt.text_type_image, None, {"src":text_node.url ,"alt":text_node.text})
    raise Exception(f'[!] Text type: {text_node.text_type} is not a supported type')