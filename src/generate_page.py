from markdown_parser import markdown_to_html_node
from htmlnode import HTMLNode


def extract_title(markdown):
    firstLine = markdown.split("\n")[0]
    if firstLine[0:2] == "# ":
        return firstLine[2:].rstrip()
    else:
        raise ValueError("Markdown string does not start with h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        markdown_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()

    html_string = markdown_to_html_node(markdown_content).to_html()
    html_title = extract_title(markdown_content)

    rendered_html = template_content.replace("{{ Title }}", html_title).replace("{{ Content }}", html_string)


    with open(dest_path, "w") as file:
        print(f"Adding content to {dest_path}")
        file.write(rendered_html)
    