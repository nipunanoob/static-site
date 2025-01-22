
import unittest

from htmlnode import HTMLNode,LeafNode

class TestTextNode(unittest.TestCase):
    def test_type(self):
        node = HTMLNode("p","sample",props={"href": "https://www.google.com"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "sample")
        self.assertEqual(node.props, {"href": "https://www.google.com"})
    def test_props_to_html(self):
        node = HTMLNode("p","sample",props={"href": "https://www.google.com",
                                            "target": "_blank",})
        props_string = node.props_to_html
        self.assertTrue(props_string, "href=\"https://www.google.com\" target=\"_blank\"")  
    def test_repr(self): 
        node = HTMLNode("p","sample",props={"href": "https://www.google.com"})
        self.assertEqual(repr(node), "HTMLNode(p, sample, None, {'href': 'https://www.google.com'})")
    def test_leaf_to_html_valid(self):
        leafnode = LeafNode("p", "This is a paragraph of text.", None)
        self.assertTrue(leafnode.to_html, "<p>This is a paragraph of text.</p>")
    def test_leaf_to_html_value_missing(self):
        leafnode = LeafNode("p", None, None)
        self.assertRaises(ValueError,leafnode.to_html)
    def test_leaf_to_html_tag_missing(self):
        leafnode = LeafNode("None", "This is raw", None)
        self.assertTrue(leafnode.to_html(),"This is raw")

if __name__ == "__main__":
    unittest.main()