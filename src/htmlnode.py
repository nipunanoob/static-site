

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):

        # An HTMLNode without a tag will just render as raw text
        # An HTMLNode without a value will be assumed to have children
        # An HTMLNode without children will be assumed to have a value
        # An HTMLNode without props simply won't have any attributes

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        return NotImplementedError
    
    def props_to_html(self):
        html_string = ""
        for key,val in self.props.items():
            html_string += f" {key}=\"{val}\""
        return html_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}), {self.props}"
    
    def __eq__(self, other):
        if (self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props):
            return True
        return False

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf node must have a value")
        elif self.tag == None:
            return self.value
        else:
            if self.props:
                html_tag = f"<{self.tag}"
                html_tag += self.props_to_html() #converts props to html text using parent function
                html_tag += f">{self.value}</{self.tag}>"
            else:
                html_tag = f"<{self.tag}>{self.value}</{self.tag}>"
            return html_tag

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag is missing in parent node")
        elif self.children == None or self.children == []:
            raise ValueError("Children must be present in parent node")
        else:
            html_tag = f"<{self.tag}>"
            for child in self.children:
                if not isinstance(child, ParentNode) and not isinstance(child, LeafNode):
                    raise TypeError("Children of parent node must be object of either leafnode or parentnode class")
                html_tag += child.to_html()
            html_tag += f"</{self.tag}>"
            return html_tag

