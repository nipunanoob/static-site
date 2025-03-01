import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_empty_url_vs_node(self):
        node1 = TextNode("This is a text node with no URL", TextType.NORMAL)
        node2 = TextNode("This is a text node with no URL", TextType.NORMAL, "")
        self.assertNotEqual(node1, node2)

    def test_different_text_type(self):
        node1 = TextNode("This is a text node with no URL", TextType.NORMAL)
        node2 = TextNode("This is a text node with no URL", TextType.BOLD)
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()