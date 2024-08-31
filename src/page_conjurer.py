from block_markdown import markdown_to_blocks, markdown_to_html_node
from copy_static import clean_up_folder, get_path_tree, print_tree, make_copy
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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"\n[i] Conjuring pages...\n")
    print(f"    from : {dir_path_content}\n    to : {dest_dir_path}")
    try:
        template_file = open_file(template_path)
        if template_file:
            print(f'    using template "{template_path}"\n')
    except Exception as e:
        print(f'[!] template {template_file} is missing')
    
    folder_structure = get_path_tree(dir_path_content)
    print("[i] The source structure looks like this:\n")
    print_tree(folder_structure)
    
    for file in folder_structure:
        if os.path.isfile(file):
            file = os.path.splitext(file)
            if file[1] == 'md':
                html_node = markdown_to_html_node(file)
                html_content = html_node.to_html()
                print(f'[i] Generated HTML content:\n{html_content}\n') # Can be safely deleted after tests
                page_title = extract_title(file)
                page_content = template_file.replace('{{ Title }}', page_title).replace('{{ Content }}', html_content)
                write_file(dest_dir_path,page_content)
            else:
                print(f'{file} might not be a markdown file')

    return True

def main():
    src = './tests/content'
    des = './tests/public_test'
    templates = 'template.html'
    generate_pages_recursive(src, templates ,des)

if __name__ == "__main__":
    main()