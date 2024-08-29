import os

def clean_up_static_folder(address):
    for root, dirs, files in os.walk(address, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f'[i] Deleted file: {file_path}')
            except Exception as e:
                print(f'[!] Could not delete file: {file_path}. Error: {e}')
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)
                print (f'[i] Deleted folder: {dir_path}')
            except OSError as e:
                print(f'[!] Could not delete folder (not empty): {dir_path}. Error: {e}')


    print (f'[!] Deleted all files and empty folders in the folder {address}')


def make_backup(address, backup_folder):
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    contents = get_path_tree(address)
    for addr, folders, files in contents:
        # Create the corresponding folders in the backup directory
        relative_path = os.path.relpath(addr, start=address)
        backup_path = os.path.join(backup_folder, relative_path)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        # Copy files to the backup directory
        for file in files:
            src_file = os.path.join(addr, file)
            dst_file = os.path.join(backup_path, file)
            copy_file(src_file, dst_file)
    
    print (f'[i] Backed up the folder to {backup_folder}')


def copy_file(src, dst):
    try:
        with open(src, 'rb') as file_source:
            with open(dst, 'wb') as file_dest:
                file_dest.write(file_source.read())
        print(f'[i] Copied file from {src} to {dst}')
    except Exception as e:
        print(f'[!] Could not copy file from {src} to {dst}. Error: {e}')

def get_path_tree(address):
    contents = []

    # Get initial address contents or return an error if address doesn't exist    
    try:
        address_data = os.listdir(address)
    except Exception as e:
        print(f'[!] The address: {address} does not exist')
        return contents

    # Make a tuple of files and a tuple of folders
    folders = []
    files = []
    for item in address_data:
        item_path = os.path.join(address, item)
        if os.path.isdir(item_path):
            folders.append(item_path)
        else:
            files.append(item)

    # Wrap this into a list of ["address", (folders), (files)]
    contents.append((address, tuple(folders), tuple(files)))

    # Now loop through until there are no directories left
    for folder in folders:
        contents.extend(get_path_tree(folder))

    return contents


def print_tree(contents):
    address_map = {address: (folders, files) for address, folders, files in contents}

    def _print_tree(address, indent):
        print(f'{indent}{os.path.basename(address)}/')
        sub_indent = indent + "    "
        folders, files = address_map.get(address, ([],[]))
        for file in files:
            print(f'{sub_indent}{file}')
        for folder in folders:
            _print_tree(folder, sub_indent)
    
    if contents:
        root_address = contents[0][0]
        _print_tree(root_address, '')
        

def main():
    public_folder = "./public"
    static_folder = "./static"
    backup_folder = './static/backups'

    make_backup(public_folder, backup_folder)
    clean_up_static_folder(public_folder)
    contents = get_path_tree(public_folder)
    print_tree(contents)


if __name__ == "__main__":
    main()