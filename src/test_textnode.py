import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_url_is_none(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.url, None)
    def test_enum_repr(self): 
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")
    def test_string_repr(self): 
        node = TextNode("This is a text node", "normal")
        self.assertEqual(repr(node), "TextNode(This is a text node, normal, None)")
    def test_text_type_bold(self):
        node = TextNode("BOLD",TextType.BOLD)
        self.assertEqual(LeafNode("b","BOLD"), text_node_to_html_node(node))
    def test_text_type_text(self):
        node = TextNode("TEXT",TextType.TEXT)
        self.assertEqual(LeafNode(None,"TEXT"), text_node_to_html_node(node))
    def test_text_type_italic(self):
        node = TextNode("Italic",TextType.ITALIC)
        self.assertEqual(LeafNode("i","Italic"), text_node_to_html_node(node))
    def test_text_type_code(self):
        node = TextNode("Code",TextType.CODE)
        self.assertEqual(LeafNode("code","Code"), text_node_to_html_node(node))
    def test_text_type_link(self):
        node = TextNode("Link",TextType.LINK,"https://google.com")
        self.assertEqual(LeafNode("a","Link", {"href": "https://google.com"}), text_node_to_html_node(node))
    def test_text_type_image(self):
        node = TextNode(None,TextType.IMAGE,"https://google.com")
        self.assertEqual(LeafNode("img","",{"src": "https://google.com", "alt": ""}), text_node_to_html_node(node))
    def test_text_type_image_with_alt(self):
        node = TextNode("Alt text",TextType.IMAGE,"https://google.com")
        self.assertEqual(LeafNode("img","",{"src": "https://google.com", "alt": "Alt text"}), text_node_to_html_node(node))
    def test_text_type_text_missing_text_error(self):
        node = TextNode(None,TextType.ITALIC)
        with self.assertRaises(ValueError) as assert_error:
            text_node_to_html_node(node)
        self.assertEqual(assert_error.exception.args[0], "Text value can not be none")
    def test_text_type_missing_url_link(self):
        node = TextNode("test", TextType.LINK, "https://google.com")
        self.assertEqual(LeafNode("a","test",{"href": "https://google.com"}), text_node_to_html_node(node))
    def test_text_type_missing_url_iage(self):
        node = TextNode("test", TextType.IMAGE, "https://google.com")
        self.assertEqual(LeafNode("img","",{"src": "https://google.com", "alt" : "test"}), text_node_to_html_node(node))
if __name__ == "__main__":
    unittest.main()