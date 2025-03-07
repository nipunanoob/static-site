from textnode import TextNode,TextType
from copy_public_to_static import copy_content_src_to_dst
from generate_page import generate_page

def main():
    copy_content_src_to_dst("static",  "public", "public") 
    generate_page("content/index.md", "template.html", "public/index.html")

main()