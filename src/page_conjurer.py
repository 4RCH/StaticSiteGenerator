from block_markdown import markdown_to_blocks, markdown_to_html_node
from copy_static import clean_up_folder
import os

def open_file(file_path):
    with open(file_path, "r", encoding="UTF-8") as content:
            file_content = content.read()
            return file_content

def write_file(file_path, content):
    if os.path.isfile(file_path):
        print(f'[i] File {os.path.basename(file_path)} already exists, cleaning up..')
        clean_up_folder(file_path)
    with open(file_path, 'x') as file:
        file.write(content)
    print (f'[i] File created: {file}')

def extract_title(markdown):
    chunks = markdown_to_blocks(markdown)
             
    # Extract the first h1 header
    header = next((chunk[2:] for chunk in chunks if chunk.startswith('# ')), None)
    
    if header:
        return header
    else:
         raise Exception('[!] Missing h1 header in the file')

def generate_page(from_path, template_path, dest_path):
    print(f'\n[i] Conjuring a page from {from_path} to {dest_path} using template {template_path}\n')
    
    # Read the markdown and template files
    markdown_file = open_file(from_path)
    template_file = open_file(template_path)

    # Convert markdown to html nodes and extract title
    html_node = markdown_to_html_node(markdown_file)
    html_content = html_node.to_html()
    print(f'[i] Generated HTML content:\n{html_content}\n')

    page_title = extract_title(markdown_file)

    # Replace the placeholder text
    page_content = template_file.replace('{{ Title }}', page_title).replace('{{ Content }}', html_content)

    #write the file to disk
    write_file(dest_path, page_content)
    return True
