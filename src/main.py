from textnode import TextNode,TextType
from copy_public_to_static import copy_content_src_to_dst
from generate_page import generate_page, generate_pages_recursive
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_content_src_to_dst("static",  "docs", "docs") 
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()