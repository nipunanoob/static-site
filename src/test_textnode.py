import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_empty_url_vs_node(self):
        node1 = TextNode("This is a text node with no URL", TextType.TEXT)
        node2 = TextNode("This is a text node with no URL", TextType.TEXT, "")
        self.assertNotEqual(node1, node2)

    def test_different_text_type(self):
        node1 = TextNode("This is a text node with no URL", TextType.TEXT)
        node2 = TextNode("This is a text node with no URL", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_link_with_no_url(self):
        node = TextNode("This is a link node", TextType.LINK)
        with self.assertRaisesRegex(ValueError, "Missing link URL for tag"): 
            html_node = text_node_to_html_node(node)

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "This is a image node"})

    def test_image_with_no_url(self):
        node = TextNode("This is a image node", TextType.IMAGE)
        with self.assertRaisesRegex(ValueError, "Missing source image URL for tag"): 
            html_node = text_node_to_html_node(node)

    def test_invalid_text_type(self):
        node = TextNode("This is a image node", "test")
        with self.assertRaisesRegex(ValueError, f"Invalid TextType: {node.text_type}"):
            html_node = text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()