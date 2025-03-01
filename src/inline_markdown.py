import re

from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        parts = old_node.text.split(delimiter)
        
        # delimiter has to have a start and an end
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter: {delimiter}")
        
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 1:
                current_type = text_type
            else:
                current_type = TextType.TEXT
            new_nodes.append(TextNode(parts[i], current_type))
        
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        matches = extract_markdown_images(remaining_text)
        if not matches:
                new_nodes.append(old_node)
                continue
        
        for match in matches:
            image_alt, image_link = match[0], match[1]
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
        
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        matches = extract_markdown_links(remaining_text)

        if not matches:
            new_nodes.append(old_node)
            continue

        for match in matches:
            hyperlink, url = match[0], match[1]
            sections = remaining_text.split(f"[{hyperlink}]({url})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
        
            new_nodes.append(TextNode(hyperlink, TextType.LINK, url))

            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
            matches = extract_markdown_links(remaining_text)
    
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text) 
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
