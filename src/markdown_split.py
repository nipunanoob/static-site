from textnode import TextNode, TextType
from extract_markdown import extract_markdown_links,extract_markdown_images

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue
        words = node.text.split(delimiter)
        if len(words) % 2 == 0:
            raise ValueError(f"Closing delimiter was not found for {delimiter}")
        for new_node_idx in range(len(words)):
            if new_node_idx % 2 == 0 and words[new_node_idx]!= "":
                new_nodes_list.append(TextNode(words[new_node_idx],TextType.TEXT))
            elif words[new_node_idx] != "":
                new_nodes_list.append(TextNode(words[new_node_idx],text_type))
    return new_nodes_list

def split_nodes_link(old_nodes):
    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue
        link_tuple_list = extract_markdown_links(node.text)
        if link_tuple_list == []:
            new_nodes_list.append(node)
            continue
        node_text = node.text
        for link_tuple in link_tuple_list:
            section = node_text.split(f"[{link_tuple[0]}]({link_tuple[1]})",1)
            if not section[0].isspace() and section[0] != "":
                new_nodes_list.append(TextNode(section[0],TextType.TEXT))
            new_nodes_list.append(TextNode(f"{link_tuple[0]}",TextType.LINK, f"{link_tuple[1]}"))
            node_text = section[1]
        if not section[1].isspace() and section[1] != "":
            new_nodes_list.append(TextNode(section[1],TextType.TEXT))
    return new_nodes_list
            
def split_nodes_image(old_nodes):
    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue
        image_tuple_list = extract_markdown_images(node.text)
        if image_tuple_list == []:
            new_nodes_list.append(node)
            continue
        node_text = node.text
        for link_tuple in image_tuple_list:
            section = node_text.split(f"![{link_tuple[0]}]({link_tuple[1]})",1)
            if not section[0].isspace() and section[0] != "":
                new_nodes_list.append(TextNode(section[0],TextType.TEXT))
            new_nodes_list.append(TextNode(f"{link_tuple[0]}",TextType.IMAGE, f"{link_tuple[1]}"))
            node_text = section[1]
        if not section[1].isspace() and section[1] != "":
            new_nodes_list.append(TextNode(section[1],TextType.TEXT))
    return new_nodes_list

# node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
# node = TextNode(" [boot](https://www.boot.dev) test [link](https://www.test.dev)",TextType.TEXT)
# print(split_nodes_link([node]))