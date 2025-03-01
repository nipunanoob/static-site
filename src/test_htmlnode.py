
import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("b", "Bold text")
        node2 = HTMLNode("b", "Bold text")
        self.assertEqual(node1, node2)
    def test_props_to_hmtl_with_single_prop(self):
        props = {"href": "https://www.google.com"}
        node1 = HTMLNode("b", "Bold text",None,props)
        self.assertEqual(node1.props_to_html(), " href=\"https://www.google.com\"")
    def test_props_to_hmtl_with_multiple_props(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
                }
        node1 = HTMLNode("b", "Bold text",None,props)
        self.assertEqual(node1.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!",{"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Hello, world!</a>")
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_children_and_props(self):

if __name__ == "__main__":
    unittest.main()