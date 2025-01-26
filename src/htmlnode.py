

class HTMLNode():
    
    def __init__(self, tag:str=None, value:str=None, children:"HTMLNode"=None, props:dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        props_string = ""
        for key,value in self.props.items():
              props_string += f" {key}=\"{value}\""
        return props_string
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag, value,None,props)
    def to_html(self):
        if self.value == None:
            raise ValueError("Value can not be missing in leaf node")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
    def __eq__(self, other):
        # Ensure all attributes match
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.props == other.props
        )
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag missing")
        if self.children == None:
            raise ValueError("Children missing")
        # return string representing html of node and its children
        if self.props:
            startingTag = f"<{self.tag}{self.props_to_html()}>"
        else:
            startingTag = f"<{self.tag}>"
        endingTag = f"</{self.tag}>"
        htmlText = ""
        for child in self.children:
            htmlText += child.to_html()
        htmlText  = startingTag + htmlText + endingTag
        return htmlText