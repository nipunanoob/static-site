from markdown_parser import markdown_to_html_node
from htmlnode import HTMLNode
import os

def extract_title(markdown):
    firstLine = markdown.split("\n")[0]
    if firstLine[0:2] == "# ":
        return firstLine[2:].rstrip()
    else:
        raise ValueError("Markdown string does not start with h1 header")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        markdown_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()

    html_string = markdown_to_html_node(markdown_content).to_html()
    html_title = extract_title(markdown_content)

    rendered_html = template_content.replace("{{ Title }}", html_title).replace("{{ Content }}", html_string)
    rendered_html = rendered_html.replace("href=\"/", f"href=\"{basepath}")
    rendered_html = rendered_html.replace("src=\"/", f"src=\"{basepath}")

    with open(dest_path, "w") as file:
        print(f"Adding content to {dest_path}")
        file.write(rendered_html)
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_list = os.listdir(dir_path_content)
    for content in content_list:
        content_path = os.path.join(dir_path_content, content)
        content_dest_path = os.path.join(dest_dir_path, content)
        if content.endswith(".md"):
            content_dest_path = content_dest_path.replace(".md",".html")
            print(content_dest_path)
            generate_page(content_path, template_path, content_dest_path, basepath)
        else:
            if os.path.isdir(content_path):
                if not os.path.exists(content_dest_path):
                    os.mkdir(content_dest_path)
                generate_pages_recursive(content_path, template_path, content_dest_path, basepath) 