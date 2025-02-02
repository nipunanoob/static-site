import re

def extract_markdown_images(text):
    # find one or more substring with this format ![alt text](url)
    # return list of tuple in format [(alt text,url),...] {there can be multiple image in text}
    image_list = re.findall("!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return image_list
def extract_markdown_links(text):
    link_list = re.findall("(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return link_list

# print(extract_markdown_bold("sample **bold text** and **another**"))
