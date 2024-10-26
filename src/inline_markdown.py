from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    #print(f"\nThis is old_nodes: {old_nodes[0]} with type {type(old_nodes[0])}, delimiter: {delimiter}, text_type: {text_type}\n")
    #print(f"\n old_nodes[0] has properties old_nodes[0].text: {old_nodes[0].text} and old_nodes[0].text_type: {old_nodes[0].text_type}\n")
    #print(f"\n old_nodes[0].text.index: {old_nodes[0].text.index(delimiter)}\n")
    #print(f"\n old_nodes[0].text.split(delimiter): {old_nodes[0].text.split(delimiter)} \n")
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            node_list.append(node)
            continue
        if node.text_type == TextType.TEXT.value:
            split_str = node.text.split(delimiter)
            if len(split_str) % 2 == 0:
                raise Exception("invalid Markdown syntax")
            delimited_string = False
            for sub_string in split_str:
                if sub_string == "":
                    delimited_string = not delimited_string
                    continue
                if delimited_string == False:
                    node_list.append(TextNode(sub_string, TextType.TEXT))
                    delimited_string = True
                else:
                    node_list.append(TextNode(sub_string, text_type))
                    delimited_string = False
    
    #if old_nodes[0].text_type == "text":
        #print("inside the text_type loop")
        #split_list = old_nodes[0].text.split(delimiter)
        #print(split_list)
        #node_list.append(TextNode(split_list[0],TextType.TEXT))
        #node_list.append(TextNode(split_list[1],TextType.CODE#))
        #node_list.append(TextNode(split_list[2],TextType.TEXT))

        #start = old_nodes[0].text.index(delimiter) + 1
        #text_substring = old_nodes[0].text[:start]
        #node_list.append(TextNode(text_substring,TextType.TEXT))
        #end = old_nodes[0].text
        #text2_substring = old_nodes[start+1:end]
    return(node_list)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1],))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0],TextType.LINK,link[1],))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_markdown_images(text):
    pattern = "!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = "(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
