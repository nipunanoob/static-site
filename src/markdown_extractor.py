import re
from textnode import TextNode,TextType
from textnode import split_nodes_delimiter

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
    stripped_blocks = [block.strip() for block in blocks if block != ""]
    return stripped_blocks

md = """

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items



"""

print(markdown_to_blocks(md))