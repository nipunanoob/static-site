import unittest

from markdown_split import split_nodes_delimiter,split_nodes_image,split_nodes_link
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
    def test_split_single_image(self):
        node = TextNode("This is text with a image ![rick roll](https://i.imgur.com/aKaOqIh.gif)",TextType.TEXT)
        self.assertEqual(split_nodes_image([node]),
                         [TextNode("This is text with a image ",TextType.TEXT, None),
                         TextNode("rick roll", TextType.IMAGE,"https://i.imgur.com/aKaOqIh.gif")])
    def test_split_multiple_image(self):
        node = TextNode("This is text with a image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and another ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",TextType.TEXT)
        self.assertEqual(split_nodes_image([node]),
                         [TextNode("This is text with a image ",TextType.TEXT, None),
                         TextNode("rick roll", TextType.IMAGE,"https://i.imgur.com/aKaOqIh.gif"),
                         TextNode(" and another ",TextType.TEXT),
                         TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])
    def test_split_image_beginning(self):
        node = TextNode("![to boot dev](https://www.boot.dev) image at start",TextType.TEXT)
        self.assertEqual(split_nodes_image([node]),
                         [TextNode("to boot dev", TextType.IMAGE,"https://www.boot.dev"),
                         TextNode(" image at start", TextType.TEXT, None)])
    def test_split_image_end(self):
        node = TextNode("image at end ![to youtube](https://www.youtube.com/@bootdotdev) ",TextType.TEXT)
        self.assertEqual(split_nodes_image([node]),
                         [TextNode("image at end ", TextType.TEXT, None),
                         TextNode("to youtube", TextType.IMAGE,"https://www.youtube.com/@bootdotdev")])
    def test_split_empty_image(self):
        node = TextNode("no image here bozo",TextType.TEXT)
        self.assertEqual(split_nodes_image([node]),
                         [TextNode("no image here bozo", TextType.TEXT, None)])
    def test_split_invalid_image(self):
        node = TextNode("no correct image here bozo [to youtube](youtube.com)",TextType.TEXT)
        self.assertEqual(split_nodes_image([node]),
                         [TextNode("no correct image here bozo [to youtube](youtube.com)",TextType.TEXT)])
    def test_split_single_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) ",TextType.TEXT)
        self.assertEqual(split_nodes_link([node]),
                         [TextNode("This is text with a link ",TextType.TEXT, None),
                         TextNode("to boot dev", TextType.LINK,"https://www.boot.dev")])
    def test_split_multiple_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        self.assertEqual(split_nodes_link([node]),
                         [TextNode("This is text with a link ",TextType.TEXT, None),
                         TextNode("to boot dev", TextType.LINK,"https://www.boot.dev"),
                         TextNode(" and ", TextType.TEXT, None),
                         TextNode("to youtube", TextType.LINK,"https://www.youtube.com/@bootdotdev")])
    def test_split_link_beginning(self):
        node = TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        self.assertEqual(split_nodes_link([node]),
                         [TextNode("to boot dev", TextType.LINK,"https://www.boot.dev"),
                         TextNode(" and ", TextType.TEXT, None),
                         TextNode("to youtube", TextType.LINK,"https://www.youtube.com/@bootdotdev")])
    def test_split_link_end(self):
        node = TextNode("end [to youtube](https://www.youtube.com/@bootdotdev) ",TextType.TEXT)
        self.assertEqual(split_nodes_link([node]),
                         [TextNode("end ", TextType.TEXT, None),
                         TextNode("to youtube", TextType.LINK,"https://www.youtube.com/@bootdotdev")])
    def test_split_empty_link(self):
        node = TextNode("no link here bozo",TextType.TEXT)
        self.assertEqual(split_nodes_link([node]),
                         [TextNode("no link here bozo", TextType.TEXT, None)])
    def test_split_invalid_link(self):
        node = TextNode("no correct link here bozo [to youtube](youtube.com",TextType.TEXT)
        self.assertEqual(split_nodes_link([node]),
                         [TextNode("no correct link here bozo [to youtube](youtube.com",TextType.TEXT)])
    