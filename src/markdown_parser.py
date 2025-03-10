import re
from textnode import TextNode,TextType
from textnode import split_nodes_delimiter, text_node_to_html_node
from htmlnode import ParentNode,LeafNode, HTMLNode
from enum import Enum

class BlockType(Enum):
   PARAGRAPH = "paragraph" 
   HEADING = "heading" 
   CODE = "code" 
   QUOTE = "quote" 
   UNORDERED = "unordered_list" 
   ORDERED = "ordered_list" 

def extract_markdown_images(text):
    return (re.findall(r"!\[([^\[\]]*)\]\(([^\)\(]*)\)", text))

def extract_markdown_links(text):
    return (re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\)\(]*)\)", text))

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_node_text = node.text
        image_tuple_list = extract_markdown_images(current_node_text)
        if image_tuple_list == []:
            new_nodes.append(node)
            continue
        for image_tuple in image_tuple_list:
            current_node_text_split = current_node_text.split(f"![{image_tuple[0]}]({image_tuple[1]})", 1)
            if current_node_text_split[0] != "":
                new_nodes.append(TextNode(current_node_text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(image_tuple[0], TextType.IMAGE, image_tuple[1]))
            current_node_text = current_node_text_split[1]
        if current_node_text_split[1] != "":
            new_nodes.append(TextNode(current_node_text_split[1], TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_node_text = node.text
        link_tuple_list = extract_markdown_links(current_node_text)
        if link_tuple_list == []:
            new_nodes.append(node)
            continue
        for link_tuple in link_tuple_list:
            current_node_text_split = current_node_text.split(f"[{link_tuple[0]}]({link_tuple[1]})", 1)
            if current_node_text_split[0] != "":
                new_nodes.append(TextNode(current_node_text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(link_tuple[0], TextType.LINK, link_tuple[1]))
            current_node_text = current_node_text_split[1]
        if current_node_text_split[1] != "":
            new_nodes.append(TextNode(current_node_text_split[1], TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    delimiter_dict = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE
    }
    for key, val in delimiter_dict.items():
        nodes = split_nodes_delimiter(nodes, key, val)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
     
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = list(filter(None, [block.strip() for block in blocks]))
    return stripped_blocks

def check_markdown_string_in_each_line(string, lines, blocktype):
    for line in lines:
        if not re.search(string, line):
            return BlockType.PARAGRAPH
    return blocktype

def block_to_block_type(block):
    if re.search("^#{1,6} ", block) and len(block.split("\n")) == 1:
        return BlockType.HEADING
    else:
        lines = block.split("\n")
        if re.search("^```", lines[0]) and re.search("```$", lines[-1]):
            return BlockType.CODE
        elif re.search("^>", lines[0]):
            return check_markdown_string_in_each_line("^>", lines[1:], BlockType.QUOTE)
        elif re.search("^- ", lines[0]):
            return check_markdown_string_in_each_line("^- ", lines[1:], BlockType.UNORDERED)
        elif re.search("^1. ", lines[0]):
            count = 1
            for line in lines:
                if not re.search(f"^{count}. ", line):
                    return BlockType.PARAGRAPH
                count += 1
            return BlockType.ORDERED
    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    html_blocks = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.PARAGRAPH:
            block_text = block.replace("\n", " ")
            paragraph_node = ParentNode("p", text_to_children(block_text))
            html_blocks.append(paragraph_node)
        elif blocktype == BlockType.CODE:
            block_text = block.replace("```","").rstrip('\r\t ').lstrip()
            if not block_text.endswith('\n'):
                block_text += '\n'
            text_node = LeafNode(None, block_text)
            code_node = ParentNode("code", [text_node])
            pre_node = ParentNode("pre",[code_node])
            html_blocks.append(pre_node)
        elif blocktype == BlockType.HEADING:
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            heading_text = block[level:].strip()
            heading_children = text_to_children(heading_text)

            heading_node = ParentNode(f"h{level}", heading_children)
            html_blocks.append(heading_node)

        elif blocktype == BlockType.QUOTE:
            quote_text = "\n".join([line.lstrip("> ").strip() for line in block.split("\n")])
            quote_children = text_to_children(quote_text)

            quote_node = ParentNode("blockquote", quote_children)
            html_blocks.append(quote_node)
        
        elif blocktype == BlockType.UNORDERED:
            list_items = []
            lines = block.split("\n")

            for line in lines:
                if line.strip().startswith("-"):
                    item_text = line[1:].strip()
                item_children = text_to_children(item_text)
                li_node = ParentNode("li", item_children)
                list_items.append(li_node)

            ul_node = ParentNode("ul", list_items)
            html_blocks.append(ul_node)  

        elif blocktype == BlockType.ORDERED:
            list_items = []
            lines = block.split("\n")

            for line_index in range(len(lines)):
                if lines[line_index].strip().startswith(f"{line_index + 1}."):
                    item_text = lines[line_index][2:].strip()
                item_children = text_to_children(item_text)
                li_node = ParentNode("li", item_children)
                list_items.append(li_node)

            ol_node = ParentNode("ol", list_items)
            html_blocks.append(ol_node)  

    htmlnode = ParentNode("div", html_blocks)
    # return htmlnode.to_html()
    return htmlnode

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        if node is not None:
            html_node = text_node_to_html_node(node)
            html_nodes.append(html_node)
    return html_nodes
