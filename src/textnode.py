from enum import Enum

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    NORMAL = "normal"
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

