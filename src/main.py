from textnode import TextNode,TextType
from copy_public_to_static import copy_content_src_to_dst
from generate_page import generate_page, generate_pages_recursive

def main():
    copy_content_src_to_dst("static",  "public", "public") 
    generate_pages_recursive("content", "template.html", "public")

main()