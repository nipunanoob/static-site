from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    TEXT = "normal"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type: TextType, url= None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        if isinstance(other, TextNode):
            if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
                return True
        return False
    def __repr__(self):
        if isinstance(self.text_type, TextType):
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    def _text_error():
        raise ValueError("Text value can not be none")
    tag_mapping = {
        TextType.BOLD: ("b", lambda tn: tn.text if tn.text else _text_error()),
        TextType.TEXT: (None, lambda tn: tn.text if tn.text else _text_error()),
        TextType.ITALIC: ("i", lambda tn: tn.text if tn.text else _text_error()),
        TextType.CODE: ("code", lambda tn: tn.text if tn.text else _text_error()),
    }
    if text_node.text_type in tag_mapping:
        tag, text_getter = tag_mapping[text_node.text_type]
        return LeafNode(tag, text_getter(text_node))
    elif text_node.text_type == TextType.LINK:
        if not text_node.text:
            raise ValueError("TextType.LINK requires anchor text")
        if not text_node.url:
            raise ValueError("TextType.LINK requires URL for href attribute")
        return LeafNode("a",text_node.text,{"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("TextType.IMAGE requires URL for src attribute")
        alt = text_node.text if text_node.text else ""
        return LeafNode("img","",{"src": text_node.url, "alt": alt})
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")

