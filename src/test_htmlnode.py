
import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode

class TestTextNode(unittest.TestCase):
    def test_type(self):
        node = HTMLNode("p","sample",props={"href": "https://www.google.com"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "sample")
        self.assertEqual(node.props, {"href": "https://www.google.com"})
    def test_props_to_html(self):
        node = HTMLNode("p","sample",props={"href": "https://www.google.com",
                                            "target": "_blank",})
        props_string = node.props_to_html()
        self.assertEqual(props_string, f" href=\"https://www.google.com\" target=\"_blank\"")  
    def test_repr(self): 
        node = HTMLNode("p","sample",props={"href": "https://www.google.com"})
        self.assertEqual(repr(node), "HTMLNode(p, sample, None, {'href': 'https://www.google.com'})")
    def test_leaf_to_html_valid(self):
        leafnode = LeafNode("p", "This is a paragraph of text.", None)
        self.assertEqual(leafnode.to_html(), "<p>This is a paragraph of text.</p>")
    def test_leaf_to_html_value_missing(self):
        leafnode = LeafNode("p", None, None)
        with self.assertRaises(ValueError) as assert_error:
            leafnode.to_html()
        self.assertEqual(assert_error.exception.args[0], "Value can not be missing in leaf node")
    def test_leaf_to_html_tag_missing(self):
        leafnode = LeafNode(None, "This is raw", None)
        self.assertEqual(leafnode.to_html(),"This is raw")
    def test_parent_only_leaf_to_html(self):
        parentnode = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(parentnode.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    def test_parent_no_children(self):
        parentnode = ParentNode("p", None)
        with self.assertRaises(ValueError) as assert_error:
            parentnode.to_html()
        self.assertEqual(assert_error.exception.args[0], "Children missing")
    def test_parent_no_tag(self):
        parentnode = ParentNode(None, [LeafNode("b", "Bold text")])
        with self.assertRaises(ValueError) as assert_error:
            parentnode.to_html()
        self.assertEqual(assert_error.exception.args[0], "Tag missing")
    def test_nested_children(self):
        parentnode = ParentNode("p", [ParentNode("h1", [LeafNode("b", "Bold Text")])])
        self.assertEqual(parentnode.to_html(), "<p><h1><b>Bold Text</b></h1></p>")
    def test_parent_pros(self):
        parentnode = ParentNode("div", [LeafNode("b", "Bold text")], {"class": "wrapper", "id": "main"})
        self.assertEqual(
        parentnode.to_html(),
        '<div class="wrapper" id="main"><b>Bold text</b></div>'
    )


if __name__ == "__main__":
    unittest.main()