import re
from textnode import TextNode
import data_constants as tt

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # Check if the old_node is a text node and if so let it go...
        if old_node.text_type != tt.text_type_text:
            new_nodes.append(old_node)
            continue
        # Check if the old_node is a list node and if so let it go...
        if old_node.text.strip().startswith(('* ', '- ', '+ ')):
            new_nodes.append(old_node)
            continue

        # Now to deal with real delimiters...
        chunks = old_node.text.split(delimiter)
        if len(chunks)% 2 == 0:
            raise ValueError("[!] Missing closing delimiter")
        for i, chunk in enumerate(chunks):
            if chunk:
                new_nodes.append(TextNode(chunk, text_type if i % 2 else tt.text_type_text))
            
    return new_nodes

def extract_markdown_images(raw_markdown):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    formatted_text = re.findall(pattern, raw_markdown)
    return formatted_text

def extract_markdown_links(raw_markdown):
    pattern = r"\[(.*?)\]\((.*?)\)"
    formatted_text = re.findall(pattern, raw_markdown)
    return formatted_text

def split_nodes_generic(nodes, pattern, text_type):
    new_nodes = []
    for node in nodes:
        if not re.search(pattern, node.text):
            new_nodes.append(node)
            continue
        
        split_nodes =[]
        matches = re.finditer(pattern, node.text)
        last_index = 0
        
        for match in matches:
            start_index = match.start()
            if start_index > last_index:
                split_nodes.append(TextNode(node.text[last_index:start_index], tt.text_type_text))
            split_nodes.append(TextNode(match.group(1), text_type, match.group(2)))
            last_index = match.end()
        
        #add remaining text after the last image
        if last_index < len(node.text):
            split_nodes.append(TextNode(node.text[last_index:], tt.text_type_text))

        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(nodes):
    return split_nodes_generic(nodes, r"!\[(.*?)\]\((.*?)\)", tt.text_type_image)

def split_nodes_links(nodes):
    return split_nodes_generic(nodes, r"\[(.*?)\]\((.*?)\)", tt.text_type_link)

def text_to_textnode(raw_text):
    new_nodes = [TextNode(raw_text, tt.text_type_text)]
    delimiters =[
        (tt.delimiter_bold, tt.text_type_bold),
        (tt.delimiter_italics, tt.text_type_italic),
        (tt.delimiter_code, tt.text_type_code),
    ]

    for delimiter, text_type in delimiters:
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, text_type)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_links(new_nodes)

    return new_nodes