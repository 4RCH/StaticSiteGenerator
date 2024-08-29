from textnode import TextNode, text_type_bold

def main():
    dummy = TextNode("This is dummy styled text", text_type_bold, "https://www.google.com")
    return print (dummy)

if __name__ == "__main__":
    main()