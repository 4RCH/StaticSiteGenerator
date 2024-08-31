from copy_static import copy_static_to_public
from page_conjurer import generate_pages_recursive

def main():
    copy_static_to_public()
    generate_pages_recursive('./content', 'template.html', './public')
    return ('Done')

if __name__ == "__main__":
    main()