from textnode import TextNode, TextType

def main():
    test = TextNode("something", TextType.ITALIC, "https://www.boot.dev")
    print(test)

if __name__ == "__main__":
    main()