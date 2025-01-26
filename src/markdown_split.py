from textnode import TextNode, TextType

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

node = TextNode("", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
print(new_nodes)