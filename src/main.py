from textnode import TextNode
import data_constants as tt
from copy_static import copy_static_to_public

def main():
    dummy = TextNode("This is dummy styled text", tt.text_type_bold, "https://www.google.com")
    copy_static_to_public()
    return ('Done')

if __name__ == "__main__":
    main()