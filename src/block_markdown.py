import re
import data_constants as tt
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnode

# Break text into blocks
def markdown_to_blocks(markdown):
    pattern = r"\n\s+"
    blocks = []

    lines = re.split(pattern, markdown)
    blocks = [line for line in lines if line.strip()]
    return blocks

# Get a block and return the type 
def block_to_blocktype(markdown_block):
    if not markdown_block:
        raise ValueError("[!] Missing markdown string")
    
    lines = markdown_block.split("\n")
    first_char = markdown_block[0]

    # Check for Heading type
    if first_char == tt.tag_heading:
        for i in range(1, 7):
            if markdown_block.startswith('#' * i + ' '):
                return (tt.markdown_heading, i)
    
    # Check for Code type
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return tt.markdown_code
    
    # Check for Quote type
    if markdown_block.startswith(tt.tag_quote + ' '):
        if all(line.startswith(f'{tt.tag_quote} ') for line in lines):
            return tt.markdown_quote
    
    # Check for unordered list type
    if markdown_block.startswith(('* ','- ')):
        if all(line.startswith(('* ', '- ')) for line in lines):                
            return tt.markdown_un_list
    
    # Check for ordered list type
    if markdown_block[0].isdigit() and markdown_block[1] == '.':
        count = 1
        if all(line.startswith(f'{count}. ') for count, line in enumerate(lines, start=1)):
            return tt.markdown_ord_list

    return tt.markdown_paragraph

def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    blocks_def = []
    for block in blocks:
        blocks_def.append((block, block_to_blocktype(block)))    
    children = block_formatter(blocks_def)
    return ParentNode('div', children, None)

def block_formatter(block_def):
    nodes_list = []

    block_type_to_function = {
        tt.markdown_paragraph: text_to_paragraph,
        tt.markdown_code: text_to_code,
        tt.markdown_quote: text_to_quote,
        tt.markdown_un_list: text_to_un_list,
        tt.markdown_ord_list: text_to_ord_list,
    }

    for block in block_def:
        block_type = block[1]
        if isinstance(block_type, tuple) and block_type[0] == tt.markdown_heading:
            nodes_list.append(text_to_header(block))
        elif block_type in block_type_to_function:
            nodes_list.append(block_type_to_function[block_type](block[0]))
        else:
            raise ValueError(f'[!] Unsuported block type: {block_type}')

    return nodes_list

def text_to_children(text):
    children = []
    text_nodes = text_to_textnode(text)
    for text_node in text_nodes:
        html_node = (text_node_to_html_node(text_node))
        children.append(html_node)
    return children

def text_to_paragraph(raw_text):
    children = text_to_children(raw_text)
    return ParentNode('p', children)

def text_to_header(header_data):
    children = text_to_children(header_data[0])
    return ParentNode(f'h{header_data[1][1]}', children)

def text_to_code(raw_text):
    children = text_to_children(raw_text)
    code = ParentNode('code', children)
    return ParentNode('pre', [code])

def text_to_quote(raw_text):
    chunks = split_text_into_chunks(raw_text, '\n')
    if not chunks or all(chunk.strip() == "" for chunk in chunks):
        raise ValueError('[!] Invalid input: empty or whitespace-only quote block')
    children = []
    for chunk in chunks:
        if chunk.strip():
            children = text_to_children(chunk)
    return ParentNode('blockquote', children)

def text_to_un_list(raw_text):
    unord_list =[]
    chunks = split_text_into_chunks(raw_text, '\n')
    for chunk in chunks:
        children = text_to_children(chunk)
        unord_list.append(ParentNode('li', children))
    return ParentNode('ul', unord_list)

def text_to_ord_list(raw_text):
    ord_list = []
    chunks = raw_text.split('\n')
    for chunk in chunks:
        children = text_to_children(chunk)
        ord_list.append(ParentNode('li', children))
    return ParentNode('ol', ord_list)

def split_text_into_chunks(text, delimiter):
    return text.split(delimiter)

'''
def main():
    with open("./src/markdown.md", "r", encoding="UTF-8") as block_list:
            markdown_content = block_list.read()
    final_object = markdown_to_html_node(markdown_content)
    print(final_object)

if __name__ == "__main__":
    main()

'''