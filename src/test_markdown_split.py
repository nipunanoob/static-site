import unittest

from markdown_split import split_nodes_delimiter
from textnode import TextNode,TextType

class TestMarkdownSplit(unittest.TestCase):
    def test_single_delimiter(self):
        node = TextNode("This is a single `code block` yay!",TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node],"`",TextType.CODE),[
            TextNode("This is a single ",TextType.TEXT),
            TextNode("code block",TextType.CODE),
            TextNode(" yay!",TextType.TEXT)
        ])
    def test_no_delimiter(self):
        node = TextNode("This has no delimiter",TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node],"`",TextType.CODE),[
            TextNode("This has no delimiter",TextType.TEXT)
        ])
    def test_multiple_delimiter(self):
        node = TextNode("This has `one code snippet` and `another code snippet` huzzah",TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node],"`",TextType.CODE),[
            TextNode("This has ",TextType.TEXT),
            TextNode("one code snippet",TextType.CODE),
            TextNode(" and ",TextType.TEXT),
            TextNode("another code snippet",TextType.CODE),
            TextNode(" huzzah",TextType.TEXT)
        ])
    def test_unclosed_delimiter(self):
        node = TextNode("This is raise error`", TextType.TEXT)
        with self.assertRaises(ValueError) as assert_error:
            split_nodes_delimiter([node],"`",TextType.CODE)
        self.assertEqual(assert_error.exception.args[0], "Closing delimiter was not found for `")
    def test_empty(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node],"`",TextType.CODE),[])
    def test_consecutive_delimiter(self):
        node = TextNode("`code1``code2`", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node],"`",TextType.CODE),[
            TextNode("code1", TextType.CODE),
            TextNode("code2", TextType.CODE)
        ])
    def test_edge_delimiter(self):
        node = TextNode("`This is edge` delimiter", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node],"`",TextType.CODE),[
            TextNode("This is edge", TextType.CODE),
            TextNode(" delimiter", TextType.TEXT)
        ])