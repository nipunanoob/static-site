import unittest

from markdown_parser import *
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with an [link 1](https://i.imgur.com/zjjcJKZ.png) and [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("link 1", "https://i.imgur.com/zjjcJKZ.png"),
                              ("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image 1](https://i.imgur.com/zjjcJKZ.png) and ![to boot dev](https://www.boot.dev/img/maptexture2.webp)"
        )
        self.assertListEqual([("image 1", "https://i.imgur.com/zjjcJKZ.png"),
                              ("to boot dev", "https://www.boot.dev/img/maptexture2.webp")], matches)

    def test_extract_markdown_images_and_links(self):
        matches_links = extract_markdown_links(
            "This is text with an ![image 1](https://i.imgur.com/zjjcJKZ.png) and [to boot dev](https://www.boot.dev)"
        )
        matches_images = extract_markdown_images(
            "This is text with an ![image 1](https://i.imgur.com/zjjcJKZ.png) and [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches_links)
        self.assertListEqual([("image 1", "https://i.imgur.com/zjjcJKZ.png")], matches_images)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_end_image(self):
        node = TextNode(
            "image at end ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image at end ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_beginning_and_end_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) image at beginning and end ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" image at beginning and end ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_beginning_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) image at beginning",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" image at beginning", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_duplicate_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_no_images_or_links(self):
        node = TextNode(
            "no images or links",
            TextType.TEXT
        )
        new_nodes_images = split_nodes_image([node])
        new_nodes_links = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("no images or links", TextType.TEXT),
            ],
            new_nodes_images,
        )
        self.assertListEqual(
            [
                TextNode("no images or links", TextType.TEXT),
            ],
            new_nodes_links,
        )

    def test_split_consecutive_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_end_link(self):
        node = TextNode(
            "link at end [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link at end ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_beginning_and_end_link(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) link at beginning and end [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" link at beginning and end ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_beginning_link(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) link at beginning",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" link at beginning", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_duplicate_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_consecutive_links(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)[link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    ]
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_text_to_no_delimiter(self):
        text = "This is text with no delimiter"
        expected = [
                    TextNode("This is text with no delimiter", TextType.TEXT),
                    ]
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_text_to_image_and_links(self):
        text = "This is text with [link](https://boot.dev) and ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
                    TextNode("This is text with ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    ]
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_multiple_same_delimiters(self):
        text = "This has **two** separate **bold** sections"
        expected = [
        TextNode("This has ", TextType.TEXT),
        TextNode("two", TextType.BOLD),
        TextNode(" separate ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" sections", TextType.TEXT),
    ]
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_empty_string(self):
        text = ""
        expected = []
        self.assertListEqual(expected, text_to_textnodes(text))
    

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_single_block(self):
        md =  """
single block
"""
        expected = ["single block"]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_markdown_to_single_block_with_newline(self):
        md =  """
first line
second line
"""
        expected = ["first line\nsecond line"]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_markdown_to_empty_block(self):
        md =  """
"""
        expected = []
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_consecutive_new_lines(self):
        md =  """
first line



second line
"""
        expected = ["first line","second line"]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_heading_block(self):
        block = "## heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_invalid_heading_block(self):
        block = " ###heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    
    def test_code_block(self):
        block = """```
code block
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_invalid_code_block(self):
        block = """```
code block
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = "> quote 1\n> quote 2\n> quote 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_invalid_quote_block(self):
        block = "> quote 1\n> quote 2\n* quote3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_block(self):
        block = "- item1\n- item2\n- item3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED)

    def test_invalid_unordered_block(self):
        block = "- item1\n- item2\n* item3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_block(self):
        block = "1. item1\n2. item2\n3. item3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED)

    def test_invalid_numbered_list(self):
        block = "1. item1\n2. item2\n4. item3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_ordered_list(self):
        block = "1. item1\n2. item2\n3.item3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "no tricks"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_multiline_heading(self):
        block = "## heading1\n# heading2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headingblock(self):
        md = """
## heading 1

#### heading 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>heading 1</h2><h4>heading 2</h4></div>"
        )

    def test_quoteblock(self):
        md = """
> john cena
> is a villain

> damn
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>john cena\nis a villain</blockquote><blockquote>damn</blockquote></div>"
        )

    def test_unorderedblock(self):
        md = """
- i am bored
- feed me
- sigh

- lol
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>i am bored</li><li>feed me</li><li>sigh</li></ul><ul><li>lol</li></ul></div>"
        )

    def test_orderedblock(self):
        md = """
1. i am bored
2. feed me
3. sigh

1. lol
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>i am bored</li><li>feed me</li><li>sigh</li></ol><ol><li>lol</li></ol></div>"
        )

if __name__ == "__main__":
    unittest.main()