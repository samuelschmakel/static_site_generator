import os
import shutil

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes 
from block_markdown import *

def main():
    # Remove anything from public
    for filename in os.listdir("public"):
        file_path = os.path.join("public", filename)

        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    # Copy all static files from static to public
    copy_contents("static", "public")

    # Write HTML page
    generate_pages_recursive("content", "template.html", "public")

def copy_contents(source, dest):
    isFile = os.path.isfile(source) 
    isFile = os.path.isfile(dest)
    isFolder = os.path.exists(source)
    isFolder = os.path.exists(dest)

    '''
    Step 1: Delete anything in dest
    '''
    for filename in os.listdir(dest):
        file_path = os.path.join(dest, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    '''
    Step 2: Extract all files and folders found in source and put them into a list.
    '''
    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest)
        elif os.path.isdir(file_path):
            dest_path = os.path.join(dest, filename)
            os.mkdir(dest_path)
            copy_contents(file_path, dest_path)
    pass

def extract_title(markdown):
    md_list = markdown.split("\n")
    for line in md_list:
        for i in range(0, len(line)):
            if line[i] == "#" and not line[i+1] == "#":
                if i == 0 or line[i-1] != "#":
                    return line.replace("#","").strip()
    raise Exception("There's no title!")

def generate_page(from_path, template_path, dest_path):

    if os.path.basename(from_path) == "index.md":
        dest_path = os.path.join(dest_path, "index.html")

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(from_path, 'r') as file:
        md = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    html_str = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_str)   
    
    with open(dest_path, 'w') as file:
        file.write(template)
    pass

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)

        if os.path.isfile(file_path):
            if file_path[-3:] == ".md":
                html_name = "index.html"
                dest_path = os.path.join(dest_dir_path, html_name)
                os.makedirs(dest_dir_path, exist_ok=True)
                generate_page(file_path, template_path, dest_dir_path)
        elif os.path.isdir(file_path):
            dest_path = os.path.join(dest_dir_path, filename)
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(file_path, template_path, dest_path)

    pass
    
main()
