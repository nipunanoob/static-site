from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other: TextType):
        if (self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url):
            return True
        return False
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode):
    text_type_dict = {
        TextType.TEXT: None,
        TextType.BOLD: "b",
        TextType.ITALIC: "i",
        TextType.CODE: "code" 
    }
    if text_node.text_type in text_type_dict.keys():
        return LeafNode(text_type_dict[text_node.text_type],text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url == None:
            raise ValueError("Missing link URL for tag")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url == None:
            raise ValueError("Missing source image URL for tag")
        return LeafNode("img", "" , {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid TextType: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text_split = node.text.split(delimiter)
        if len(node_text_split) % 2 == 0:
            raise Exception(f"Delimiter {delimiter} was not closed!")
        else:
            for index in range(len(node_text_split)):
                if index % 2 == 0:
                    if node_text_split[index] != "":
                        new_nodes.append(TextNode(node_text_split[index], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(node_text_split[index], text_type))
    return new_nodes
