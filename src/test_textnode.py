import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()